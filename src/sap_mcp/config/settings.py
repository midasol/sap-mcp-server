"""Configuration settings for SAP MCP Server"""

from typing import Dict, List, Optional
from pydantic import BaseSettings, Field, validator
import os


class SAPConnectionConfig(BaseSettings):
    """SAP Gateway connection configuration"""
    
    host: str = Field(..., description="SAP server hostname")
    port: int = Field(44300, description="SAP server port")
    client: str = Field("100", description="SAP client number")
    username: str = Field(..., description="SAP username")
    password: str = Field(..., description="SAP password")
    verify_ssl: bool = Field(True, description="Verify SSL certificates")
    timeout: int = Field(30, description="Request timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts")
    
    class Config:
        env_prefix = "SAP_"
        
    @validator("host")
    def validate_host(cls, v):
        if not v or not v.strip():
            raise ValueError("SAP host cannot be empty")
        return v.strip()
    
    @validator("port")
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


class MCPServerConfig(BaseSettings):
    """MCP server configuration"""
    
    host: str = Field("0.0.0.0", description="Server bind address")
    port: int = Field(8000, description="Server port")
    log_level: str = Field("INFO", description="Logging level")
    max_workers: int = Field(10, description="Maximum worker threads")
    debug: bool = Field(False, description="Enable debug mode")
    
    class Config:
        env_prefix = "MCP_"
    
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()


class SecurityConfig(BaseSettings):
    """Security configuration"""
    
    session_timeout: int = Field(3600, description="Session timeout in seconds")
    max_concurrent_sessions: int = Field(100, description="Maximum concurrent sessions")
    rate_limit_per_minute: int = Field(60, description="Rate limit per minute")
    encryption_key: Optional[str] = Field(None, description="Encryption key for sensitive data")
    
    class Config:
        env_prefix = "SECURITY_"
    
    @validator("session_timeout")
    def validate_session_timeout(cls, v):
        if v <= 0:
            raise ValueError("Session timeout must be positive")
        return v


class SAPServiceConfig(BaseSettings):
    """SAP service-specific configuration"""
    
    name: str
    path: str
    version: str = "v2"
    entities: List[str] = []
    custom_headers: Dict[str, str] = {}
    
    @validator("version")
    def validate_version(cls, v):
        if v not in ["v2", "v4"]:
            raise ValueError("OData version must be v2 or v4")
        return v


class AppConfig(BaseSettings):
    """Main application configuration"""
    
    # Core configurations
    sap: SAPConnectionConfig
    server: MCPServerConfig
    security: SecurityConfig
    
    # Optional configurations
    services: Dict[str, SAPServiceConfig] = {}
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        return cls(
            sap=SAPConnectionConfig(),
            server=MCPServerConfig(),
            security=SecurityConfig()
        )
    
    @classmethod
    def load_default_services(cls) -> Dict[str, SAPServiceConfig]:
        """Load default SAP service configurations"""
        return {
            "Z_SALES_ORDER_GENAI_SRV": SAPServiceConfig(
                name="Z_SALES_ORDER_GENAI_SRV",
                path="/sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV",
                version="v2",
                entities=["zsd004Set"],
                custom_headers={}
            )
        }
    
    def get_service_config(self, service_name: str) -> Optional[SAPServiceConfig]:
        """Get configuration for a specific service"""
        return self.services.get(service_name)
    
    def validate_required_env_vars(self) -> None:
        """Validate that all required environment variables are set"""
        required_vars = [
            "SAP_HOST",
            "SAP_USERNAME", 
            "SAP_PASSWORD"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")


# Global configuration instance
config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance"""
    global config
    if config is None:
        config = AppConfig.load_from_env()
        config.services = AppConfig.load_default_services()
        config.validate_required_env_vars()
    return config


def reload_config() -> AppConfig:
    """Reload configuration from environment"""
    global config
    config = None
    return get_config()