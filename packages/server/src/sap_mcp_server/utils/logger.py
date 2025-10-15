"""Structured logging configuration for SAP MCP Server"""

import logging
import sys
from typing import Any, Optional

import structlog
from structlog.types import FilteringBoundLogger


def setup_logging(
    level: str = "INFO",
    json_logs: bool = False,
    include_timestamp: bool = True,
) -> FilteringBoundLogger:
    """Configure structured logging for the application

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: If True, output logs in JSON format
        include_timestamp: If True, include timestamp in logs

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging(level="DEBUG", json_logs=True)
        >>> logger.info("Server started", port=8080, transport="stdio")
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Build processor chain
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
    ]

    if include_timestamp:
        processors.append(structlog.processors.TimeStamper(fmt="iso"))

    processors.extend([
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ])

    # Choose renderer based on format
    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(
            structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())
        )

    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger(name: Optional[str] = None) -> FilteringBoundLogger:
    """Get a logger instance with the given name

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing request", request_id="123")
    """
    return structlog.get_logger(name)


def log_function_call(
    logger: FilteringBoundLogger,
    func_name: str,
    **kwargs: Any,
) -> None:
    """Log a function call with parameters

    Args:
        logger: Logger instance
        func_name: Name of the function being called
        **kwargs: Function parameters to log

    Example:
        >>> logger = get_logger(__name__)
        >>> log_function_call(logger, "authenticate", username="admin", host="sap.example.com")
    """
    logger.debug(
        "Function call",
        function=func_name,
        **kwargs,
    )


def log_performance(
    logger: FilteringBoundLogger,
    operation: str,
    duration_ms: float,
    **kwargs: Any,
) -> None:
    """Log performance metrics for an operation

    Args:
        logger: Logger instance
        operation: Name of the operation
        duration_ms: Duration in milliseconds
        **kwargs: Additional context

    Example:
        >>> logger = get_logger(__name__)
        >>> log_performance(logger, "sap_query", 1234.5, entity_set="OrderSet", rows=100)
    """
    logger.info(
        "Performance metric",
        operation=operation,
        duration_ms=duration_ms,
        **kwargs,
    )


def log_error_with_context(
    logger: FilteringBoundLogger,
    error: Exception,
    context: str,
    **kwargs: Any,
) -> None:
    """Log an error with rich context

    Args:
        logger: Logger instance
        error: The exception that occurred
        context: Description of what was being done when error occurred
        **kwargs: Additional context

    Example:
        >>> logger = get_logger(__name__)
        >>> try:
        ...     # some code
        ... except Exception as e:
        ...     log_error_with_context(logger, e, "SAP authentication", host="sap.example.com")
    """
    logger.error(
        "Error occurred",
        context=context,
        error_type=type(error).__name__,
        error_message=str(error),
        **kwargs,
        exc_info=error,
    )


# Global logger instance
_default_logger: Optional[FilteringBoundLogger] = None


def get_default_logger() -> FilteringBoundLogger:
    """Get the default application logger

    Returns:
        Default logger instance

    Example:
        >>> from sap_mcp_server.utils.logger import get_default_logger
        >>> logger = get_default_logger()
        >>> logger.info("Application started")
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logging()
    return _default_logger
