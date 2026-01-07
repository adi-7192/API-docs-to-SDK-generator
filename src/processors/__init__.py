"""Document processing utilities."""

from .url_fetcher import (
    validate_url,
    fetch_url,
    extract_text_from_html,
    get_preview,
    get_character_count,
    estimate_token_count,
)
from .file_parser import (
    validate_file_size,
    parse_pdf,
    parse_html,
    parse_text,
    parse_file,
    get_file_info,
)
from .text_cleaner import (
    clean_text,
    normalize_whitespace,
    remove_navigation_elements,
    truncate_if_needed,
    extract_code_blocks,
    remove_code_blocks,
    sanitize_for_llm,
    get_text_statistics,
)

__all__ = [
    # URL Fetcher
    "validate_url",
    "fetch_url",
    "extract_text_from_html",
    "get_preview",
    "get_character_count",
    "estimate_token_count",
    # File Parser
    "validate_file_size",
    "parse_pdf",
    "parse_html",
    "parse_text",
    "parse_file",
    "get_file_info",
    # Text Cleaner
    "clean_text",
    "normalize_whitespace",
    "remove_navigation_elements",
    "truncate_if_needed",
    "extract_code_blocks",
    "remove_code_blocks",
    "sanitize_for_llm",
    "get_text_statistics",
]
