"""OpenAI provider implementation."""

import json
import openai
from typing import Dict, List, Tuple, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from .base_provider import BaseLLMProvider
from .prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT_TEMPLATE,
    ENDPOINT_METHOD_PROMPT_TEMPLATE,
    TYPE_DEFINITIONS_PROMPT_TEMPLATE,
    README_PROMPT_TEMPLATE,
    DOCUMENTATION_ANALYSIS_PROMPT,
)
from ..models.api_spec import APISpecification
from ..models.endpoint import Endpoint
from ..models.documentation_analysis import DocumentationAnalysis


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT-4 provider implementation."""
    
    def __init__(self, api_key: str, config: Dict = None):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
            config: Configuration dictionary with optional keys:
                - model: Model name (default: gpt-4-turbo)
                - temperature: Temperature setting (default: 0.2)
                - max_tokens: Maximum tokens (default: 4000)
                - timeout: Request timeout in seconds (default: 120)
        """
        super().__init__(api_key, config)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = self.config.get('model', 'gpt-4-turbo')
        self.temperature = self.config.get('temperature', 0.2)
        self.max_tokens = self.config.get('max_tokens', 16000)  # Increased from 4000 to handle large API specs
        self.timeout = self.config.get('timeout', 120)
    
    def validate_api_key(self) -> Tuple[bool, str]:
        """
        Validate the OpenAI API key by making a test request.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Make a minimal test request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True, "API key is valid"
        except openai.AuthenticationError:
            return False, "Invalid API key. Please check your OpenAI API key."
        except openai.RateLimitError:
            return False, "Rate limit exceeded. Please try again later."
        except Exception as e:
            return False, f"Error validating API key: {str(e)}"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((
            openai.APITimeoutError,
            openai.RateLimitError,
            openai.APIConnectionError,
        ))
    )
    def _make_request(
        self,
        messages: List[Dict[str, str]],
        response_format: Dict = None
    ) -> str:
        """
        Make a request to OpenAI API with retry logic.
        
        Args:
            messages: List of message dictionaries
            response_format: Optional response format specification
            
        Returns:
            Response content
            
        Raises:
            Various OpenAI exceptions
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    
    def extract_api_specification(
        self,
        documentation: str
    ) -> Tuple[bool, APISpecification | None, str]:
        """
        Extract API specification from documentation using GPT-4.
        
        Args:
            documentation: Raw documentation text
            
        Returns:
            Tuple of (success, api_spec_or_none, error_message)
        """
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": EXTRACTION_USER_PROMPT_TEMPLATE.format(
                        documentation=documentation
                    )
                }
            ]
            
            # Request JSON response
            response_content = self._make_request(
                messages,
                response_format={"type": "json_object"}
            )
            
            # Parse JSON response
            extracted_data = json.loads(response_content)
            
            # Validate and create APISpecification
            try:
                api_spec = APISpecification(**extracted_data)
                return True, api_spec, "Successfully extracted API specification"
            except Exception as validation_error:
                return False, None, f"Validation error: {str(validation_error)}"
            
        except openai.AuthenticationError:
            return False, None, "Authentication failed. Please check your API key."
        except openai.RateLimitError:
            return False, None, "Rate limit exceeded. Please wait and try again."
        except openai.APITimeoutError:
            return False, None, "Request timed out. Try with smaller documentation or increase timeout."
        except json.JSONDecodeError as e:
            return False, None, f"Failed to parse LLM response as JSON: {str(e)}"
        except Exception as e:
            return False, None, f"Unexpected error during extraction: {str(e)}"
    
    def analyze_documentation(
        self,
        documentation: str
    ) -> Tuple[bool, Optional[DocumentationAnalysis], str]:
        """
        Analyze documentation structure using GPT-4o-mini (cheaper, faster).
        
        Args:
            documentation: Raw documentation text
            
        Returns:
            Tuple of (success, analysis_or_none, error_message)
        """
        try:
            # Limit input to first 10K characters for cost efficiency
            doc_sample = documentation[:10000]
            
            # Prepare prompt
            prompt = DOCUMENTATION_ANALYSIS_PROMPT.format(documentation=doc_sample)
            
            # Use gpt-4o-mini for cost efficiency (~10x cheaper than gpt-4-turbo)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an API documentation analyzer."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000,  # Smaller response needed for analysis
                timeout=30  # Faster timeout for analysis
            )
            
            # Parse JSON response
            analysis_data = json.loads(response.choices[0].message.content)
            
            # Create DocumentationAnalysis object
            analysis = DocumentationAnalysis(**analysis_data)
            
            return True, analysis, ""
            
        except openai.AuthenticationError:
            return False, None, "Authentication failed. Please check your API key."
        except openai.RateLimitError:
            return False, None, "Rate limit exceeded. Please wait and try again."
        except openai.APITimeoutError:
            return False, None, "Analysis timed out. Please try again."
        except json.JSONDecodeError as e:
            return False, None, f"Failed to parse analysis response: {str(e)}"
        except Exception as e:
            return False, None, f"Analysis failed: {str(e)}"

    
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
        try:
            # Prepare endpoint details
            parameters_str = json.dumps([
                {
                    "name": p.name,
                    "type": p.type.value,
                    "required": p.required,
                    "location": p.location.value,
                    "description": p.description
                }
                for p in endpoint.parameters
            ], indent=2)
            
            request_body_str = (
                json.dumps(endpoint.request_body.model_dump(), indent=2)
                if endpoint.request_body
                else "null"
            )
            
            response_schema_str = json.dumps(
                endpoint.response_schema.model_dump(),
                indent=2
            )
            
            # Create prompt
            prompt = ENDPOINT_METHOD_PROMPT_TEMPLATE.format(
                base_url=str(api_spec.base_url),
                auth_type=api_spec.auth_type.value,
                path=endpoint.path,
                method=endpoint.method.value,
                description=endpoint.description,
                parameters=parameters_str,
                request_body=request_body_str,
                response_schema=response_schema_str
            )
            
            messages = [
                {"role": "system", "content": "You are an expert TypeScript developer."},
                {"role": "user", "content": prompt}
            ]
            
            method_code = self._make_request(messages)
            
            # Extract code from markdown if present
            if "```typescript" in method_code:
                method_code = method_code.split("```typescript")[1].split("```")[0].strip()
            elif "```" in method_code:
                method_code = method_code.split("```")[1].split("```")[0].strip()
            
            return True, method_code, "Successfully generated endpoint method"
            
        except Exception as e:
            return False, "", f"Error generating endpoint method: {str(e)}"
    
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
        try:
            # Serialize endpoints for prompt
            endpoints_json = json.dumps(
                [
                    {
                        "path": e.path,
                        "method": e.method.value,
                        "parameters": [p.model_dump() for p in e.parameters],
                        "response_schema": e.response_schema.model_dump()
                    }
                    for e in api_spec.endpoints
                ],
                indent=2
            )
            
            prompt = TYPE_DEFINITIONS_PROMPT_TEMPLATE.format(
                endpoints_json=endpoints_json
            )
            
            messages = [
                {"role": "system", "content": "You are an expert TypeScript developer."},
                {"role": "user", "content": prompt}
            ]
            
            type_defs = self._make_request(messages)
            
            # Extract code from markdown if present
            if "```typescript" in type_defs:
                type_defs = type_defs.split("```typescript")[1].split("```")[0].strip()
            elif "```" in type_defs:
                type_defs = type_defs.split("```")[1].split("```")[0].strip()
            
            return True, type_defs, "Successfully generated type definitions"
            
        except Exception as e:
            return False, "", f"Error generating type definitions: {str(e)}"
    
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
        try:
            # Create endpoints summary
            endpoints_summary = "\n".join([
                f"- {e.method.value} {e.path}: {e.description}"
                for e in api_spec.endpoints
            ])
            
            # Convert API name to class name (e.g., "My API" -> "MyAPI")
            api_name_class = api_spec.api_name.replace(" ", "").replace("-", "")
            
            prompt = README_PROMPT_TEMPLATE.format(
                api_name=api_spec.api_name,
                base_url=str(api_spec.base_url),
                auth_type=api_spec.auth_type.value,
                endpoints_summary=endpoints_summary,
                api_name_class=api_name_class,
                package_name=package_name
            )
            
            messages = [
                {"role": "system", "content": "You are a technical documentation writer."},
                {"role": "user", "content": prompt}
            ]
            
            readme_content = self._make_request(messages)
            
            return True, readme_content, "Successfully generated README content"
            
        except Exception as e:
            return False, "", f"Error generating README: {str(e)}"
    
    def estimate_cost(self, text: str) -> float:
        """
        Estimate cost for processing the given text.
        
        Args:
            text: Text to estimate cost for
            
        Returns:
            Estimated cost in USD
        """
        # Rough estimate: 1 token ≈ 4 characters
        estimated_tokens = len(text) // 4
        
        # GPT-4-turbo pricing (as of 2024):
        # Input: $0.01 per 1K tokens
        # Output: $0.03 per 1K tokens
        # Assume output is 50% of input for extraction
        input_cost = (estimated_tokens / 1000) * 0.01
        output_cost = (estimated_tokens * 0.5 / 1000) * 0.03
        
        total_cost = input_cost + output_cost
        return round(total_cost, 4)
