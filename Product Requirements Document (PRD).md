<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Product Requirements Document (PRD)

## API SDK Generator

**Version:** 1.0
**Last Updated:** January 7, 2026
**Author:** Product Manager / Technical Lead
**Status:** Ready for Development
**Development Platform:** Google Antigravity AI

***

## Executive Summary

### Overview

API SDK Generator is an AI-powered web application that transforms unstructured API documentation into production-ready TypeScript SDKs. The tool addresses the significant pain point of developers spending 4-6 hours writing boilerplate API client code for every new service integration.

### Vision Statement

Enable developers to generate fully-typed, production-grade API client libraries in under 60 seconds by leveraging LLM technology to parse documentation and hybrid template-based code generation.

### Target Users

- Full-stack developers integrating third-party APIs
- Backend engineers building microservices
- Technical founders prototyping products
- DevOps engineers automating API interactions


### Success Metrics

- SDK generation time: Under 2 minutes for typical API (20 endpoints)
- Extraction accuracy: 70%+ success rate on real-world API documentation
- Code quality: Generated SDKs compile without syntax errors
- Portfolio impact: Demo-ready application with public deployment link
- Interview value: Showcases AI integration, product thinking, and full-stack skills

***

## Problem Statement

### Current Pain Points

1. **Time-consuming boilerplate**: Developers spend 4-6 hours per API writing client code for authentication, request formatting, error handling, retry logic, and type definitions
2. **Repetitive work**: Same patterns (retry logic, rate limiting, error handling) rewritten for each API
3. **Maintenance burden**: API changes require manual SDK updates
4. **Type safety gaps**: Hand-written clients often lack comprehensive TypeScript types
5. **Quality inconsistency**: Different developers implement retry/error handling differently

### Market Gap

Existing solutions focus on structured API specifications (OpenAPI/Swagger), leaving developers with unstructured documentation to manually parse and interpret. No tool combines LLM-powered parsing with production-grade code generation.

***

## Product Goals

### Primary Goals (MVP)

1. **Functional**: Generate working TypeScript SDK from unstructured API documentation
2. **Portfolio**: Create impressive demo for technical interviews
3. **Educational**: Showcase AI integration, product design, and engineering skills
4. **Deployable**: Public Streamlit deployment with shareable link

### Secondary Goals (Post-MVP)

1. Support additional languages (Python, Go)
2. Advanced features (webhooks, streaming, pagination)
3. Integration with development workflows (VS Code extension)
4. Community-driven template library

### Non-Goals (Out of Scope)

- Production-grade SaaS with user authentication
- Database-backed storage of generated SDKs
- Real-time collaboration features
- Monetization or commercial launch
- Enterprise deployment support

***

## User Personas

### Primary Persona: Sarah - Full-Stack Developer

**Background:**

- 3-5 years experience building web applications
- Integrates 2-3 new APIs per project
- Values developer experience and type safety
- Prefers TypeScript for frontend/backend work

**Pain Points:**

- Wastes hours writing API client boilerplate
- API documentation often incomplete or ambiguous
- Copy-pasting code patterns from previous projects
- Maintaining multiple API clients across projects

**Goals:**

- Generate SDK quickly to focus on business logic
- Ensure type safety for API responses
- Have reliable error handling and retry logic built-in
- Easy integration into existing TypeScript projects

**Success Criteria:**

- Can generate SDK in under 5 minutes
- Generated code is readable and follows best practices
- SDK handles common edge cases (network errors, rate limits)


### Secondary Persona: Marcus - Technical Interviewer

**Background:**

- Senior Engineer evaluating candidates
- Looks for problem-solving and technical depth
- Values production-ready thinking over toy projects

**Evaluation Criteria:**

- Does it solve a real problem?
- Is the architecture well-designed?
- How are edge cases handled?
- Can the candidate explain technical decisions?

***

## Product Overview

### Core Functionality

Transform unstructured API documentation → Production-ready TypeScript SDK with retry logic, rate limiting, error handling, and full type safety.

### Key Differentiators

1. **Unstructured doc support**: Parses any documentation format, not just OpenAPI specs
2. **Hybrid generation**: Combines proven templates with LLM customization for reliability
3. **Production features**: Built-in retry logic, rate limiting, comprehensive error handling
4. **Multi-LLM support**: Flexible provider choice (OpenAI, Anthropic, Gemini)
5. **Interactive review**: User validates/edits extracted API structure before generation

### Technology Stack

**Frontend Framework:**

- Streamlit 1.30+ (rapid development, built-in UI components, free deployment)
- streamlit-code-editor (syntax highlighting)
- streamlit-option-menu (multi-step navigation)
- streamlit-extras (enhanced UI components)

**Backend Processing:**

- Python 3.10+ (core logic)
- Pydantic (data validation and modeling)
- Jinja2 (template engine for code generation)

**LLM Integration:**

- openai (GPT-4/GPT-4-turbo support)
- tenacity (retry logic with exponential backoff)
- User provides own API keys (zero hosting costs)

**Document Processing:**

- requests + beautifulsoup4 (HTML parsing)
- pypdf2 (PDF extraction)
- trafilatura (clean text extraction)

**Utilities:**

- zipfile (bundle generated SDK)
- json/yaml (configuration)
- python-dotenv (environment management)

***

## User Journey \& Workflow

### High-Level Flow

```
Input Selection → LLM Configuration → Doc Parsing & Review → SDK Generation → Code Preview & Download
```


### Detailed User Journey

#### Step 1: Input Selection (Entry Point)

**User arrives at:** Landing page with hero section

**Actions available:**

1. **Tab: URL Input**
    - Paste API documentation URL
    - Click "Fetch Documentation"
    - System validates URL accessibility
    - Displays preview of fetched content
2. **Tab: File Upload**
    - Drag-and-drop or browse file
    - Supported formats: PDF, HTML, Markdown, TXT
    - Max file size: 5MB
    - System extracts text content
3. **Tab: Text Paste**
    - Direct paste into text area
    - Minimum 100 characters required
    - Character count indicator
    - Preview formatting
4. **Tab: Example Gallery**
    - Pre-built SDK showcase (Stripe, GitHub, Twilio)
    - Cards display: Logo, API name, description
    - "View Generation Process" button
    - "Download SDK" button

**Validation:**

- URL must be accessible (200 status)
- File must be valid format and under size limit
- Text must meet minimum length
- Clear error messages for failures

**User proceeds to:** Step 2 (LLM Configuration)

