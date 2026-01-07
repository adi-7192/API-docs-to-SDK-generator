"""Unit tests for SDK generators."""

import pytest
from src.generators import (
    validate_typescript_syntax,
    scan_for_security_issues,
    format_code,
    bundle_to_zip,
    get_file_tree_display,
)


def test_validate_typescript_syntax_valid():
    """Test TypeScript syntax validation with valid code."""
    code = """
    function hello() {
        return "world";
    }
    """
    
    errors = validate_typescript_syntax(code)
    assert len(errors) == 0


def test_validate_typescript_syntax_mismatched_braces():
    """Test detection of mismatched braces."""
    code = """
    function hello() {
        return "world";
    // Missing closing brace
    """
    
    errors = validate_typescript_syntax(code)
    assert len(errors) > 0
    assert "braces" in errors[0].lower()


def test_scan_for_security_issues_eval():
    """Test detection of eval() usage."""
    code = 'const result = eval("dangerous code");'
    
    warnings = scan_for_security_issues(code)
    assert len(warnings) > 0
    assert any("eval" in w.lower() for w in warnings)


def test_scan_for_security_issues_hardcoded_key():
    """Test detection of hardcoded API keys."""
    code = 'const apiKey = "sk_test_1234567890abcdefghijklmnop";'
    
    warnings = scan_for_security_issues(code)
    assert len(warnings) > 0
    assert any("api key" in w.lower() or "token" in w.lower() for w in warnings)


def test_format_code():
    """Test code formatting."""
    code = "function test()   {  \n\n\n\n  return true;  \n\n\n}"
    
    formatted = format_code(code)
    
    # Should remove trailing whitespace and excessive blank lines
    assert "  \n" not in formatted
    assert "\n\n\n\n" not in formatted


def test_bundle_to_zip():
    """Test ZIP bundling."""
    file_structure = {
        "package.json": '{"name": "test"}',
        "src/index.ts": "export default {};"
    }
    
    zip_bytes = bundle_to_zip(file_structure, "Test API")
    
    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 0


def test_get_file_tree_display():
    """Test file tree display generation."""
    file_structure = {
        "package.json": "...",
        "src/client.ts": "...",
        "src/types.ts": "..."
    }
    
    tree = get_file_tree_display(file_structure)
    
    assert "package.json" in tree
    assert "src/" in tree or "src" in tree
    assert "client.ts" in tree
