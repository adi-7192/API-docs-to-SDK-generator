"""Prompt templates for LLM-based API extraction and code generation."""

# System prompt for API specification extraction
EXTRACTION_SYSTEM_PROMPT = """You are an expert API documentation parser. Your task is to extract structured information from unstructured API documentation and return it in a specific JSON format.

You must be thorough and accurate. If information is unclear or missing, mark it as "unclear" rather than guessing.

The documentation may come from multiple sources or files. Your job is to:
- Combine all endpoints from all documents into a single comprehensive API specification
- Use the most complete information available when there are duplicates
- Maintain consistency in naming and structure across all endpoints

⚠️ CRITICAL: Extract ALL endpoints mentioned in the documentation. Do not skip or summarize.

For EACH endpoint, extract:
- HTTP method (GET, POST, PUT, DELETE, PATCH)
- Path (must start with /)
- Description (detailed explanation of what the endpoint does)
- Parameters (name, type, required, location)
- Request body schema (for POST/PUT/PATCH)
- Response schema (example structure)
- Authentication requirements
- Rate limiting information (if mentioned)

Be especially careful to:
1. Scan the ENTIRE documentation for ALL endpoints - do not stop early
2. If multiple documents are provided, extract endpoints from EVERY document
3. Identify the correct base URL (use the most specific one if multiple are mentioned)
4. Determine the authentication method used
5. Extract parameter types accurately (string, number, boolean, array, object)
6. Note parameter locations (query, path, header, body)
7. Provide example values where possible
8. Merge information from multiple documents when they describe the same API
9. Before finalizing, count the endpoints you found and verify you didn't miss any"""

# User prompt template for extraction
EXTRACTION_USER_PROMPT_TEMPLATE = """Parse the following API documentation and extract structured information.

⚠️ CRITICAL INSTRUCTIONS:
1. Read through the ENTIRE documentation carefully
2. Extract EVERY SINGLE endpoint you find - do not skip any
3. If multiple documents are provided (separated by === markers), extract endpoints from ALL of them
4. Count the total number of endpoints as you go
5. Before returning your response, verify you've included all endpoints

Return a JSON object with this exact structure:
{{
  "api_name": "string (name of the API)",
  "base_url": "string (base URL, e.g., https://api.example.com/v1 - REQUIRED, must be a valid URL)",
  "auth_type": "string (one of: api_key, oauth2, bearer, basic, none)",
  "global_headers": {{
    "header_name": "header_value"
  }},
  "endpoints": [
    {{
      "path": "string (must start with /, e.g., /users/{{id}})",
      "method": "string (GET, POST, PUT, DELETE, or PATCH)",
      "description": "string (detailed description, minimum 10 characters)",
      "parameters": [
        {{
          "name": "string",
          "type": "string (string, number, boolean, array, or object)",
          "required": boolean,
          "location": "string (query, path, header, or body)",
          "description": "string (optional)",
          "example": "any (optional)"
        }}
      ],
      "request_body": {{
        "type": "string (object, array, string, number, or boolean)",
        "properties": {{}},
        "example": {{}}
      }},
      "response_schema": {{
        "type": "string (object, array, string, number, or boolean)",
        "properties": {{}},
        "example": {{}}
      }},
      "auth_required": boolean,
      "rate_limit": "string (optional, e.g., '100 requests per minute')"
    }}
  ],
  "metadata": {{
    "version": "string (optional)",
    "description": "string (optional)",
    "total_endpoints_found": "number (total count of endpoints extracted)"
  }}
}}

Documentation to parse:

{documentation}

IMPORTANT RULES:
- base_url is REQUIRED and must be a valid URL (e.g., https://api.example.com/v1)
- If the base URL is not explicitly stated, infer it from the examples or use a placeholder like https://api.example.com
- NEVER use "unclear" for base_url - always provide a valid URL
- For request_body and response_schema, the "type" field must be one of: object, array, string, number, boolean
- If a request body or response is not documented, omit the request_body or response_schema field entirely (don't use "unclear")
- Only include "properties" field when type is "object"
- ⚠️ Extract ALL endpoints mentioned - this is critical for completeness
- Provide detailed descriptions (minimum 10 characters)
- Include example values where possible
- Be accurate with parameter types and locations
- Add total_endpoints_found to metadata so we can verify completeness"""

