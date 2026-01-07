"""Unit tests for document processors."""

import pytest
from src.processors import (
    validate_url,
    get_text_statistics,
    clean_text,
    sanitize_for_llm,
)


def test_validate_url_valid():
    """Test URL validation with valid URLs."""
    is_valid, error = validate_url("https://docs.example.com/api")
    assert is_valid is True
    assert error == ""
    
    is_valid, error = validate_url("http://api.example.com")
    assert is_valid is True


def test_validate_url_invalid():
    """Test URL validation with invalid URLs."""
    is_valid, error = validate_url("not-a-url")
    assert is_valid is False
    assert "Invalid URL" in error
    
    is_valid, error = validate_url("ftp://example.com")
    assert is_valid is False
    assert "HTTP or HTTPS" in error


def test_get_text_statistics():
    """Test text statistics calculation."""
    text = "Hello world! This is a test."
    stats = get_text_statistics(text)
    
    assert stats["characters"] == len(text)
    assert stats["words"] == 6
    assert stats["estimated_tokens"] > 0
    assert "estimated_cost_gpt4" in stats


def test_clean_text():
    """Test text cleaning."""
    text = "Hello   world\n\n\n\nTest"
    cleaned = clean_text(text)
    
    # Should remove excessive whitespace and newlines
    assert "   " not in cleaned
    assert "\n\n\n" not in cleaned


def test_sanitize_for_llm():
    """Test text sanitization for LLM."""
    text = "API Documentation\n\nSkip to content\n\nTable of Contents\n\nActual content here"
    sanitized = sanitize_for_llm(text)
    
    # Should remove navigation elements
    assert "Skip to content" not in sanitized or len(sanitized) > 0
