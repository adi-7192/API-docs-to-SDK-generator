"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from ..models.api_spec import APISpecification
from ..models.endpoint import Endpoint


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str, config: Dict = None):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: API key for the LLM service
            config: Optional configuration dictionary
        """
        self.api_key = api_key
        self.config = config or {}
    
    @abstractmethod
    def validate_api_key(self) -> Tuple[bool, str]:
        """
        Validate the API key.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def extract_api_specification(
        self, 
        documentation: str
    ) -> Tuple[bool, APISpecification | None, str]:
        """
        Extract API specification from documentation.
        
        Args:
            documentation: Raw documentation text
            
        Returns:
            Tuple of (success, api_spec_or_none, error_message)
        """
        pass
    
    @abstractmethod
    def generate_endpoint_method(
        self,
        endpoint: Endpoint,
        api_spec: APISpecification
    ) -> Tuple[bool, str, str]:
        """
        Generate TypeScript method code for an endpoint.
        
        Args:
            endpoint: Endpoint to generate method for
            api_spec: Full API specification for context
            
        Returns:
            Tuple of (success, method_code, error_message)
        """
        pass
    
    @abstractmethod
    def generate_type_definitions(
        self,
        api_spec: APISpecification
    ) -> Tuple[bool, str, str]:
        """
        Generate TypeScript type definitions for all endpoints.
        
        Args:
            api_spec: API specification
            
        Returns:
            Tuple of (success, type_definitions, error_message)
        """
        pass
    
    @abstractmethod
    def generate_readme_section(
        self,
        api_spec: APISpecification,
        package_name: str
    ) -> Tuple[bool, str, str]:
        """
        Generate README documentation sections.
        
        Args:
            api_spec: API specification
            package_name: NPM package name
            
        Returns:
            Tuple of (success, readme_content, error_message)
        """
        pass
    
    @abstractmethod
    def estimate_cost(
        self,
        text: str
    ) -> float:
        """
        Estimate cost for processing the given text.
        
        Args:
            text: Text to estimate cost for
            
        Returns:
            Estimated cost in USD
        """
        pass
    
    def get_provider_name(self) -> str:
        """Get the name of this provider."""
        return self.__class__.__name__.replace('Provider', '')