***

#### Step 2: LLM Configuration

**User sees:** Configuration panel for AI processing

**Configuration options:**

**Provider Selection:**

- Radio buttons: OpenAI (default) | Anthropic | Google Gemini
- Display pricing info per provider (informational)
- Recommended model pre-selected:
    - OpenAI: gpt-4-turbo
    - Anthropic: claude-3-5-sonnet
    - Gemini: gemini-1.5-pro

**API Key Input:**

- Password field with visibility toggle
- Placeholder: "Enter your OpenAI API key (sk-...)"
- Security note: "Key stored in session only, never saved"
- "Test API Key" button (validates before proceeding)

**Advanced Settings (Collapsible):**

- Temperature slider (0.0 - 1.0, default: 0.2)
- Max tokens (1000 - 8000, default: 4000)
- Timeout seconds (30 - 300, default: 120)

**Cost Estimation:**

- Calculate based on documentation length
- Display: "Estimated cost: \$0.50 from your API key"
- Tip: "Use Gemini for lowest cost"

**Validation:**

- API key format check
- Optional test call to verify key works
- Show error if invalid

**User proceeds to:** Step 3 (Parsing \& Review)

***

#### Step 3: Documentation Parsing \& Review

**Phase A: Parsing (Automated)**

**Loading State:**

- Full-screen spinner with status updates
- Progress indicators:
    - "Analyzing documentation structure..."
    - "Identifying API endpoints..."
    - "Extracting request/response schemas..."
    - "Detecting authentication methods..."
- Real-time token usage counter
- Estimated time remaining

**Background Process:**

- LLM extracts structured API specification
- Uses structured output (JSON mode) for reliability
- Extracts: API name, base URL, auth type, endpoints, parameters, schemas
- Confidence scoring per extracted field
- Error handling: Retry up to 3 times on failure

**Error Scenarios:**

- **LLM Timeout**: Show "Generation timed out. Try with smaller document or different provider."
- **Extraction Failed**: Show "Couldn't extract API structure. Try manual input or upload OpenAPI spec."
- **Partial Success**: Show warning, allow proceeding with incomplete data

***

**Phase B: Review \& Edit (User Validation)**

**Display Format:**

**API Overview Section:**

- API Name (editable text input)
- Base URL (editable text input)
- Authentication Type (dropdown: API Key, OAuth2, Bearer Token, Basic Auth, None)
- Global Headers (key-value pairs, add/remove)

**Endpoints Section:**

- Expandable cards for each endpoint
- Header shows: `[METHOD] /endpoint/path` with confidence badge
    - ✅ Complete (green)
    - ⚠️ Review Needed (yellow)
    - ❌ Missing Data (red)

**Per-Endpoint Fields (All Editable):**

- Path (text input)
- HTTP Method (dropdown: GET, POST, PUT, DELETE, PATCH)
- Description (text area)
- Authentication Required (checkbox)
- Rate Limit (optional text input)

**Parameters Table:**

- Columns: Name, Type, Required, Location (query/path/header/body)
- Add/Remove row buttons
- Inline editing

**Request Body Schema:**

- JSON editor with syntax highlighting
- Optional (only for POST/PUT/PATCH)
- Example value shown

**Response Schema:**

- JSON editor with syntax highlighting
- Default status code: 200
- Add additional status codes (400, 401, 404, 500)

**Action Buttons:**

- "Add Endpoint" - Create new blank endpoint
- "Remove Endpoint" - Delete selected endpoint
- "Regenerate" - Re-run LLM extraction with adjusted settings
- "Continue to Generation" - Proceed to next step

**Validation:**

- Check all required fields populated
- Verify valid JSON in schemas
- Show validation errors in-line
- Block proceeding if critical errors

**User proceeds to:** Step 4 (SDK Generation Configuration)

***

#### Step 4: SDK Generation Configuration

**User sees:** Final configuration before generation

**SDK Metadata:**

- Package Name (auto-filled from API name, editable)
- Version (default: 1.0.0)
- Author (optional)
- License (dropdown: MIT, Apache-2.0, ISC, default: MIT)

**Feature Toggles:**

All enabled by default with checkboxes:

**✅ Retry Logic**

- Description: "Automatic retry with exponential backoff for failed requests"
- Sub-options (shown when checked):
    - Max Retries: Number input (1-10, default: 3)
    - Base Delay: Slider (0.5s - 5s, default: 1s)
    - Max Delay: Slider (5s - 60s, default: 30s)
    - Retry on Status Codes: Multi-select (408, 429, 500, 502, 503, 504)

**✅ Rate Limiting**

- Description: "Built-in rate limiter to respect API quotas"
- Sub-options:
    - Requests per Second: Number input (1-100, default: 10)
    - Burst Allowance: Number input (1-50, default: 5)
    - Algorithm: Dropdown (Token Bucket, Sliding Window)

**✅ Error Handling**

- Description: "Comprehensive typed error classes for all scenarios"
- Auto-generates: APIError, NetworkError, ValidationError, RateLimitError

**⏸️ Pagination Support** (Deferred to post-MVP)

- Description: "Auto-detect and handle paginated responses"
- Grayed out with tooltip: "Coming in next version"

**⏸️ Webhook Utilities** (Deferred to post-MVP)

- Description: "Signature verification and payload parsing for webhooks"
- Grayed out with tooltip: "Coming in next version"

**⏸️ Streaming Support** (Deferred to post-MVP)

- Description: "Handle Server-Sent Events and chunked responses"
- Grayed out with tooltip: "Coming in next version"

**Generation Preview:**

- Estimated file count: "8 files"
- Estimated size: "~50KB"
- Estimated generation time: "30-60 seconds"

**Primary Action Button:**

- Large, prominent: "Generate SDK 🚀"
- Shows confirmation modal on click:
    - Summary: API name, endpoint count, enabled features
    - Cost estimate: "\$0.30 from your API key"
    - "Confirm and Generate" / "Cancel" buttons

**User proceeds to:** Step 5 (Code Preview \& Download)

***

#### Step 5: Code Preview \& Download

**Phase A: Generation (Automated with Progress)**

**Progress Display:**

- Progress bar with percentage (0-100%)
- Step-by-step status updates:

1. "Generating base client class..." (20%)
2. "Creating TypeScript type definitions..." (40%)
3. "Adding retry and rate limiting logic..." (60%)
4. "Generating endpoint methods..." (80%)
5. "Building package files..." (90%)
6. "Finalizing SDK..." (100%)

