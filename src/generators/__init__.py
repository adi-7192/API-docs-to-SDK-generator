"""SDK code generation utilities."""

from .template_engine import TemplateEngine
from .assembler import (
    assemble_client_class,
    assemble_types_file,
    assemble_example_file,
    create_file_structure,
    bundle_to_zip,
    get_file_tree_display,
    calculate_total_size,
    format_size,
)
from .validator import (
    validate_typescript_syntax,
    check_imports,
    scan_for_security_issues,
    validate_no_any_type,
    format_code,
    validate_all,
)

__all__ = [
    # Template Engine
    "TemplateEngine",
    # Assembler
    "assemble_client_class",
    "assemble_types_file",
    "assemble_example_file",
    "create_file_structure",
    "bundle_to_zip",
    "get_file_tree_display",
    "calculate_total_size",
    "format_size",
    # Validator
    "validate_typescript_syntax",
    "check_imports",
    "scan_for_security_issues",
    "validate_no_any_type",
    "format_code",
    "validate_all",
]
