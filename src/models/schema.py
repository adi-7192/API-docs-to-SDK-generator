"""Schema model for request/response structures."""

from typing import Any, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class SchemaType(str, Enum):
    """Supported schema types."""
    OBJECT = "object"
    ARRAY = "array"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"


class Schema(BaseModel):
    """Model representing a JSON schema for request/response bodies."""
    
    type: SchemaType = Field(..., description="Type of the schema")
    properties: Optional[Dict[str, Any]] = Field(
        None, 
        description="Properties for object type schemas"
    )
    items: Optional['Schema'] = Field(
        None, 
        description="Schema for array items (recursive)"
    )
    example: Optional[Any] = Field(
        None, 
        description="Example value for this schema"
    )
    
    @field_validator('properties')
    @classmethod
    def validate_properties(cls, v: Optional[Dict[str, Any]], info) -> Optional[Dict[str, Any]]:
        """Validate that properties is only set for object types."""
        if v is not None and info.data.get('type') != SchemaType.OBJECT:
            raise ValueError("Properties can only be set for object type schemas")
        return v
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v: Optional['Schema'], info) -> Optional['Schema']:
        """Validate that items is only set for array types."""
        if v is not None and info.data.get('type') != SchemaType.ARRAY:
            raise ValueError("Items can only be set for array type schemas")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "count": {"type": "number"}
                    },
                    "example": {"id": "123", "name": "Test", "count": 42}
                }
            ]
        }
    }


# Enable forward references for recursive Schema
Schema.model_rebuild()
