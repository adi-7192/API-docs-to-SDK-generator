"""Unit tests for data models."""

import pytest
from src.models import (
    APISpecification,
    Endpoint,
    Parameter,
    Schema,
    SDKConfig,
    HTTPMethod,
    ParameterType,
    ParameterLocation,
    SchemaType,
    AuthType,
    License,
)


def test_schema_creation():
    """Test creating a basic schema."""
    schema = Schema(
        type=SchemaType.OBJECT,
        properties={
            "id": {"type": "string"},
            "name": {"type": "string"}
        },
        example={"id": "123", "name": "Test"}
    )
    
    assert schema.type == SchemaType.OBJECT
    assert "id" in schema.properties
    assert schema.example["id"] == "123"


def test_schema_recursive():
    """Test recursive schema (array of objects)."""
    item_schema = Schema(
        type=SchemaType.OBJECT,
        properties={"id": {"type": "string"}}
    )
    
    array_schema = Schema(
        type=SchemaType.ARRAY,
        items=item_schema
    )
    
    assert array_schema.type == SchemaType.ARRAY
    assert array_schema.items.type == SchemaType.OBJECT


def test_parameter_creation():
    """Test creating a parameter."""
    param = Parameter(
        name="user_id",
        type=ParameterType.STRING,
        required=True,
        location=ParameterLocation.PATH,
        description="User identifier"
    )
    
    assert param.name == "user_id"
    assert param.required is True
    assert param.location == ParameterLocation.PATH


def test_endpoint_creation():
    """Test creating an endpoint."""
    endpoint = Endpoint(
        path="/users/{id}",
        method=HTTPMethod.GET,
        description="Get a user by ID",
        parameters=[
            Parameter(
                name="id",
                type=ParameterType.STRING,
                required=True,
                location=ParameterLocation.PATH
            )
        ],
        response_schema=Schema(
            type=SchemaType.OBJECT,
            properties={"id": {"type": "string"}}
        )
    )
    
    assert endpoint.path == "/users/{id}"
    assert endpoint.method == HTTPMethod.GET
    assert len(endpoint.parameters) == 1


def test_endpoint_path_validation():
    """Test that endpoint path must start with /."""
    with pytest.raises(ValueError, match="must start with /"):
        Endpoint(
            path="users",  # Missing leading slash
            method=HTTPMethod.GET,
            description="Get users",
            response_schema=Schema(type=SchemaType.OBJECT)
        )


def test_endpoint_path_parameter_matching():
    """Test that path parameters must match declared parameters."""
    with pytest.raises(ValueError, match="not declared in parameters"):
        Endpoint(
            path="/users/{id}",
            method=HTTPMethod.GET,
            description="Get user",
            parameters=[],  # Missing id parameter
            response_schema=Schema(type=SchemaType.OBJECT)
        )


def test_api_specification_creation():
    """Test creating an API specification."""
    api_spec = APISpecification(
        api_name="Test API",
        base_url="https://api.example.com/v1",
        auth_type=AuthType.BEARER,
        endpoints=[
            Endpoint(
                path="/users",
                method=HTTPMethod.GET,
                description="List all users",
                response_schema=Schema(type=SchemaType.ARRAY)
            )
        ]
    )
    
    assert api_spec.api_name == "Test API"
    assert str(api_spec.base_url) == "https://api.example.com/v1"
    assert len(api_spec.endpoints) == 1


def test_api_specification_unique_endpoints():
    """Test that duplicate endpoints are not allowed."""
    with pytest.raises(ValueError, match="Duplicate endpoint"):
        APISpecification(
            api_name="Test API",
            base_url="https://api.example.com/v1",
            auth_type=AuthType.BEARER,
            endpoints=[
                Endpoint(
                    path="/users",
                    method=HTTPMethod.GET,
                    description="Get all users from the system",
                    response_schema=Schema(type=SchemaType.ARRAY)
                ),
                Endpoint(
                    path="/users",
                    method=HTTPMethod.GET,  # Duplicate!
                    description="Get all users from the system again",
                    response_schema=Schema(type=SchemaType.ARRAY)
                )
            ]
        )


def test_sdk_config_creation():
    """Test creating SDK configuration."""
    sdk_config = SDKConfig(
        package_name="my-api-sdk",
        version="1.0.0",
        author="Test Author",
        license=License.MIT,
        enable_retry_logic=True,
        enable_rate_limiting=True
    )
    
    assert sdk_config.package_name == "my-api-sdk"
    assert sdk_config.version == "1.0.0"
    assert sdk_config.enable_retry_logic is True
    assert sdk_config.license == License.MIT


def test_sdk_config_with_retry_config():
    """Test SDK config with retry configuration."""
    from src.models.sdk_config import RetryConfig
    
    retry_config = RetryConfig(
        max_retries=5,
        base_delay=2.0,
        max_delay=60.0
    )
    
    sdk_config = SDKConfig(
        package_name="test-sdk",
        enable_retry_logic=True,
        retry_config=retry_config
    )
    
    assert sdk_config.retry_config.max_retries == 5
    assert sdk_config.retry_config.base_delay == 2.0
