"""Text cleaning and preprocessing utilities."""

import re
from typing import Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Normalize whitespace
    text = normalize_whitespace(text)
    
    # Remove excessive newlines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    # Replace tabs with spaces
    text = text.replace('\t', ' ')
    
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove spaces at the beginning and end of lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text


def remove_navigation_elements(html_text: str) -> str:
    """
    Remove common navigation elements from extracted HTML text.
    
    Args:
        html_text: Text extracted from HTML
        
    Returns:
        Cleaned text
    """
    # Common navigation patterns to remove
    patterns = [
        r'Skip to (main )?content',
        r'Table of [Cc]ontents?',
        r'Navigation',
        r'Menu',
        r'Copyright ©.*',
        r'All rights reserved',
        r'Privacy Policy',
        r'Terms of Service',
        r'Cookie Policy',
    ]
    
    for pattern in patterns:
        html_text = re.sub(pattern, '', html_text, flags=re.IGNORECASE)
    
    return html_text


def truncate_if_needed(text: str, max_tokens: int = 50000) -> Tuple[str, bool]:
    """
    Truncate text if it exceeds maximum token count.
    
    Args:
        text: Text to potentially truncate
        max_tokens: Maximum allowed tokens (rough estimate: 1 token ≈ 4 chars)
        
    Returns:
        Tuple of (truncated_text, was_truncated)
    """
    max_chars = max_tokens * 4
    
    if len(text) <= max_chars:
        return text, False
    
    # Truncate and add notice
    truncated = text[:max_chars]
    
    # Try to truncate at a sentence boundary
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.9:  # If we can find a period in the last 10%
        truncated = truncated[:last_period + 1]
    
    return truncated, True


def extract_code_blocks(text: str) -> list:
    """
    Extract code blocks from markdown-style text.
    
    Args:
        text: Text potentially containing code blocks
        
    Returns:
        List of code block contents
    """
    # Match code blocks with triple backticks
    pattern = r'```[\w]*\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def remove_code_blocks(text: str) -> str:
    """
    Remove code blocks from text (useful for focusing on documentation prose).
    
    Args:
        text: Text potentially containing code blocks
        
    Returns:
        Text with code blocks removed
    """
    # Remove code blocks with triple backticks
    text = re.sub(r'```[\w]*\n.*?```', '[CODE BLOCK REMOVED]', text, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '[CODE]', text)
    
    return text


def sanitize_for_llm(text: str) -> str:
    """
    Sanitize text for LLM processing.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Clean text
    text = clean_text(text)
    
    # Remove navigation elements
    text = remove_navigation_elements(text)
    
    # Remove excessive code blocks (keep some for context)
    # This is optional - we might want to keep code examples
    
    return text


def get_text_statistics(text: str) -> dict:
    """
    Get statistics about the text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with text statistics
    """
    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.splitlines())
    estimated_tokens = char_count // 4
    
    return {
        "characters": char_count,
        "words": word_count,
        "lines": line_count,
        "estimated_tokens": estimated_tokens,
        "estimated_cost_gpt4": round(estimated_tokens * 0.00003, 4),  # Rough estimate
    }


# Fix import
from typing import Tuple