# Prompt for generating endpoint methods
ENDPOINT_METHOD_PROMPT_TEMPLATE = """Generate a TypeScript method for the following API endpoint.

API Information:
- Base URL: {base_url}
- Authentication: {auth_type}

Endpoint Details:
- Path: {path}
- Method: {method}
- Description: {description}
- Parameters: {parameters}
- Request Body: {request_body}
- Response Schema: {response_schema}

Generate a complete TypeScript async method that:
1. Has a descriptive name based on the endpoint (e.g., getUser, createPayment)
2. Accepts typed parameters
3. Validates required parameters
4. Builds the correct URL with path parameters
5. Calls this.request() with the appropriate configuration
6. Returns a typed Promise with the response

Use this pattern:

```typescript
/**
 * {description}
 */
async methodName(params: ParamsType): Promise<ResponseType> {{
  // Validate required parameters
  if (!requiredParam) {{
    throw new ValidationError('Required parameter missing');
  }}
  
  // Build URL
  const url = `${{this.baseURL}}{path}`;
  
  // Make request
  const response = await this.request<ResponseType>({{
    method: '{method}',
    url,
    params: queryParams,
    data: requestBody,
  }});
  
  return response;
}}
```

Only return the method code, no explanations."""

# Prompt for generating type definitions
TYPE_DEFINITIONS_PROMPT_TEMPLATE = """Generate TypeScript type definitions for the following API endpoints.

Endpoints:
{endpoints_json}

Generate:
1. Interface for each unique request parameter set
2. Interface for each unique response body
3. Use descriptive names (e.g., GetUserParams, UserResponse)
4. Include JSDoc comments
5. Use proper TypeScript types (string, number, boolean, etc.)
6. Mark optional fields with ?

Example format:

```typescript
/**
 * Parameters for getting a user
 */
export interface GetUserParams {{
  id: string;
  include?: string[];
}}

/**
 * User response object
 */
export interface UserResponse {{
  id: string;
  name: string;
  email: string;
  created_at: string;
}}
```

Only return the type definitions, no explanations."""

# Prompt for generating README sections
README_PROMPT_TEMPLATE = """Generate usage examples and documentation for the following API SDK.

API Name: {api_name}
Base URL: {base_url}
Authentication: {auth_type}
Endpoints: {endpoints_summary}

Generate markdown documentation including:

1. **Quick Start** - Basic initialization example
2. **Authentication** - How to provide API credentials
3. **Usage Examples** - One example per endpoint showing:
   - How to call the method
   - What parameters to provide
   - What response to expect
4. **Error Handling** - How to catch and handle errors

Use this format:

## Quick Start

```typescript
import {{ {api_name_class} }} from './{package_name}';

const client = new {api_name_class}({{
  apiKey: 'your-api-key',
  baseURL: '{base_url}'
}});
```

## Authentication

[Explain how to authenticate]

## Usage Examples

### [Endpoint Name]

```typescript
// Example code
```

Only return the markdown documentation, no meta-commentary."""