**Real-time Metrics:**

- Token Usage: "2,450 tokens"
- Actual Cost: "\$0.28"
- Time Elapsed: "42 seconds"

**Error Handling:**

- If generation fails: Show partial results with warning
- "⚠️ Generation incomplete. You can download what we generated or try again."
- Option to retry or proceed with partial SDK

***

**Phase B: Preview \& Download (Success State)**

**File Navigation (Left Sidebar):**

File tree structure (collapsible folders):

```
📁 [api-name]-sdk/
├── 📁 src/
│   ├── 📄 client.ts ⭐ (main client class)
│   ├── 📄 types.ts (TypeScript interfaces)
│   ├── 📄 errors.ts (error classes)
│   ├── 📄 utils/
│   │   ├── 📄 retry.ts
│   │   ├── 📄 rateLimiter.ts
│   │   └── 📄 logger.ts
│   └── 📄 index.ts (main exports)
├── 📄 package.json
├── 📄 tsconfig.json
├── 📄 README.md ⭐
├── 📄 .gitignore
└── 📄 example.ts (usage examples)
```

**File icons:**

- ⭐ = Important files (highlighted)
- File size shown next to name
- Click to display in main panel

**Code Display (Main Panel):**

**Tab-based viewer:**

- One file displayed at a time
- Syntax highlighting with line numbers
- Language badge (TypeScript)
- File path breadcrumb at top

**File Actions:**

- "Copy Code" button (copies to clipboard)
- "Download This File" button
- Font size controls (+/-)

**Navigation:**

- "Previous File" / "Next File" buttons
- Keyboard shortcuts displayed (← / →)

**Usage Instructions (Expandable Section):**

**Installation Commands:**

```
# Navigate to SDK directory
cd [api-name]-sdk

# Install dependencies
npm install

# Build the SDK
npm run build

# Run example
npm run example
```

**Quick Start Code Example:**
Shows basic usage pulled from example.ts with syntax highlighting

**Link to Generated README:**
"📖 See full documentation in README.md"

***

**Download Options:**

**Primary Button (Large, Prominent):**

- "Download Complete SDK (.zip)"
- Downloads ZIP file: `[api-name]-sdk.zip`
- File size displayed

**Secondary Actions:**

- "Copy All Code to Clipboard" (concatenates all files with headers)
- "View on GitHub" (grayed out - future feature)

**Share Section:**

- "Generate Another SDK" button (resets to Step 1, clears session)
- "Share This SDK" button (grayed out - future feature)

**Feedback Section:**

- "How did we do?" rating (1-5 stars)
- Optional comment text area
- "Submit Feedback" button

**Quality Indicators:**

- ✅ "TypeScript syntax validated"
- ✅ "8 files generated successfully"
- ✅ "README included"
- ⚠️ "Manual testing recommended" (if validation incomplete)

***

