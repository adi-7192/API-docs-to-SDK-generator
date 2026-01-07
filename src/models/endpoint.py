"""Endpoint model for API endpoints."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import re

from .parameter import Parameter
from .schema import Schema


class HTTPMethod(str, Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Endpoint(BaseModel):
    """Model representing an API endpoint."""
    
    path: str = Field(..., description="Endpoint path (must start with /)", min_length=1)
    method: HTTPMethod = Field(..., description="HTTP method")
    description: str = Field(..., description="Endpoint description", min_length=10)
    parameters: List[Parameter] = Field(default_factory=list, description="Endpoint parameters")
    request_body: Optional[Schema] = Field(None, description="Request body schema")
    response_schema: Schema = Field(..., description="Response schema")
    auth_required: bool = Field(default=True, description="Whether authentication is required")
    rate_limit: Optional[str] = Field(None, description="Rate limit information")
    confidence_score: float = Field(
        default=1.0, 
        ge=0.0, 
        le=1.0, 
        description="Confidence score for extracted data"
    )
    
    @field_validator('path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate that path starts with /."""
        if not v.startswith('/'):
            raise ValueError("Endpoint path must start with /")
        return v
    
    @field_validator('parameters')
    @classmethod
    def validate_path_parameters(cls, v: List[Parameter], info) -> List[Parameter]:
        """Validate that path parameters match the path string."""
        path = info.data.get('path', '')
        
        # Extract path parameters from the path (e.g., {id}, {user_id})
        path_param_names = set(re.findall(r'\{(\w+)\}', path))
        
        # Get path parameters from the parameters list
        declared_path_params = {
            p.name for p in v if p.location.value == 'path'
        }
        
        # Check for missing path parameters
        missing = path_param_names - declared_path_params
        if missing:
            raise ValueError(
                f"Path parameters {missing} are in the path but not declared in parameters"
            )
        
        # Check for extra path parameters
        extra = declared_path_params - path_param_names
        if extra:
            raise ValueError(
                f"Path parameters {extra} are declared but not in the path"
            )
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "path": "/users/{user_id}",
                    "method": "GET",
                    "description": "Retrieve a user by their unique identifier",
                    "parameters": [
                        {
                            "name": "user_id",
                            "type": "string",
                            "required": True,
                            "location": "path"
                        }
                    ],
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    },
                    "auth_required": True,
                    "confidence_score": 0.95
                }
            ]
        }
    }
