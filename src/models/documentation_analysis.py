"""Data model for documentation analysis results."""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class EndpointSummary(BaseModel):
    """Summary of a single endpoint found in documentation."""
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")
    path: str = Field(..., description="Endpoint path")
    description: str = Field(..., description="Brief description of endpoint")


class NavigationDetection(BaseModel):
    """Information about additional endpoints detected in navigation."""
    has_more_endpoints: bool = Field(
        default=False,
        description="Whether more endpoints are available on the site"
    )
    other_sections: List[str] = Field(
        default_factory=list,
        description="Names of other API sections found in navigation"
    )
    reference_urls: List[str] = Field(
        default_factory=list,
        description="URLs to other API reference pages"
    )


class DocumentationAnalysis(BaseModel):
    """Analysis results for API documentation."""
    
    document_type: Literal["api_reference", "guide", "setup_instructions", "mixed"] = Field(
        ...,
        description="Type of documentation provided"
    )
    
    endpoints_found: dict = Field(
        ...,
        description="Dictionary with 'count' and 'list' of endpoints"
    )
    
    is_complete_api: bool = Field(
        ...,
        description="Whether this appears to be complete API documentation"
    )
    
    api_name: Optional[str] = Field(
        default=None,
        description="Detected name of the API"
    )
    
    base_url: Optional[str] = Field(
        default=None,
        description="Detected base URL for the API"
    )
    
    navigation_detected: NavigationDetection = Field(
        default_factory=NavigationDetection,
        description="Information about additional endpoints in navigation"
    )
    
    user_message: str = Field(
        ...,
        description="Clear, conversational explanation of findings"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable suggestions for the user"
    )
