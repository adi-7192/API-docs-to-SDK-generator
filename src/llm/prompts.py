"""Prompt templates for LLM-based API extraction and code generation."""

# System prompt for API specification extraction
EXTRACTION_SYSTEM_PROMPT = """You are an expert API documentation parser. Your task is to extract structured information from unstructured API documentation and return it in a specific JSON format.

You must be thorough and accurate. If information is unclear or missing, mark it as "unclear" rather than guessing.

Extract ALL endpoints mentioned in the documentation, along with their:
- HTTP method (GET, POST, PUT, DELETE, PATCH)
- Path (must start with /)
- Description (detailed explanation of what the endpoint does)
- Parameters (name, type, required, location)
- Request body schema (for POST/PUT/PATCH)
- Response schema (example structure)
- Authentication requirements
- Rate limiting information (if mentioned)

Be especially careful to:
1. Identify the correct base URL
2. Determine the authentication method used
3. Extract parameter types accurately (string, number, boolean, array, object)
4. Note parameter locations (query, path, header, body)
5. Provide example values where possible"""

# User prompt template for extraction
EXTRACTION_USER_PROMPT_TEMPLATE = """Parse the following API documentation and extract structured information.

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
    "description": "string (optional)"
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
- Extract ALL endpoints mentioned
- Provide detailed descriptions (minimum 10 characters)
- Include example values where possible
- Be accurate with parameter types and locations"""

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
