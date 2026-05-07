"""Input validation helpers for SAP MCP Server"""

import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from pydantic import ValidationError


def validate_odata_filter(filter_expr: str) -> bool:
    """Validate OData filter expression syntax

    Args:
        filter_expr: OData filter expression (e.g., "OrderID eq '12345'")

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_odata_filter("OrderID eq '12345'")
        True
        >>> validate_odata_filter("OrderID = 12345")  # Invalid syntax
        False
    """
    # Basic validation - check for common OData operators
    odata_operators = [
        r"\beq\b",  # equals
        r"\bne\b",  # not equals
        r"\bgt\b",  # greater than
        r"\bge\b",  # greater than or equal
        r"\blt\b",  # less than
        r"\ble\b",  # less than or equal
        r"\band\b",  # logical and
        r"\bor\b",  # logical or
        r"\bnot\b",  # logical not
    ]

    pattern = "|".join(odata_operators)
    return bool(re.search(pattern, filter_expr, re.IGNORECASE))


def validate_entity_key(key: str) -> bool:
    """Validate entity key format

    Args:
        key: Entity key value

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_entity_key("12345")
        True
        >>> validate_entity_key("")
        False
    """
    # Keys should be non-empty strings with alphanumeric characters
    # Can include hyphens, underscores, and periods
    if not key or not isinstance(key, str):
        return False

    return bool(re.match(r"^[a-zA-Z0-9._-]+$", key))


def validate_field_name(field_name: str) -> bool:
    """Validate OData field name

    Args:
        field_name: Field name to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_field_name("OrderID")
        True
        >>> validate_field_name("Order-ID")  # Invalid character
        False
    """
    # Field names should start with letter or underscore
    # Can contain letters, numbers, and underscores
    if not field_name or not isinstance(field_name, str):
        return False

    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", field_name))


def validate_service_path(path: str) -> bool:
    """Validate SAP OData service path

    Args:
        path: Service path (e.g., "/sap/opu/odata/sap/Z_ORDER_SRV")

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_service_path("/sap/opu/odata/sap/Z_ORDER_SRV")
        True
        >>> validate_service_path("invalid path")
        False
    """
    # Service path should start with / and contain valid characters
    if not path or not isinstance(path, str):
        return False

    return bool(re.match(r"^/[a-zA-Z0-9/_-]+$", path))


def validate_url(url: str, require_https: bool = False) -> bool:
    """Validate URL format

    Args:
        url: URL to validate
        require_https: If True, only accept HTTPS URLs

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_url("https://sap.example.com:8000")
        True
        >>> validate_url("http://sap.example.com", require_https=True)
        False
    """
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False

        if require_https and result.scheme != "https":
            return False

        return result.scheme in ["http", "https"]
    except Exception:
        return False


def validate_port(port: int) -> bool:
    """Validate port number

    Args:
        port: Port number

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_port(8000)
        True
        >>> validate_port(70000)
        False
    """
    return isinstance(port, int) and 1 <= port <= 65535


def validate_select_fields(fields: str) -> List[str]:
    """Validate and parse OData $select parameter

    Args:
        fields: Comma-separated list of field names

    Returns:
        List of valid field names

    Raises:
        ValueError: If any field name is invalid

    Example:
        >>> validate_select_fields("OrderID,CustomerName,OrderDate")
        ['OrderID', 'CustomerName', 'OrderDate']
        >>> validate_select_fields("OrderID,Invalid-Field")
        Traceback (most recent call last):
        ...
        ValueError: Invalid field name: Invalid-Field
    """
    field_list = [f.strip() for f in fields.split(",")]

    for field in field_list:
        if not validate_field_name(field):
            raise ValueError(f"Invalid field name: {field}")

    return field_list


def validate_pagination_params(top: Optional[int] = None, skip: Optional[int] = None) -> Dict[str, int]:
    """Validate OData pagination parameters

    Args:
        top: Maximum number of records ($top)
        skip: Number of records to skip ($skip)

    Returns:
        Dict with validated pagination parameters

    Raises:
        ValueError: If parameters are invalid

    Example:
        >>> validate_pagination_params(top=10, skip=5)
        {'top': 10, 'skip': 5}
        >>> validate_pagination_params(top=-1)
        Traceback (most recent call last):
        ...
        ValueError: $top must be a positive integer
    """
    result = {}

    if top is not None:
        if not isinstance(top, int) or top <= 0:
            raise ValueError("$top must be a positive integer")
        if top > 10000:  # Reasonable limit
            raise ValueError("$top cannot exceed 10000")
        result["top"] = top

    if skip is not None:
        if not isinstance(skip, int) or skip < 0:
            raise ValueError("$skip must be a non-negative integer")
        result["skip"] = skip

    return result


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """Sanitize user input to prevent injection attacks

    Args:
        value: Input value to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized input string

    Raises:
        ValueError: If input is too long or contains dangerous characters

    Example:
        >>> sanitize_input("OrderID")
        'OrderID'
        >>> sanitize_input("A" * 2000)
        Traceback (most recent call last):
        ...
        ValueError: Input exceeds maximum length of 1000 characters
    """
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    if len(value) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length} characters")

    # Check for potentially dangerous characters
    dangerous_patterns = [
        r"<script",  # XSS
        r"javascript:",  # XSS
        r"on\w+=",  # Event handlers
        r"--",  # SQL comment
        r";.*--",  # SQL injection
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, value, re.IGNORECASE):
            raise ValueError(f"Input contains potentially dangerous content: {pattern}")

    return value


def validate_tool_arguments(
    arguments: Dict[str, Any],
    schema: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate tool arguments against JSON schema

    Args:
        arguments: Tool arguments to validate
        schema: JSON schema defining required structure

    Returns:
        Validated arguments

    Raises:
        ValueError: If arguments don't match schema

    Example:
        >>> schema = {
        ...     "type": "object",
        ...     "properties": {"service": {"type": "string"}},
        ...     "required": ["service"]
        ... }
        >>> validate_tool_arguments({"service": "Z_ORDER_SRV"}, schema)
        {'service': 'Z_ORDER_SRV'}
    """
    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in arguments:
            raise ValueError(f"Missing required argument: {field}")

    # Basic type checking
    properties = schema.get("properties", {})
    for key, value in arguments.items():
        if key in properties:
            expected_type = properties[key].get("type")
            if expected_type == "string" and not isinstance(value, str):
                raise ValueError(f"Argument '{key}' must be a string")
            elif expected_type == "integer" and not isinstance(value, int):
                raise ValueError(f"Argument '{key}' must be an integer")

    return arguments
