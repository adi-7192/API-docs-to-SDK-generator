"""Parameter model for endpoint parameters."""

from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ParameterType(str, Enum):
    """Supported parameter types."""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


class ParameterLocation(str, Enum):
    """Parameter location in the request."""
    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    BODY = "body"


class Parameter(BaseModel):
    """Model representing an API endpoint parameter."""
    
    name: str = Field(..., description="Parameter name", min_length=1)
    type: ParameterType = Field(..., description="Parameter data type")
    required: bool = Field(default=False, description="Whether the parameter is required")
    location: ParameterLocation = Field(..., description="Where the parameter is located")
    description: Optional[str] = Field(None, description="Parameter description")
    default_value: Optional[Any] = Field(None, description="Default value if not provided")
    example: Optional[Any] = Field(None, description="Example value")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "user_id",
                    "type": "string",
                    "required": True,
                    "location": "path",
                    "description": "Unique identifier for the user",
                    "example": "usr_123abc"
                },
                {
                    "name": "limit",
                    "type": "number",
                    "required": False,
                    "location": "query",
                    "description": "Maximum number of results to return",
                    "default_value": 10,
                    "example": 25
                }
            ]
        }
    }
