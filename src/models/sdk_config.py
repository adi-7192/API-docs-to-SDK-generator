"""SDK Configuration model."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class License(str, Enum):
    """Supported license types."""
    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    ISC = "ISC"
    BSD_3_CLAUSE = "BSD-3-Clause"


class RetryConfig(BaseModel):
    """Configuration for retry logic."""
    
    max_retries: int = Field(default=3, ge=1, le=10, description="Maximum number of retries")
    base_delay: float = Field(default=1.0, ge=0.5, le=5.0, description="Base delay in seconds")
    max_delay: float = Field(default=30.0, ge=5.0, le=60.0, description="Maximum delay in seconds")
    retryable_status_codes: List[int] = Field(
        default=[408, 429, 500, 502, 503, 504],
        description="HTTP status codes to retry on"
    )


class RateLimitConfig(BaseModel):
    """Configuration for rate limiting."""
    
    requests_per_second: int = Field(
        default=10, 
        ge=1, 
        le=100, 
        description="Maximum requests per second"
    )
    burst_allowance: int = Field(
        default=5, 
        ge=1, 
        le=50, 
        description="Burst allowance for token bucket"
    )
    algorithm: str = Field(
        default="token_bucket",
        description="Rate limiting algorithm"
    )


class SDKConfig(BaseModel):
    """Configuration for SDK generation."""
    
    # Metadata
    package_name: str = Field(..., description="NPM package name", min_length=1)
    version: str = Field(default="1.0.0", description="Package version")
    author: Optional[str] = Field(None, description="Package author")
    license: License = Field(default=License.MIT, description="Package license")
    
    # Feature toggles
    enable_retry_logic: bool = Field(default=True, description="Include retry logic")
    enable_rate_limiting: bool = Field(default=True, description="Include rate limiting")
    enable_error_handling: bool = Field(default=True, description="Include error handling")
    
    # Feature configurations
    retry_config: Optional[RetryConfig] = Field(
        default_factory=RetryConfig,
        description="Retry logic configuration"
    )
    rate_limit_config: Optional[RateLimitConfig] = Field(
        default_factory=RateLimitConfig,
        description="Rate limiting configuration"
    )
    
    # Generation settings
    include_examples: bool = Field(default=True, description="Include example.ts file")
    include_tests: bool = Field(default=False, description="Include test files (future)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "package_name": "my-api-sdk",
                    "version": "1.0.0",
                    "author": "John Doe",
                    "license": "MIT",
                    "enable_retry_logic": True,
                    "enable_rate_limiting": True,
                    "enable_error_handling": True,
                    "retry_config": {
                        "max_retries": 3,
                        "base_delay": 1.0,
                        "max_delay": 30.0
                    },
                    "rate_limit_config": {
                        "requests_per_second": 10,
                        "burst_allowance": 5
                    }
                }
            ]
        }
    }
