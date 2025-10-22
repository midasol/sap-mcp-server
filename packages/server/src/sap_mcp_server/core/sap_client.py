"""SAP Gateway client implementation"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union, cast

import aiohttp
import xmltodict

from sap_mcp_server.config.schemas import GatewayConfig
from sap_mcp_server.config.loader import get_services_config
from sap_mcp_server.config.settings import SAPConnectionConfig, get_services_config_path
from sap_mcp_server.core.auth import SAPAuthenticator
from sap_mcp_server.core.exceptions import (
    SAPAuthenticationError,
    SAPConnectionError,
    SAPRequestError,
    SAPTimeoutError,
    SAPValidationError,
)

logger = logging.getLogger(__name__)


class SAPClient:
    """SAP Gateway OData client with authentication and session management"""

    def __init__(
        self,
        config: SAPConnectionConfig,
        gateway_config: Optional[GatewayConfig] = None,
    ):
        self.config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_lock = asyncio.Lock()

        # Load gateway configuration
        if gateway_config is None:
            from sap_mcp_server.config.loader import get_services_config

            self.services_config = get_services_config(get_services_config_path())
            self.gateway_config = self.services_config.gateway
        else:
            self.services_config = None
            self.gateway_config = gateway_config

        # Initialize authenticator with auth endpoint configuration
        self.authenticator = SAPAuthenticator(
            config=config,
            auth_endpoint=self.gateway_config.auth_endpoint,
            services_config=self.services_config,
        )

        # Build base URLs using gateway configuration
        self.base_url = f"https://{config.host}:{config.port}"
        self.odata_base = self.gateway_config.base_url_pattern.format(
            host=config.host, port=config.port
        )

    async def __aenter__(self) -> "SAPClient":
        """Async context manager entry"""
        await self._ensure_session()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Async context manager exit"""
        await self.close()

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure HTTP session is created"""
        async with self._session_lock:
            if self._session is None or self._session.closed:
                timeout = aiohttp.ClientTimeout(total=self.config.timeout)

                # Create SSL context when verification is disabled (for self-signed certs)
                ssl_context = None
                if not self.config.verify_ssl:
                    import ssl

                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    logger.warning("SSL certificate verification is disabled")

                connector = aiohttp.TCPConnector(
                    ssl=ssl_context if ssl_context else True,
                    limit=100,  # Connection pool limit
                    limit_per_host=10,
                )

                self._session = aiohttp.ClientSession(
                    timeout=timeout, connector=connector
                )

        return self._session

    async def close(self) -> None:
        """Close the HTTP session"""
        async with self._session_lock:
            if self._session and not self._session.closed:
                await self._session.close()
                self._session = None

    async def authenticate(self) -> bool:
        """Authenticate with SAP Gateway"""
        try:
            await self.authenticator.get_valid_token()
            logger.info("SAP authentication successful")
            return True
        except Exception as e:
            logger.error(f"SAP authentication failed: {str(e)}")
            return False

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Union[str, Dict[str, Any]]] = None,
        params: Optional[Dict[str, str]] = None,
        retry_count: int = 0,
        read_response: bool = True,
    ) -> Union[aiohttp.ClientResponse, str]:
        """Make authenticated HTTP request to SAP

        Args:
            read_response: If True, reads response body as text and returns it.
                         If False, returns the response object (caller must read).
        """

        if retry_count >= self.config.retry_attempts:
            raise SAPRequestError(
                f"Max retry attempts ({self.config.retry_attempts}) exceeded"
            )

        # Get valid authentication token
        try:
            token = await self.authenticator.get_valid_token()
        except Exception as e:
            raise SAPAuthenticationError(
                f"Failed to get authentication token: {str(e)}"
            )

        # Prepare headers
        request_headers = self.authenticator.get_auth_headers(token)
        if headers:
            request_headers.update(headers)

        # Prepare session
        session = await self._ensure_session()

        # Set cookies from token
        for name, value in token.cookies.items():
            session.cookie_jar.update_cookies({name: value})

        # Prepare data
        if isinstance(data, dict):
            data = json.dumps(data)
            request_headers["Content-Type"] = "application/json"

        # Ensure sap-client parameter is always included
        if params is None:
            params = {}
        if "sap-client" not in params:
            params["sap-client"] = self.config.client

        try:
            async with session.request(
                method=method,
                url=url,
                headers=request_headers,
                data=data,
                params=params,
            ) as response:

                # Handle authentication errors
                if response.status == 401:
                    logger.warning("Authentication token expired, refreshing...")
                    await self.authenticator.invalidate_token()
                    # Retry with new token
                    return await self._make_request(
                        method,
                        url,
                        headers,
                        data,
                        params,
                        retry_count + 1,
                        read_response,
                    )

                # Handle other errors
                if response.status >= 400:
                    error_text = await response.text()
                    raise SAPRequestError(
                        f"SAP request failed: {response.status} - {error_text}",
                        status_code=response.status,
                        response_data={"url": url, "method": method},
                    )

                # Read response body if requested (to avoid connection closing issues)
                if read_response:
                    response_text = await response.text()
                    return response_text
                else:
                    return response

        except asyncio.TimeoutError:
            raise SAPTimeoutError(f"Request timeout for {method} {url}")
        except aiohttp.ClientError as e:
            if retry_count < self.config.retry_attempts - 1:
                logger.warning(
                    f"Request failed, retrying "
                    f"({retry_count + 1}/{self.config.retry_attempts}): {str(e)}"
                )
                await asyncio.sleep(2**retry_count)  # Exponential backoff
                return await self._make_request(
                    method, url, headers, data, params, retry_count + 1, read_response
                )
            else:
                raise SAPConnectionError(f"Connection error: {str(e)}")

    async def get_service_metadata(self, service_path: str) -> Dict[str, Any]:
        """Get OData service metadata"""
        url = f"{self.odata_base}{service_path}/$metadata"

        headers = {"Accept": "application/xml"}
        xml_content = await self._make_request(
            "GET", url, headers=headers, read_response=True
        )

        # Parse XML metadata
        try:
            metadata = xmltodict.parse(xml_content)
            logger.info(f"Retrieved metadata for service: {service_path}")
            return cast(Dict[str, Any], metadata)
        except Exception as e:
            raise SAPValidationError(f"Failed to parse metadata XML: {str(e)}")

    async def list_services(self) -> List[Dict[str, Any]]:
        """List available OData services"""
        # Use catalog path from gateway configuration
        catalog_path = self.gateway_config.service_catalog_path
        # If catalog path is absolute, use it; otherwise append to odata_base
        if catalog_path.startswith("http"):
            url = catalog_path
        else:
            url = f"{self.base_url}{catalog_path}"

        # Add Accept header for JSON format
        headers = {"Accept": "application/json"}

        response_text = await self._make_request(
            "GET", url, headers=headers, read_response=True
        )
        data = json.loads(response_text)

        # Extract service information
        services = []
        if "d" in data and "results" in data["d"]:
            for service in data["d"]["results"]:
                services.append(
                    {
                        "id": service.get("ID"),
                        "title": service.get("Title"),
                        "version": service.get("Version"),
                        "url": service.get("TechnicalServiceName"),
                    }
                )

        logger.info(f"Retrieved {len(services)} available services")
        return services

    async def query_entity_set(
        self,
        service_path: str,
        entity_set: str,
        filters: Optional[Dict[str, Any]] = None,
        select_fields: Optional[List[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Query an OData entity set"""

        # Build URL
        url = f"{self.odata_base}{service_path}/{entity_set}"

        # Add Accept header for JSON format
        headers = {"Accept": "application/json"}

        # Build query parameters
        params = {}

        if filters:
            filter_expressions = []
            for key, value in filters.items():
                if isinstance(value, str):
                    filter_expressions.append(f"{key} eq '{value}'")
                else:
                    filter_expressions.append(f"{key} eq {value}")
            if filter_expressions:
                params["$filter"] = " and ".join(filter_expressions)

        if select_fields:
            params["$select"] = ",".join(select_fields)

        if top is not None:
            params["$top"] = str(top)

        if skip is not None:
            params["$skip"] = str(skip)

        # Add format parameter for JSON response
        params["$format"] = "json"

        response_text = await self._make_request(
            "GET", url, headers=headers, params=params, read_response=True
        )
        data = json.loads(response_text)

        logger.info(f"Queried entity set {entity_set} from service {service_path}")
        return cast(Dict[str, Any], data)

    async def create_entity(
        self, service_path: str, entity_set: str, entity_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new entity in the specified entity set"""

        url = f"{self.odata_base}{service_path}/{entity_set}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response_text = await self._make_request(
            "POST", url, headers=headers, data=entity_data, read_response=True
        )

        # For successful POST, parse the response
        data = json.loads(response_text)
        logger.info(f"Created entity in {entity_set}")
        return cast(Dict[str, Any], data)

    async def update_entity(
        self,
        service_path: str,
        entity_set: str,
        entity_key: str,
        entity_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Update an existing entity"""

        url = f"{self.odata_base}{service_path}/{entity_set}('{entity_key}')"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response_text = await self._make_request(
            "PUT", url, headers=headers, data=entity_data, read_response=True
        )

        # Parse response if not empty (204 No Content returns empty string)
        if response_text:
            data = json.loads(response_text)
            return cast(Dict[str, Any], data)
        else:
            return {"status": "updated"}

    async def delete_entity(
        self, service_path: str, entity_set: str, entity_key: str
    ) -> bool:
        """Delete an entity"""

        url = f"{self.odata_base}{service_path}/{entity_set}('{entity_key}')"

        # DELETE typically returns 204 No Content (empty response)
        response_text = await self._make_request("DELETE", url, read_response=True)

        logger.info(f"Deleted entity {entity_key} from {entity_set}")
        return True

    async def get_entity(
        self,
        service_path: str,
        entity_set: str,
        entity_key: str,
        select_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Get a specific entity by key"""

        url = f"{self.odata_base}{service_path}/{entity_set}('{entity_key}')"

        # Add Accept header for JSON format
        headers = {"Accept": "application/json"}

        params = {"$format": "json"}
        if select_fields:
            params["$select"] = ",".join(select_fields)

        try:
            response_text = await self._make_request(
                "GET", url, headers=headers, params=params, read_response=True
            )
            logger.debug(f"Response text: {response_text[:500]}")

            # Parse JSON from the text
            data = json.loads(response_text)

            logger.info(f"Retrieved entity {entity_key} from {entity_set}")
            return cast(Dict[str, Any], data)

        except Exception as e:
            logger.error(f"Error in get_entity: {str(e)}")
            raise