## Technical Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│                   (Streamlit Multi-Step)                     │
│  Step 1: Input | Step 2: Config | Step 3: Review |          │
│  Step 4: Generate | Step 5: Download                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Document Processing Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ URL Fetcher  │  │ File Parser  │  │ Text Cleaner │      │
│  │  (requests)  │  │   (pypdf)    │  │(trafilatura) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  LLM Extraction Layer                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │       LLM Provider Abstraction                   │       │
│  │  (Supports: OpenAI, Anthropic, Gemini)           │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Retry Logic  │  │Circuit Breaker│  │ Rate Limiter │      │
│  │  (tenacity)  │  │   (failsafe)  │  │   (built-in) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Data Validation Layer                        │
│  ┌──────────────────────────────────────────────────┐       │
│  │          Pydantic Models                         │       │
│  │  - APISpecification                              │       │
│  │  - Endpoint                                      │       │
│  │  - Parameter                                     │       │
│  │  - Schema                                        │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ Confidence   │  │  Validator   │                         │
│  │   Scoring    │  │   (checks)   │                         │
│  └──────────────┘  └──────────────┘                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Hybrid SDK Generation Layer                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │        Template Engine (Jinja2)                  │       │
│  │  80% of code from pre-built templates            │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │        LLM Code Generator                        │       │
│  │  20% of code (endpoint-specific methods)         │       │
│  └──────────────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────────────┐       │
│  │        Code Assembler                            │       │
│  │  Combines templates + LLM output                 │       │
│  └──────────────────────────────────────────────────┘       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Output Bundling Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │File Generator│  │ ZIP Bundler  │  │Syntax Highlight│     │
│  │(all TS files)│  │  (zipfile)   │  │   (display)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```


### Data Models (Pydantic Schemas)

**Core Data Structures:**

**APISpecification Model:**

- api_name: string (required)
- base_url: string (required, URL format)
- auth_type: enum (api_key, oauth2, bearer, basic, none)
- global_headers: dict (key-value pairs)
- endpoints: list of Endpoint objects (required, min 1)
- metadata: dict (optional, version, description, etc.)

**Endpoint Model:**

- path: string (required, must start with /)
- method: enum (GET, POST, PUT, DELETE, PATCH)
- description: string (required, min 10 chars)
- parameters: list of Parameter objects
- request_body: Schema object (optional)
- response_schema: Schema object (required)
- auth_required: boolean (default: true)
- rate_limit: string (optional, e.g., "100 req/min")
- confidence_score: float (0.0-1.0, calculated)

**Parameter Model:**

- name: string (required)
- type: enum (string, number, boolean, array, object)
- required: boolean
- location: enum (query, path, header, body)
- description: string (optional)
- default_value: any (optional)
- example: any (optional)

**Schema Model:**

- type: enum (object, array, string, number, boolean)
- properties: dict (for object type)
- items: Schema object (for array type)
- example: any (optional)

**Validation Rules:**

- All URLs must be valid format
- HTTP methods must be uppercase
- Path parameters must match path string (e.g., {id} in /users/{id})
- Required parameters must be marked
- JSON schemas must be valid

***

### Hybrid Generation Strategy

**Philosophy:** Templates for correctness, LLM for customization

**Template-Based Components (80% of code):**

Pre-built, tested, guaranteed-correct TypeScript files:

**1. Retry Logic Template (retry.ts)**

- Exponential backoff implementation
- Configurable max retries, delays
- Respects Retry-After headers
- Handles all transient error codes (408, 429, 500-504)
- Circuit breaker integration
- Logging integration

**2. Rate Limiter Template (rateLimiter.ts)**

- Token bucket algorithm
- Sliding window fallback
- Per-endpoint configuration
- Concurrent request handling
- Burst allowance support
- Queue management

**3. Error Classes Template (errors.ts)**

- Base APIError class
- NetworkError (connection issues)
- ValidationError (input validation)
- RateLimitError (quota exceeded)
- AuthenticationError (401/403)
- NotFoundError (404)
- ServerError (500+)
- All errors include: statusCode, message, originalError

**4. Base Client Template (client.ts)**

- Constructor accepting config
- Request method (handles all HTTP verbs)
- Authentication injection
- Header management
- Request/response interceptors
- Timeout handling
- Logging hooks

**5. Logger Template (logger.ts)**

- Configurable log levels
- Request/response logging
- Redact sensitive data (API keys, tokens)
- Structured logging format

**6. Package Configuration Templates:**

- package.json (with correct dependencies)
- tsconfig.json (strict mode, proper target)
- .gitignore (node_modules, dist, .env)

***

**LLM-Generated Components (20% of code):**

Custom, endpoint-specific code:

**1. Endpoint Methods:**
For each endpoint, generate:

```
async methodName(params: ParamsType): Promise<ResponseType> {
  // Input validation
  // Build request URL
  // Call base client's request method
  // Parse and return typed response
}
```

**2. Type Definitions (types.ts):**

- Interface for each request parameter set
- Interface for each response body
- Enum for status codes
- Type unions for optional fields

**3. Example Usage (example.ts):**

- Import statements
- Client initialization
- Example calls for each endpoint
- Error handling examples

**4. README Content:**

- Installation instructions
- Authentication setup
- Usage examples per endpoint
- Error handling guide
- Configuration options

***

**Generation Process:**

**Phase 1: Template Rendering**

- Load all template files
- Inject configuration variables (API name, base URL, etc.)
- Render templates with Jinja2
- Validate rendered output (syntax check)

**Phase 2: LLM Code Generation**

- For each endpoint, generate method signature and implementation
- Generate type definitions from schemas
- Generate README sections
- Generate example code
- Use specific prompts optimized for each task

**Phase 3: Assembly**

- Combine templates with LLM-generated code
- Insert endpoint methods into client class
- Organize imports and exports
- Format code (consistent style)
- Validate final output

**Phase 4: Validation**

- Basic syntax check (regex patterns)
- Verify all imports resolve
- Check no undefined references
- Ensure type consistency
- Flag potential issues for user review

***

### LLM Integration Architecture

**Provider Abstraction Layer:**

Base interface all providers implement:

- extract_api_specification(documentation: str, config: dict) → APISpecification
- generate_endpoint_method(endpoint: Endpoint, config: dict) → str
- generate_type_definitions(endpoints: list) → str
- generate_readme_section(api_spec: APISpecification) → str

**Provider Implementations:**

**OpenAI Provider:**

- Model: gpt-4-turbo (default), gpt-4
- Structured output mode (JSON schema enforcement)
- Function calling for structured extraction
- Streaming disabled (unnecessary for this use case)
- Temperature: 0.2 (deterministic output)

**Anthropic Provider (Post-MVP):**

- Model: claude-3-5-sonnet-20241022
- JSON mode with schema
- Extended context window (200k tokens)
- Temperature: 0.2

**Google Gemini Provider (Post-MVP):**

- Model: gemini-1.5-pro
- JSON response format
- Lower cost option
- Temperature: 0.2

**Retry Configuration:**

- Max attempts: 3
- Backoff strategy: Exponential (1s, 2s, 4s)
- Retry on: Timeout, 429, 500, 502, 503, 504
- Circuit breaker: Open after 3 consecutive failures

**Error Handling:**

- Timeout errors: Show "LLM took too long, try smaller document"
- Rate limit errors: Show "API rate limit hit, wait 60 seconds or try different provider"
- Authentication errors: Show "Invalid API key, please check and retry"
- Content policy violations: Show "Documentation content flagged, try rephrasing"

***

### Security Architecture

**API Key Handling:**

**Storage Strategy:**

- Session-only storage (Streamlit session_state)
- Never write to disk or logs
- Clear from memory on session end
- No server-side persistence

**Display Protection:**

- Mask API keys in UI (show only last 4 characters)
- Password input fields (hidden by default)
- Redact from all log outputs
- Never include in error messages

**Transmission Security:**

- HTTPS only (enforced by Streamlit Cloud)
- Direct to LLM provider (no intermediary servers)
- No API key sent to backend analytics

**Code Security Scanning:**

Scan generated code for dangerous patterns:

- eval() or Function() usage
- innerHTML assignments
- document.write calls
- Hardcoded secrets or API keys
- SQL-like injection patterns
- Unsafe regular expressions (ReDoS)

Flag warnings if found, block generation if critical.

***

### Performance Optimization

**Caching Strategy:**

**Document Caching:**

- Cache fetched URLs for 1 hour
- Cache key: URL hash
- Invalidate on explicit user request

**LLM Response Caching:**

- Cache extraction results for identical documents
- Cache key: Document hash + provider + config
- TTL: 24 hours
- Saves cost on repeated generations

**Template Caching:**

- Load templates once at startup
- Cache rendered templates per configuration
- Invalidate only on template file changes

**Streamlit Optimizations:**

- Use @st.cache_data for pure functions
- Use @st.cache_resource for LLM client initialization
- Minimize script reruns (proper session state management)
- Lazy load heavy dependencies

**Performance Targets:**

- Document fetch: <5 seconds
- LLM extraction: <30 seconds (for 20 endpoints)
- Code generation: <30 seconds
- Total time: <90 seconds end-to-end

***

### Error Handling \& Recovery

**Error Categories:**

**1. Input Errors (User-fixable):**

- Invalid URL (not accessible)
- File too large (>5MB)
- Unsupported file format
- Empty or too-short text
- **Recovery:** Clear error message with fix instructions

**2. LLM Errors (Retry-able):**

- Timeout (LLM took too long)
- Rate limit (quota exceeded)
- Service unavailable (503)
- **Recovery:** Automatic retry (3 attempts), suggest alternative provider

**3. Extraction Errors (Partial success):**

- Incomplete API spec extracted
- Low confidence scores
- Ambiguous documentation
- **Recovery:** Show what was extracted, allow manual editing, proceed with warnings

**4. Generation Errors (Graceful degradation):**

- TypeScript syntax errors in generated code
- Missing type definitions
- Incomplete methods
- **Recovery:** Show partial SDK, allow download, provide manual fix guidance

**5. System Errors (Technical issues):**

- Out of memory
- Streamlit crash
- Network errors
- **Recovery:** Error page with "Try again" button, contact info

**Error UX Principles:**

- Never show raw exceptions to users
- Always provide next step ("Try X" or "Contact Y")
- Use friendly, non-technical language
- Show what succeeded even if something failed
- Offer alternatives (different provider, manual input, template SDK)

***

### Generated SDK Structure

**File Organization:**

```
[api-name]-sdk/
├── src/
│   ├── client.ts          # Main client class (300-500 lines)
│   ├── types.ts           # All TypeScript interfaces (200-400 lines)
│   ├── errors.ts          # Error class definitions (100-150 lines)
│   ├── utils/
│   │   ├── retry.ts       # Retry logic implementation (150-200 lines)
│   │   ├── rateLimiter.ts # Rate limiting logic (100-150 lines)
│   │   └── logger.ts      # Logging utilities (50-100 lines)
│   └── index.ts           # Main exports (20-30 lines)
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── README.md              # Complete documentation (500-1000 lines)
├── .gitignore             # Git ignore rules
└── example.ts             # Usage examples (100-200 lines)
```

**Client Class Structure:**

**Constructor:**

- Accepts SDKConfig object
- Initializes auth handler
- Sets up retry manager
- Configures rate limiter
- Creates logger instance

**Configuration Interface:**

```
interface SDKConfig {
  apiKey?: string;
  baseURL: string;
  timeout?: number;           // Default: 30000ms
  retryConfig?: {
    maxRetries: number;       // Default: 3
    baseDelay: number;        // Default: 1000ms
    maxDelay: number;         // Default: 30000ms
  };
  rateLimitConfig?: {
    requestsPerSecond: number; // Default: 10
    burstAllowance: number;    // Default: 5
  };
  logLevel?: 'debug' | 'info' | 'warn' | 'error'; // Default: 'info'
}
```

**Core Methods:**

- Private request() method (handles all HTTP logic)
- Public endpoint methods (one per API endpoint)
- Authentication helpers
- Configuration updaters

**Endpoint Method Pattern:**

```
async getResource(id: string, params?: GetResourceParams): Promise<ResourceResponse> {
  // Validate inputs
  if (!id) throw new ValidationError('Resource ID required');
  
  // Build URL
  const url = `${this.baseURL}/resources/${id}`;
  
  // Make request (with retry, rate limiting, error handling)
  const response = await this.request<ResourceResponse>({
    method: 'GET',
    url,
    params,
  });
  
  return response;
}
```

**Type Definitions Pattern:**

```
// Request parameter interfaces
interface GetResourceParams {
  include?: string[];
  fields?: string[];
  limit?: number;
}

