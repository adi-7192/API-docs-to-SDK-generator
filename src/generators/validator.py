"""Code validation and security scanning."""

import re
from typing import List, Tuple


def validate_typescript_syntax(code: str) -> List[str]:
    """
    Perform basic TypeScript syntax validation using regex patterns.
    
    Args:
        code: TypeScript code to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    # Check for unclosed braces
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")
    
    # Check for unclosed parentheses
    open_parens = code.count('(')
    close_parens = code.count(')')
    if open_parens != close_parens:
        errors.append(f"Mismatched parentheses: {open_parens} opening, {close_parens} closing")
    
    # Check for unclosed brackets
    open_brackets = code.count('[')
    close_brackets = code.count(']')
    if open_brackets != close_brackets:
        errors.append(f"Mismatched brackets: {open_brackets} opening, {close_brackets} closing")
    
    return errors


def check_imports(code: str) -> List[str]:
    """
    Check for potential undefined references in imports.
    
    Args:
        code: TypeScript code to check
        
    Returns:
        List of potential issues
    """
    issues = []
    
    # Extract import statements
    import_pattern = r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'
    imports = re.findall(import_pattern, code)
    
    # Check for relative imports that might be broken
    for imp in imports:
        if imp.startswith('./') or imp.startswith('../'):
            # This is a relative import - we can't fully validate without file system
            # but we can check for obvious issues
            if imp.count('../') > 3:
                issues.append(f"Suspiciously deep relative import: {imp}")
    
    return issues


def scan_for_security_issues(code: str) -> List[str]:
    """
    Scan code for dangerous patterns.
    
    Args:
        code: Code to scan
        
    Returns:
        List of security warnings
    """
    warnings = []
    
    # Dangerous patterns
    dangerous_patterns = [
        (r'\beval\s*\(', "Use of eval() detected - potential security risk"),
        (r'\bFunction\s*\(', "Use of Function() constructor detected - potential security risk"),
        (r'\.innerHTML\s*=', "Direct innerHTML assignment detected - potential XSS risk"),
        (r'document\.write\s*\(', "Use of document.write() detected - not recommended"),
        (r'dangerouslySetInnerHTML', "Use of dangerouslySetInnerHTML detected"),
        (r'__proto__', "Direct __proto__ manipulation detected"),
    ]
    
    for pattern, message in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            warnings.append(message)
    
    # Check for hardcoded secrets (basic check)
    secret_patterns = [
        (r'api[_-]?key\s*[:=]\s*["\'][\w-]{20,}["\']', "Potential hardcoded API key detected"),
        (r'password\s*[:=]\s*["\'].+["\']', "Potential hardcoded password detected"),
        (r'secret\s*[:=]\s*["\'].+["\']', "Potential hardcoded secret detected"),
        (r'token\s*[:=]\s*["\'][\w-]{20,}["\']', "Potential hardcoded token detected"),
    ]
    
    for pattern, message in secret_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            warnings.append(message)
    
    return warnings


def validate_no_any_type(code: str) -> List[str]:
    """
    Check for use of 'any' type in TypeScript code.
    
    Args:
        code: TypeScript code to check
        
    Returns:
        List of warnings about 'any' usage
    """
    warnings = []
    
    # Find 'any' type usage
    any_pattern = r':\s*any\b'
    matches = re.finditer(any_pattern, code)
    
    count = 0
    for match in matches:
        count += 1
    
    if count > 0:
        warnings.append(f"Found {count} uses of 'any' type - consider using specific types")
    
    return warnings


def format_code(code: str) -> str:
    """
    Apply basic code formatting.
    
    Args:
        code: Code to format
        
    Returns:
        Formatted code
    """
    # Remove trailing whitespace from each line
    lines = code.split('\n')
    lines = [line.rstrip() for line in lines]
    
    # Remove multiple consecutive blank lines
    formatted_lines = []
    prev_blank = False
    for line in lines:
        is_blank = len(line.strip()) == 0
        if is_blank and prev_blank:
            continue  # Skip consecutive blank lines
        formatted_lines.append(line)
        prev_blank = is_blank
    
    # Ensure file ends with newline
    code = '\n'.join(formatted_lines)
    if not code.endswith('\n'):
        code += '\n'
    
    return code


def validate_all(code: str, file_path: str) -> Tuple[bool, List[str], List[str]]:
    """
    Run all validation checks on code.
    
    Args:
        code: Code to validate
        file_path: Path of the file (for context in messages)
        
    Returns:
        Tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Syntax validation
    syntax_errors = validate_typescript_syntax(code)
    errors.extend([f"{file_path}: {err}" for err in syntax_errors])
    
    # Import checks
    import_issues = check_imports(code)
    warnings.extend([f"{file_path}: {issue}" for issue in import_issues])
    
    # Security scanning
    security_warnings = scan_for_security_issues(code)
    warnings.extend([f"{file_path}: {warn}" for warn in security_warnings])
    
    # Type checking
    any_warnings = validate_no_any_type(code)
    warnings.extend([f"{file_path}: {warn}" for warn in any_warnings])
    
    is_valid = len(errors) == 0
    
    return is_valid, errors, warnings
