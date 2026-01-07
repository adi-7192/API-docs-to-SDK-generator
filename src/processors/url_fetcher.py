"""URL fetching and content extraction."""

import requests
from typing import Tuple
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format. Must include scheme (http/https) and domain."
        if result.scheme not in ['http', 'https']:
            return False, "URL must use HTTP or HTTPS protocol."
        return True, ""
    except Exception as e:
        return False, f"Invalid URL: {str(e)}"


def fetch_url(url: str, timeout: int = 5) -> Tuple[bool, str, str]:
    """
    Fetch content from a URL.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        Tuple of (success, content_or_error, status_message)
    """
    # Validate URL first
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        return False, "", error_msg
    
    try:
        # Make request with redirects
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (API SDK Generator Bot)'
            }
        )
        
        # Check status code
        if response.status_code == 404:
            return False, "", "Page not found (404)"
        elif response.status_code == 403:
            return False, "", "Access forbidden (403). Try uploading the documentation as a file instead."
        elif response.status_code >= 400:
            return False, "", f"HTTP error {response.status_code}"
        
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type and 'text/plain' not in content_type:
            return False, "", f"Unsupported content type: {content_type}. Expected HTML or text."
        
        return True, response.text, f"Successfully fetched {len(response.text)} characters"
        
    except requests.exceptions.Timeout:
        return False, "", f"Request timed out after {timeout} seconds"
    except requests.exceptions.ConnectionError:
        return False, "", "Connection error. Please check the URL and your internet connection."
    except requests.exceptions.TooManyRedirects:
        return False, "", "Too many redirects. The URL may be misconfigured."
    except requests.exceptions.SSLError:
        return False, "", "SSL certificate verification failed."
    except Exception as e:
        return False, "", f"Unexpected error: {str(e)}"


def extract_text_from_html(html: str) -> str:
    """
    Extract clean text from HTML content using trafilatura.
    
    Args:
        html: HTML content
        
    Returns:
        Extracted text
    """
    # Use trafilatura for clean extraction
    extracted = trafilatura.extract(html, include_comments=False, include_tables=True)
    
    if extracted:
        return extracted
    
    # Fallback to BeautifulSoup if trafilatura fails
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text


def get_preview(text: str, max_chars: int = 500) -> str:
    """
    Get a preview of the text content.
    
    Args:
        text: Full text
        max_chars: Maximum characters to include in preview
        
    Returns:
        Preview string
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def get_character_count(text: str) -> int:
    """Get character count of text."""
    return len(text)


def estimate_token_count(text: str) -> int:
    """
    Estimate token count for LLM processing.
    Rough estimate: 1 token ≈ 4 characters
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    return len(text) // 4
