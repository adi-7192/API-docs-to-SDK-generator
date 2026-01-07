"""Confidence scoring for extracted API specifications."""

from typing import List
from ..models.api_spec import APISpecification
from ..models.endpoint import Endpoint


def calculate_endpoint_confidence(endpoint: Endpoint) -> float:
    """
    Calculate confidence score for a single endpoint.
    
    Args:
        endpoint: The endpoint to score
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    score = 1.0
    
    # Deduct for missing or unclear fields
    if not endpoint.description or len(endpoint.description) < 20:
        score -= 0.1
    
    if "unclear" in endpoint.description.lower() or "todo" in endpoint.description.lower():
        score -= 0.2
    
    # Deduct for missing parameters
    if not endpoint.parameters:
        score -= 0.15
    
    # Deduct for parameters without types or descriptions
    for param in endpoint.parameters:
        if not param.description:
            score -= 0.05
        if not param.example and not param.default_value:
            score -= 0.03
    
    # Deduct for missing response schema details
    if not endpoint.response_schema.example:
        score -= 0.1
    
    # Bonus for having examples
    if endpoint.response_schema.example:
        score += 0.1
    
    # Bonus for rate limit info
    if endpoint.rate_limit:
        score += 0.05
    
    return max(0.0, min(1.0, score))


def calculate_api_confidence(api_spec: APISpecification) -> float:
    """
    Calculate overall confidence score for an API specification.
    
    Args:
        api_spec: The API specification to score
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    score = 1.0
    
    # Deduct for missing critical fields
    if not api_spec.base_url:
        score -= 0.3
    
    if api_spec.auth_type.value == "none":
        # Might be intentional, but flag for review
        score -= 0.1
    
    # Deduct for unclear metadata
    if "unclear" in str(api_spec.metadata).lower():
        score -= 0.2
    
    # Calculate average endpoint confidence
    if api_spec.endpoints:
        endpoint_scores = [
            calculate_endpoint_confidence(endpoint) 
            for endpoint in api_spec.endpoints
        ]
        avg_endpoint_score = sum(endpoint_scores) / len(endpoint_scores)
        
        # Weight the overall score by endpoint quality
        score = (score * 0.3) + (avg_endpoint_score * 0.7)
    else:
        score -= 0.5  # No endpoints is a major issue
    
    # Bonus for having global headers
    if api_spec.global_headers:
        score += 0.05
    
    # Bonus for having metadata
    if api_spec.metadata and len(api_spec.metadata) > 0:
        score += 0.05
    
    return max(0.0, min(1.0, score))


def get_confidence_level(score: float) -> str:
    """
    Get a human-readable confidence level.
    
    Args:
        score: Confidence score between 0.0 and 1.0
        
    Returns:
        Confidence level string
    """
    if score >= 0.9:
        return "✅ Complete"
    elif score >= 0.7:
        return "⚠️ Review Needed"
    else:
        return "❌ Missing Data"


def get_confidence_color(score: float) -> str:
    """
    Get a color code for the confidence level.
    
    Args:
        score: Confidence score between 0.0 and 1.0
        
    Returns:
        Color string (green, yellow, red)
    """
    if score >= 0.9:
        return "green"
    elif score >= 0.7:
        return "yellow"
    else:
        return "red"
