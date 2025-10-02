"""SAP authentication handling"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional

import aiohttp

from ..config.settings import SAPConnectionConfig
from .exceptions import SAPAuthenticationError, SAPConnectionError

logger = logging.getLogger(__name__)


@dataclass
class AuthToken:
    """Represents an SAP authentication token"""

    csrf_token: str
    cookies: Dict[str, str]
    expires_at: datetime
    session_id: Optional[str] = None

    @property
    def is_expired(self) -> bool:
        """Check if token is expired"""
        return datetime.utcnow() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if token is valid"""
        return bool(self.csrf_token and not self.is_expired)


class SAPAuthenticator:
    """Handles SAP Gateway authentication with CSRF tokens"""

    def __init__(self, config: SAPConnectionConfig):
        self.config = config
        self._current_token: Optional[AuthToken] = None
        self._auth_lock = asyncio.Lock()

        # Build base URL
        protocol = "https" if self.config.verify_ssl else "http"
        self.base_url = f"{protocol}://{self.config.host}:{self.config.port}"

    async def get_valid_token(self) -> AuthToken:
        """Get a valid authentication token, refreshing if necessary"""
        async with self._auth_lock:
            if self._current_token and self._current_token.is_valid:
                return self._current_token

            logger.info("Authenticating with SAP Gateway...")
            self._current_token = await self._authenticate()
            return self._current_token

    async def _authenticate(self) -> AuthToken:
        """Perform SAP authentication and get CSRF token"""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=aiohttp.TCPConnector(verify_ssl=self.config.verify_ssl),
        ) as session:

            # Step 1: Get initial session and CSRF token
            csrf_token, cookies = await self._get_csrf_token(session)

            # Step 2: Authenticate with credentials
            await self._authenticate_session(session, csrf_token, cookies)

            # Create token with expiration (SAP sessions typically last 30 minutes)
            expires_at = datetime.utcnow() + timedelta(minutes=30)

            return AuthToken(
                csrf_token=csrf_token, cookies=cookies, expires_at=expires_at
            )

    async def _get_csrf_token(
        self, session: aiohttp.ClientSession
    ) -> tuple[str, Dict[str, str]]:
        """Get CSRF token from SAP Gateway"""
        url = f"{self.base_url}/sap/bc/rest/csrf"

        headers = {"X-CSRF-Token": "Fetch", "Accept": "application/json"}

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    csrf_token = response.headers.get("X-CSRF-Token")
                    if not csrf_token:
                        raise SAPAuthenticationError("No CSRF token in response")

                    # Extract cookies
                    cookies: Dict[str, str] = {}
                    for cookie_name, cookie_obj in response.cookies.items():
                        cookies[cookie_name] = cookie_obj.value

                    logger.info("CSRF token obtained successfully")
                    return csrf_token, cookies

                else:
                    error_text = await response.text()
                    raise SAPAuthenticationError(
                        f"Failed to get CSRF token: {response.status} - {error_text}",
                        status_code=response.status,
                    )

        except asyncio.TimeoutError:
            raise SAPConnectionError("Timeout while getting CSRF token")
        except aiohttp.ClientError as e:
            raise SAPConnectionError(
                f"Connection error while getting CSRF token: {str(e)}"
            )

    async def _authenticate_session(
        self, session: aiohttp.ClientSession, csrf_token: str, cookies: Dict[str, str]
    ) -> None:
        """Authenticate the session with user credentials"""

        # For basic authentication, we'll use the service metadata endpoint
        # This validates credentials without requiring a specific service call
        url = f"{self.base_url}/sap/opu/odata/IWFND/CATALOGSERVICE;v=2/$metadata"

        headers = {
            "X-CSRF-Token": csrf_token,
            "Accept": "application/xml",
            "Authorization": self._build_auth_header(),
        }

        # Set cookies from CSRF call
        for name, value in cookies.items():
            session.cookie_jar.update_cookies({name: value})

        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    logger.info(
                        f"Authentication successful for user: {self.config.username}"
                    )
                    return

                elif response.status == 401:
                    error_text = await response.text()
                    raise SAPAuthenticationError(
                        f"Invalid credentials for user {self.config.username}: {error_text}",
                        status_code=401,
                    )

                else:
                    error_text = await response.text()
                    raise SAPAuthenticationError(
                        f"Authentication failed: {response.status} - {error_text}",
                        status_code=response.status,
                    )

        except asyncio.TimeoutError:
            raise SAPConnectionError("Timeout during authentication")
        except aiohttp.ClientError as e:
            raise SAPConnectionError(
                f"Connection error during authentication: {str(e)}"
            )

    def _build_auth_header(self) -> str:
        """Build Authorization header for basic auth"""
        import base64

        credentials = f"{self.config.username}:{self.config.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    async def invalidate_token(self) -> None:
        """Invalidate the current token"""
        async with self._auth_lock:
            self._current_token = None
            logger.info("Authentication token invalidated")

    def get_auth_headers(self, token: AuthToken) -> Dict[str, str]:
        """Get headers for authenticated requests"""
        return {
            "X-CSRF-Token": token.csrf_token,
            "Authorization": self._build_auth_header(),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