// Response interfaces
interface ResourceResponse {
  id: string;
  name: string;
  created_at: string;
  metadata: Record<string, any>;
}

// Error response interfaces
interface APIErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
```

**Error Handling Pattern:**
All errors extend base APIError with:

- statusCode: number
- message: string
- originalError?: Error
- response?: Response object

Usage in methods:

```
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new APIError(`Request failed: ${response.statusText}`, response.status);
  }
  return await response.json();
} catch (error) {
  if (error instanceof APIError) throw error;
  throw new NetworkError('Network request failed', { cause: error });
}
```

**README Structure:**

Sections:

1. Overview (what the SDK does)
2. Installation (npm install steps)
3. Quick Start (minimal example)
4. Authentication (how to provide API key)
5. Usage Examples (one per endpoint)
6. Configuration Options (all config parameters)
7. Error Handling (all error types)
8. Rate Limiting (how it works)
9. Retry Logic (how it works)
10. TypeScript Types (overview of available types)
11. Contributing (future)
12. License

***

## Feature Specifications

### Feature 1: URL-Based Documentation Fetching

**Description:** Allow users to input a URL pointing to API documentation, automatically fetch and extract the content.

**Acceptance Criteria:**

- User can paste any valid HTTP/HTTPS URL
- System validates URL format before fetching
- System displays loading state during fetch
- Successfully fetches HTML content within 5 seconds
- Extracts clean text from HTML (removes navigation, ads, footers)
- Shows preview of fetched content (first 500 characters)
- Handles errors gracefully (404, timeout, invalid SSL, etc.)
- Supports redirects (follows up to 3 redirects)

**Technical Implementation Notes:**

- Use requests library with timeout (5 seconds)
- Use beautifulsoup4 to parse HTML
- Use trafilatura for clean text extraction
- Validate URL with regex before fetching
- Handle connection errors, timeouts, HTTP errors
- Display character count and estimated processing time

**Edge Cases:**

- URL requires authentication (show error, suggest file upload)
- URL returns non-HTML content (JSON, XML) - attempt to parse anyway
- URL is very large (>2MB) - show warning, may timeout
- URL is paywalled - error message suggesting alternatives

***

### Feature 2: File Upload Support

**Description:** Allow users to upload API documentation files in multiple formats.

**Acceptance Criteria:**

- Supports file formats: PDF, HTML, Markdown, TXT
- Drag-and-drop interface for easy upload
- File size limit: 5MB (enforced, clear error if exceeded)
- Displays file name, size, type after upload
- Extracts text content from uploaded file
- Shows character count of extracted text
- Validates file is readable and not corrupted
- Clears previous file when new one uploaded

**Technical Implementation Notes:**

- Use Streamlit's file_uploader widget
- Use pypdf2 for PDF text extraction
- Use beautifulsoup4 for HTML parsing
- Plain text for MD and TXT files
- Validate file size before processing
- Handle encoding issues (try UTF-8, then latin-1)
- Sanitize extracted text (remove excessive whitespace)

**Edge Cases:**

- PDF is scanned image (no extractable text) - show error
- File is corrupted - show error with retry option
- File encoding is unusual - attempt common encodings
- HTML file has inline styles/scripts - clean during extraction

***

### Feature 3: Example Gallery

**Description:** Showcase pre-generated SDKs for popular APIs as inspiration and proof of concept.

**Acceptance Criteria:**

- Display gallery of 3 example SDKs: Stripe, GitHub, Twilio
- Each card shows: API logo, name, short description
- "View Process" button shows simulated generation flow
- "Download SDK" button provides pre-generated ZIP
- Process view shows: Original docs snippet → Extracted spec → Generated code
- User can navigate through example without using API key
- Examples are high-quality, production-looking code

**Technical Implementation Notes:**

- Pre-generate SDKs offline, store as assets
- Create mock flow data (saved API specs, partial docs)
- Use same UI components as real generation for consistency
- Store ZIPs in repository or cloud storage
- Load examples from JSON manifest file

**Examples to Include:**

1. **Stripe Payments API**
    - Endpoints: Create payment, retrieve payment, list payments, refund
    - Demonstrates: OAuth-style auth, nested objects, error handling
2. **GitHub REST API**
    - Endpoints: Get user, list repos, create issue, star repo
    - Demonstrates: Token auth, pagination hints, rate limiting
3. **Twilio Messaging API**
    - Endpoints: Send SMS, get message status, list messages
    - Demonstrates: Basic auth, webhooks, simple responses

***

### Feature 4: LLM-Powered API Specification Extraction

**Description:** Use large language models to parse unstructured documentation and extract structured API information.

**Acceptance Criteria:**

- Supports OpenAI GPT-4-turbo (MVP), extensible to other providers
- Accepts user's own API key (never stored permanently)
- Extracts minimum viable spec: API name, base URL, auth type, endpoints
- For each endpoint extracts: path, method, parameters, response structure
- Assigns confidence score to each extracted field (0.0-1.0)
- Completes extraction within 60 seconds for typical docs (20 endpoints)
- Uses structured output (JSON mode) for reliable parsing
- Retries up to 3 times on transient failures
- Estimates and displays cost to user before processing

**Technical Implementation Notes:**

- Create Pydantic model for desired output structure
- Use OpenAI's structured output feature (JSON schema)
- Craft detailed system prompt with extraction instructions
- Include few-shot examples in prompt for better accuracy
- Calculate confidence based on field completeness and ambiguity markers
- Implement retry with tenacity library (exponential backoff)
- Timeout after 120 seconds total
- Track token usage for cost calculation

**Prompt Engineering Strategy:**

```
System: You are an API documentation parser. Extract structured information.

