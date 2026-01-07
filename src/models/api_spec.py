"""API Specification model."""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field, field_validator, HttpUrl

from .endpoint import Endpoint


class AuthType(str, Enum):
    """Supported authentication types."""
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BEARER = "bearer"
    BASIC = "basic"
    NONE = "none"


class APISpecification(BaseModel):
    """Model representing a complete API specification."""
    
    api_name: str = Field(..., description="Name of the API", min_length=1)
    base_url: HttpUrl = Field(..., description="Base URL for the API")
    auth_type: AuthType = Field(..., description="Authentication type")
    global_headers: Dict[str, str] = Field(
        default_factory=dict, 
        description="Global headers to include in all requests"
    )
    endpoints: List[Endpoint] = Field(
        ..., 
        min_length=1, 
        description="List of API endpoints"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata"
    )
    
    @field_validator('endpoints')
    @classmethod
    def validate_unique_endpoints(cls, v: List[Endpoint]) -> List[Endpoint]:
        """Validate that endpoint paths and methods are unique."""
        seen = set()
        for endpoint in v:
            key = (endpoint.path, endpoint.method.value)
            if key in seen:
                raise ValueError(
                    f"Duplicate endpoint: {endpoint.method.value} {endpoint.path}"
                )
            seen.add(key)
        return v
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v: HttpUrl) -> HttpUrl:
        """Validate base URL format."""
        url_str = str(v)
        if url_str.endswith('/'):
            # Remove trailing slash for consistency
            return HttpUrl(url_str.rstrip('/'))
        return v
    
    def get_endpoint_count(self) -> int:
        """Get the total number of endpoints."""
        return len(self.endpoints)
    
    def get_endpoints_by_method(self, method: str) -> List[Endpoint]:
        """Get all endpoints for a specific HTTP method."""
        return [e for e in self.endpoints if e.method.value == method.upper()]
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "api_name": "Example API",
                    "base_url": "https://api.example.com/v1",
                    "auth_type": "bearer",
                    "global_headers": {
                        "Content-Type": "application/json"
                    },
                    "endpoints": [
                        {
                            "path": "/users",
                            "method": "GET",
                            "description": "List all users in the system",
                            "response_schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "name": {"type": "string"}
                                    }
                                }
                            }
                        }
                    ],
                    "metadata": {
                        "version": "1.0.0",
                        "description": "Example API for demonstration"
                    }
                }
            ]
        }
    }
