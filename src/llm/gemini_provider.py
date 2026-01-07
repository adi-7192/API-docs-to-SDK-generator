"""Google Gemini LLM provider implementation."""

import json
from typing import Tuple, Optional, Dict
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from .base_provider import BaseLLMProvider
from ..models.api_spec import APISpecification
from ..models.endpoint import Endpoint
from .prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT_TEMPLATE,
    ENDPOINT_METHOD_PROMPT_TEMPLATE,
    TYPE_DEFINITIONS_PROMPT_TEMPLATE,
)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(self, api_key: str, config: Optional[Dict] = None):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key
            config: Optional configuration (temperature, max_tokens, etc.)
        """
        self.api_key = api_key
        self.config = config or {}
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Pro for best results
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',
            generation_config=genai.GenerationConfig(
                temperature=self.config.get('temperature', 0.2),
                max_output_tokens=self.config.get('max_tokens', 4000),
            )
        )
    
    def validate_api_key(self) -> Tuple[bool, str]:
        """
        Validate the Gemini API key.
        
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Try a simple generation to validate the key
            response = self.model.generate_content("Hello")
            return True, "API key is valid"
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
                return False, "Invalid API key"
            elif "quota" in error_msg.lower():
                return False, "API key valid but quota exceeded"
            else:
                return False, f"Validation error: {error_msg}"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def extract_api_specification(
        self,
        documentation: str
    ) -> Tuple[bool, Optional[APISpecification], Optional[str]]:
        """
        Extract API specification from documentation using Gemini.
        
        Args:
            documentation: Raw API documentation text
            
        Returns:
            Tuple of (success, api_spec, error_message)
        """
        try:
            # Prepare prompt
            prompt = f"""{EXTRACTION_SYSTEM_PROMPT}

{EXTRACTION_USER_PROMPT_TEMPLATE.format(documentation=documentation)}"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            api_data = json.loads(response_text)
            
            # Create APISpecification from JSON
            api_spec = APISpecification(**api_data)
            
            return True, api_spec, None
            
        except json.JSONDecodeError as e:
            return False, None, f"Failed to parse JSON response: {str(e)}"
        except Exception as e:
            return False, None, f"Extraction failed: {str(e)}"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_endpoint_method(
        self,
        endpoint: Endpoint,
        api_spec: APISpecification
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate TypeScript method code for an endpoint using Gemini.
        
        Args:
            endpoint: Endpoint to generate method for
            api_spec: Full API specification for context
            
        Returns:
            Tuple of (success, method_code, error_message)
        """
        try:
            # Prepare prompt using the template
            prompt = ENDPOINT_METHOD_PROMPT_TEMPLATE.format(
                base_url=api_spec.base_url,
                auth_type=api_spec.auth_type.value,
                path=endpoint.path,
                method=endpoint.method.value,
                description=endpoint.description,
                parameters=endpoint.parameters,
                request_body=endpoint.request_body,
                response_schema=endpoint.response_schema
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            method_code = response.text.strip()
            
            # Remove markdown code blocks if present
            if "```typescript" in method_code:
                method_code = method_code.split("```typescript")[1].split("```")[0].strip()
            elif "```" in method_code:
                method_code = method_code.split("```")[1].split("```")[0].strip()
            
            return True, method_code, None
            
        except Exception as e:
            return False, None, f"Method generation failed: {str(e)}"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_type_definitions(
        self,
        api_spec: APISpecification
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate TypeScript type definitions using Gemini.
        
        Args:
            api_spec: API specification
            
        Returns:
            Tuple of (success, types_code, error_message)
        """
        try:
            # Prepare prompt using the template
            prompt = TYPE_DEFINITIONS_PROMPT_TEMPLATE.format(
                endpoints_json=api_spec.model_dump_json(indent=2)
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            types_code = response.text.strip()
            
            # Remove markdown code blocks if present
            if "```typescript" in types_code:
                types_code = types_code.split("```typescript")[1].split("```")[0].strip()
            elif "```" in types_code:
                types_code = types_code.split("```")[1].split("```")[0].strip()
            
            return True, types_code, None
            
        except Exception as e:
            return False, None, f"Type generation failed: {str(e)}"
    
    def generate_readme_section(
        self,
        api_spec: APISpecification,
        section: str
    ) -> str:
        """
        Generate a README section using Gemini.
        
        Args:
            api_spec: API specification
            section: Section to generate (e.g., "usage_examples")
            
        Returns:
            Generated markdown content
        """
        try:
            prompt = f"""Generate a {section} section for a README.md file for this API SDK:

API: {api_spec.api_name}
Base URL: {api_spec.base_url}
Endpoints: {len(api_spec.endpoints)}

Please provide clear, concise markdown content with code examples."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception:
            return f"## {section.replace('_', ' ').title()}\n\nDocumentation coming soon."
    
    def estimate_cost(self, documentation: str) -> float:
        """
        Estimate cost for processing documentation with Gemini.
        
        Args:
            documentation: Documentation text
            
        Returns:
            Estimated cost in USD
        """
        # Gemini 1.5 Pro pricing (as of 2024):
        # Input: $0.00125 per 1K characters (up to 128K)
        # Output: $0.005 per 1K characters
        
        input_chars = len(documentation)
        estimated_output_chars = min(input_chars, 4000)  # Max output tokens
        
        input_cost = (input_chars / 1000) * 0.00125
        output_cost = (estimated_output_chars / 1000) * 0.005
        
        # Multiply by ~3 for extraction + method generation + types
        total_cost = (input_cost + output_cost) * 3
        
        return total_cost