User: Parse this documentation and return JSON with:
{
  "api_name": string,
  "base_url": string,
  "auth_type": enum,
  "endpoints": [
    {
      "path": string (must start with /),
      "method": enum (GET/POST/PUT/DELETE/PATCH),
      "description": string (detailed),
      "parameters": [...],
      "response_schema": {...}
    }
  ]
}

Rules:
- If information is unclear, mark field as "unclear" not guess
- Extract ALL endpoints mentioned
- For parameters, identify: name, type, required, location
- For responses, provide example structure
- Be thorough but accurate

Documentation:
[USER_PROVIDED_DOCS]
```

**Confidence Scoring Algorithm:**

```
Base score: 1.0

Deductions:
- Missing base_url: -0.3
- Missing auth_type: -0.2
- Endpoint missing description: -0.1 per endpoint
- Endpoint missing parameters: -0.15 per endpoint
- Endpoint missing response: -0.2 per endpoint
- Contains "unclear" or "TODO": -0.2
- Parameters missing types: -0.05 per parameter

Bonuses:
- Includes example values: +0.1
- Includes rate limit info: +0.1
- Includes error responses: +0.1

Final score: clamp(0.0, adjusted_score, 1.0)
```

**Edge Cases:**

- Documentation mentions multiple APIs - extract all, let user choose
- Base URL not explicitly stated - attempt to infer from examples
- Authentication mentioned but unclear - set to "unclear", require user input
- Pagination mentioned - note in endpoint description
- Webhooks mentioned - note separately from REST endpoints
- GraphQL API - show error, suggest REST API or manual input

***

### Feature 5: Interactive Review \& Editing

**Description:** Allow users to review and manually correct the LLM-extracted API specification before generation.

**Acceptance Criteria:**

- Display extracted spec in user-friendly, editable format
- Show confidence badges (✅ Complete, ⚠️ Review, ❌ Missing)
- All fields are editable (text inputs, dropdowns, text areas)
- Support adding new endpoints manually
- Support removing incorrect endpoints
- Validate edits in real-time (e.g., valid JSON in schemas)
- Show validation errors inline with helpful messages
- Save edits to session state (persist during session)
- "Regenerate" option to re-run LLM extraction with adjusted settings
- Clear visual distinction between high-confidence and low-confidence fields

**Technical Implementation Notes:**

- Use Streamlit forms and expandable sections
- Color-code confidence levels (green, yellow, red)
- Use st.json for schema editing (syntax highlighting)
- Validate JSON on blur/submit
- Store edited spec in session_state
- Provide helpful placeholders (e.g., "Enter base URL like https://api.example.com")
- Add tooltips explaining each field

**Validation Rules:**

- Base URL must be valid HTTP/HTTPS URL
- Endpoint paths must start with /
- HTTP methods must be from allowed set
- Parameter types must be valid (string, number, boolean, array, object)
- Required parameters cannot have default values
- Response schemas must be valid JSON

**UI Components:**

- Expandable cards for each endpoint
- Parameter table with add/remove row functionality
- JSON editor for request/response schemas
- Dropdown menus for enums (method, auth type, etc.)
- Checkboxes for booleans (required, auth_required)
- Help icons with tooltips for complex fields

**Regeneration Feature:**

- "Regenerate" button at bottom of review page
- Shows modal with options:
    - Different temperature (lower = more conservative)
    - Focus on specific endpoints (user can list paths)
    - Provide hints (e.g., "Base URL is https://api.stripe.com")
- Re-runs LLM with adjusted prompt
- Merges new results with user's existing edits (user edits take precedence)

***

### Feature 6: Hybrid SDK Code Generation

**Description:** Generate production-quality TypeScript SDK by combining pre-built templates with LLM-generated endpoint-specific code.

**Acceptance Criteria:**

- Generates complete, compilable TypeScript project
- Uses templates for: retry logic, rate limiting, error classes, base client
- Uses LLM for: endpoint methods, type definitions, README content
- Assembles all components into cohesive SDK structure
- Includes all necessary config files (package.json, tsconfig.json, .gitignore)
- Generated code follows TypeScript best practices (strict types, no any)
- Retry logic implements exponential backoff correctly
- Rate limiting uses token bucket or sliding window algorithm
- Error handling covers all HTTP status codes
- All endpoint methods are fully typed (parameters and return values)
- README includes installation, usage examples, configuration docs

**Technical Implementation Notes:**

**Template Files to Create:**

1. **retry.ts.jinja2**: Retry logic with exponential backoff
2. **rateLimiter.ts.jinja2**: Rate limiting implementation
3. **errors.ts.jinja2**: Error class hierarchy
4. **client_base.ts.jinja2**: Base client class structure
5. **logger.ts.jinja2**: Logging utilities
6. **index.ts.jinja2**: Main exports file
7. **package.json.jinja2**: NPM package configuration
8. **tsconfig.json.jinja2**: TypeScript compiler configuration
9. **gitignore.jinja2**: Git ignore rules

**LLM Generation Tasks:**

- Per-endpoint method generation (one prompt per endpoint)
- Type definitions generation (all interfaces)
- README sections (usage examples, configuration)
- Example.ts (working usage examples)

**Assembly Process:**

1. Render all templates with config variables
2. Generate LLM code for each endpoint sequentially
3. Combine endpoint methods into client class
4. Generate type definitions from all schemas
5. Insert types into types.ts template
6. Generate README from template + LLM content
7. Format all code consistently
8. Validate basic syntax (regex checks)
9. Bundle into file structure

**Quality Checks:**

- All imports resolve (no undefined references)
- No use of TypeScript 'any' type
- All async functions return Promises
- Error handling in all methods
- Consistent code style (2-space indent, semicolons)

**Generated Package Dependencies:**

```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "winston": "^3.11.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.10.0",
    "ts-node": "^10.9.2"
  }
}
```


***

### Feature 7: Code Preview \& Download

**Description:** Display generated SDK code with syntax highlighting and provide download as ZIP file.

**Acceptance Criteria:**

- Shows all generated files in navigable tree structure
- Displays one file at a time with syntax highlighting
- Supports navigation between files (previous/next buttons)
- "Copy Code" button for each file
- "Download Complete SDK" generates ZIP file
- ZIP file contains all files in proper directory structure
- ZIP filename follows pattern: [api-name]-sdk.zip
- Syntax highlighting matches TypeScript conventions
- Line numbers displayed
- Code is scrollable for long files
- Font size adjustable (zoom in/out)
- Displays file sizes next to each filename

**Technical Implementation Notes:**

- Use streamlit-code-editor for syntax highlighting
- Store generated files in session state
- Use Python zipfile module to create archive
- Create in-memory ZIP (no disk writes)
- Use st.download_button for ZIP download
- Implement file tree with st.expander or custom HTML
- Track current file index in session state
- Provide keyboard shortcuts (left/right arrows)

**File Tree Display:**

```
📁 stripe-payments-sdk/
  📁 src/
    📄 client.ts (15.2 KB)
    📄 types.ts (8.5 KB)
    📄 errors.ts (3.1 KB)
    📁 utils/
      📄 retry.ts (4.8 KB)
      📄 rateLimiter.ts (3.9 KB)
      📄 logger.ts (2.1 KB)
    📄 index.ts (0.5 KB)
  📄 package.json (0.8 KB)
  📄 tsconfig.json (0.4 KB)
  📄 README.md (12.3 KB)
  📄 .gitignore (0.2 KB)
  📄 example.ts (3.7 KB)

