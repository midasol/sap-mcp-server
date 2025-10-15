"""SAP-specific exceptions"""

from typing import Any, Dict, Optional


class SAPError(Exception):
    """Base exception for SAP-related errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class SAPAuthenticationError(SAPError):
    """Raised when SAP authentication fails"""

    pass


class SAPConnectionError(SAPError):
    """Raised when SAP connection fails"""

    pass


class SAPRequestError(SAPError):
    """Raised when SAP request fails"""

    pass


class SAPTimeoutError(SAPError):
    """Raised when SAP request times out"""

    pass


class SAPValidationError(SAPError):
    """Raised when request validation fails"""

    pass