# Few-shot examples for better extraction
FEW_SHOT_EXAMPLES = [
    {
        "documentation": """
        # Users API
        
        Base URL: https://api.example.com/v1
        
        ## Authentication
        Use Bearer token in Authorization header.
        
        ## Endpoints
        
        ### GET /users/{id}
        Retrieve a user by ID.
        
        Parameters:
        - id (path, required): User ID
        - include (query, optional): Related resources to include
        
        Response:
        ```json
        {
          "id": "123",
          "name": "John Doe",
          "email": "john@example.com"
        }
        ```
        """,
        "expected_output": {
            "api_name": "Users API",
            "base_url": "https://api.example.com/v1",
            "auth_type": "bearer",
            "endpoints": [
                {
                    "path": "/users/{id}",
                    "method": "GET",
                    "description": "Retrieve a user by their unique identifier",
                    "parameters": [
                        {
                            "name": "id",
                            "type": "string",
                            "required": True,
                            "location": "path"
                        },
                        {
                            "name": "include",
                            "type": "string",
                            "required": False,
                            "location": "query"
                        }
                    ],
                    "response_schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            ]
        }
    }
]

# Documentation analysis prompt
DOCUMENTATION_ANALYSIS_PROMPT = """You are an API documentation analyzer. Your job is to help users understand what they provided and guide them to complete API specifications.

Analyze this documentation and provide a structured report:

{documentation}

Return a JSON object with this exact structure:
{{
  "document_type": "api_reference" | "guide" | "setup_instructions" | "mixed",
  "endpoints_found": {{
    "count": <number>,
    "list": [
      {{"method": "POST", "path": "/auth/token", "description": "Request access token"}}
    ]
  }},
  "is_complete_api": true/false,
  "api_name": "<detected API name or null>",
  "base_url": "<detected base URL or null>",
  "navigation_detected": {{
    "has_more_endpoints": true/false,
    "other_sections": ["Payments", "Workflows", "Transfers"],
    "reference_urls": [
      "https://docs.example.com/reference/payments",
      "https://docs.example.com/reference/workflows"
    ]
  }},
  "user_message": "<clear explanation of findings>",
  "recommendations": [
    "<actionable suggestions for user>"
  ]
}}

Analysis Guidelines:

1. **Document Type Classification**:
   - "api_reference": Contains HTTP methods (GET, POST), endpoint paths (/resource/id), request/response examples
   - "guide": Explains concepts, best practices, tutorials - no actual endpoints
   - "setup_instructions": Configuration, authentication setup, installation - no endpoints
   - "mixed": Contains both guides and API references

2. **Endpoint Detection**:
   - Count ALL unique endpoints (method + path combinations)
   - List each endpoint with method, path, and brief description
   - An endpoint must have: HTTP method + path + some documentation

3. **Completeness Assessment**:
   - Set is_complete_api: false if:
     * Only 1-3 endpoints found but navigation shows more sections
     * Documentation mentions "see also" or "other endpoints"
     * Clear signs this is a subset (e.g., only auth endpoints)
   - Set is_complete_api: true if:
     * 5+ endpoints covering multiple resource types
     * No navigation to additional endpoint pages
     * Appears to be comprehensive documentation

4. **Navigation Detection**:
   - Look for sidebar menus, navigation links, "See also" sections
   - Extract section names (e.g., "Payments API", "Users API")
   - Extract URLs to other API reference pages
   - Estimate if more endpoints exist based on navigation structure

5. **User Message**:
   - Write a clear, conversational explanation
   - Example: "Found 1 API endpoint (POST /auth/token) from your documentation. However, this appears to be just the authentication page. The site navigation shows 15+ other endpoint sections including Payments, Workflows, and Transfers that weren't included."

6. **Recommendations**:
   - Provide specific, actionable suggestions
   - Include exact URLs when possible
   - Explain what each URL contains
   - Example recommendations:
     * "To extract the complete API, provide the main API reference URL: https://docs.example.com/reference"
     * "Or provide specific endpoint pages you need: /reference/payments, /reference/workflows"
     * "The pages you provided (api-credentials, mtls-configuration) are setup guides with no endpoints"

7. **Special Cases**:
   - If 0 endpoints found: Clearly state it's a guide/setup page, suggest reference URLs
   - If multiple documents provided (=== separators): Analyze each section separately
   - If navigation is unclear: Set has_more_endpoints: false, don't guess

Be helpful, specific, and actionable. Your goal is to help users get complete API specifications."""