Total size: 54.5 KB
```

**Code Display Features:**

- Language badge (e.g., "TypeScript")
- File path breadcrumb (e.g., src/utils/retry.ts)
- Line numbers on left
- Monospace font (Fira Code or JetBrains Mono)
- Syntax colors: keywords (blue), strings (green), comments (gray)
- Scrollable viewport (max height 600px)

**Navigation Controls:**

- ← Previous File button
- → Next File button
- Dropdown to jump to any file
- Keyboard shortcuts (document in UI)

**Usage Instructions Section:**
Expandable section showing:

```bash
# Extract the ZIP file
unzip stripe-payments-sdk.zip
cd stripe-payments-sdk

# Install dependencies
npm install

# Build the SDK
npm run build

# Try the example
npm run example
```

**Quality Indicators:**

- ✅ "8 files generated successfully"
- ✅ "TypeScript syntax validated"
- ✅ "README included"
- ℹ️ "Total size: 54.5 KB"
- ⚠️ "Manual testing recommended"

***

### Feature 8: Retry Logic \& Error Handling (Generated SDK Feature)

**Description:** Generated SDKs include production-grade retry logic with exponential backoff and comprehensive error handling.

**Acceptance Criteria:**

- Retry logic automatically retries failed requests (default: 3 attempts)
- Uses exponential backoff with jitter (1s, 2s, 4s delays)
- Respects Retry-After headers when present
- Retries on: 408, 429, 500, 502, 503, 504 status codes
- Does NOT retry on: 400, 401, 403, 404 (client errors)
- Circuit breaker opens after consecutive failures
- All errors thrown are typed (extend base APIError)
- Error messages are helpful and actionable
- Logs all retry attempts (when logging enabled)
- Configurable via SDKConfig (can disable or adjust)

**Technical Implementation (Template):**

**Retry Configuration:**

```typescript
interface RetryConfig {
  maxRetries: number;      // Default: 3
  baseDelay: number;       // Default: 1000ms
  maxDelay: number;        // Default: 30000ms
  retryableStatusCodes: number[]; // Default: [408, 429, 500, 502, 503, 504]
}
```

**Retry Logic Algorithm:**

```
1. Attempt request
2. If success (2xx) → Return response
3. If client error (4xx except 429) → Throw error immediately
4. If server error (5xx) or timeout (408) or rate limit (429):
   a. Check remaining retries
   b. If retries exhausted → Throw error
   c. Calculate delay: min(baseDelay * 2^attempt, maxDelay)
   d. Add jitter: delay += random(0, 1000)
   e. Check for Retry-After header:
      - If present, use that delay instead
   f. Wait for delay
   g. Decrement retry count
   h. Go to step 1
```

**Error Class Hierarchy:**

```
APIError (base)
├── NetworkError (connection failures, timeouts)
├── RateLimitError (429 status, includes retryAfter)
├── AuthenticationError (401, 403)
├── ValidationError (400, includes validation details)
├── NotFoundError (404)
└── ServerError (500+)
```

**Each error includes:**

- statusCode: number (HTTP status)
- message: string (human-readable)
- originalError: Error (underlying error object)
- timestamp: Date (when error occurred)
- requestInfo: object (method, URL, headers - sanitized)

**Template Implementation Strategy:**

- Pre-write retry logic as tested, correct TypeScript
- Use Jinja2 variables for configuration defaults
- Include comprehensive comments explaining logic
- Add debug logging at each retry attempt
- Handle edge cases (NaN delays, negative values)

***

### Feature 9: Rate Limiting (Generated SDK Feature)

**Description:** Generated SDKs include built-in rate limiting to respect API quotas and prevent abuse.

**Acceptance Criteria:**

- Implements token bucket algorithm (default)
- Configurable requests per second (default: 10)
- Configurable burst allowance (default: 5)
- Thread-safe for concurrent requests
- Queues requests when limit reached (FIFO)
- Per-endpoint limits supported (if API specifies)
- Global SDK-level limit as fallback
- Non-blocking (uses async/await)
- Logs rate limit events (when logging enabled)
- Can be disabled via configuration

**Technical Implementation (Template):**

**Rate Limit Configuration:**

```typescript
interface RateLimitConfig {
  requestsPerSecond: number;  // Default: 10
  burstAllowance: number;     // Default: 5
  algorithm: 'token_bucket' | 'sliding_window'; // Default: token_bucket
  perEndpointLimits?: Record<string, number>; // Optional endpoint-specific
}
```

**Token Bucket Algorithm:**

```
Bucket capacity: burstAllowance
Refill rate: requestsPerSecond tokens/second
Refill interval: 1000ms / requestsPerSecond

On request:
1. Refill bucket (add tokens based on time elapsed)
2. If bucket has tokens:
   a. Remove 1 token
   b. Allow request
3. Else:
   a. Calculate wait time: timeUntilNextToken
   b. Queue request
   c. Wait for wait time
   d. Go to step 1
```

**Implementation Details:**

- Track last refill timestamp
- Calculate tokens to add: (now - lastRefill) * requestsPerSecond / 1000
- Clamp bucket size to capacity
- Use async queue for waiting requests
- Per-endpoint tracking (separate buckets)
- Fallback to global limit if endpoint not specified

**Edge Cases Handled:**

- System time changes (clock skew) - reset bucket
- Negative wait times - treat as zero
- Very high burst - cap at reasonable maximum
- Concurrent requests - use mutex/lock

**Template Implementation Strategy:**

- Pre-write token bucket as class
- Use Jinja2 for default configuration
- Include performance optimizations (avoid unnecessary loops)
- Add metrics tracking (requests allowed, denied, queued)

***

## Non-Functional Requirements

### Performance

**Response Time:**

- Page load: <2 seconds
- URL fetch: <5 seconds
- LLM extraction: <60 seconds (20 endpoints)
- Code generation: <30 seconds
- Total end-to-end: <90 seconds

**Scalability:**

- Support 10 concurrent users (Streamlit free tier limit)
- Handle API docs up to 50k tokens (~200KB text)
- Generate SDKs with up to 50 endpoints
- Create ZIPs up to 1MB

**Resource Constraints:**

- Memory usage: <512MB per session
- Streamlit Cloud limits: 1 CPU, 800MB RAM
- Storage: No persistent storage required


### Reliability

**Uptime:**

- Target: 95% uptime (accounting for Streamlit maintenance)
- Graceful degradation when LLM provider unavailable
- Fallback to cached results when possible

**Error Recovery:**

- Automatic retry for transient failures (3 attempts)
- Clear error messages for permanent failures
- Partial results shown even if generation incomplete
- No data loss during session (everything in session_state)

**Data Integrity:**

- Validate all user inputs before processing
- Validate LLM outputs before displaying
- Ensure generated code has no syntax errors (basic check)
- ZIP files properly formatted and extractable


### Security

**API Key Protection:**

- Never log API keys (even in debug mode)
- Mask in UI (show only last 4 characters)
- Clear from memory on session end
- Never send to analytics or third parties
- Session-only storage (no persistence)

**Input Sanitization:**

- Sanitize user text inputs (prevent XSS)
- Validate URLs before fetching
- Scan uploaded files for malicious content
- Limit file sizes to prevent DoS

**Generated Code Security:**

- Scan for dangerous patterns (eval, innerHTML)
- No hardcoded secrets in generated code
- Use secure dependencies (pinned versions)
- Flag security warnings to user

**Network Security:**

- All communication over HTTPS
- Validate SSL certificates
- No sensitive data in URL parameters
- CORS headers properly configured


### Usability

**Learnability:**

- New users can generate first SDK in <10 minutes
- Tooltips and help text on all complex fields
- Example gallery as learning tool
- Clear visual feedback at every step

**Efficiency:**

- Minimal clicks required (5 steps, 1 click per step)
- Keyboard shortcuts for power users
- Autosave user progress in session
- Quick restart (Generate Another button)

**Error Prevention:**

- Inline validation with helpful messages
- Confirmation dialogs for destructive actions
- Disable invalid options (grayed out)
- Suggest corrections for common mistakes

**Accessibility:**

- Keyboard navigation support
- Screen reader compatible (alt text on images)
- High contrast mode support
- Responsive design (mobile-friendly)


### Maintainability

**Code Quality:**

- Type hints on all Python functions
- Docstrings for all modules and classes
- Consistent code style (Black formatter)
- Modular architecture (separation of concerns)

**Documentation:**

- README with setup instructions
- Architecture documentation (this PRD)
- Inline code comments for complex logic
- API documentation for all modules

**Testability:**

- Unit tests for core functions (80% coverage target)
- Integration tests for end-to-end flows
- Mock LLM responses for deterministic tests
- Test fixtures for common scenarios

**Extensibility:**

- Plugin architecture for new LLM providers
- Template system for adding new languages
- Configuration-driven feature flags
- Modular components (easy to swap)


### Compatibility

**Browser Support:**

- Chrome 90+ (primary)
- Firefox 88+
- Safari 14+
- Edge 90+

**Platform Support:**

- Desktop: Windows, macOS, Linux
- Mobile: iOS Safari, Android Chrome (responsive view)

**Deployment:**

- Streamlit Community Cloud (primary)
- Compatible with Docker deployment (backup)
- Can run locally (python app.py)

***

## Technical Constraints \& Limitations

### Acknowledged Limitations (Transparency)

**1. Demo Tool, Not Production Service:**

- Single-threaded Streamlit server (not scalable)
- No user authentication or per-user storage
- Session-based only (data lost on refresh)
- Not designed for high traffic (10 concurrent users max)
- No SLA or uptime guarantees

**2. LLM Extraction Accuracy:**

- Success rate: 70-80% on real-world docs (not 100%)
- Requires human review and editing
- Struggles with very ambiguous or incomplete docs
- May hallucinate details not in documentation
- Dependent on L

