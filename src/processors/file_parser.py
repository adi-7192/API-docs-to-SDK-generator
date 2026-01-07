"""File parsing for uploaded documentation files."""

from typing import Tuple, Optional
from io import BytesIO
import PyPDF2
from bs4 import BeautifulSoup


def validate_file_size(file_bytes: bytes, max_mb: int = 5) -> Tuple[bool, str]:
    """
    Validate file size.
    
    Args:
        file_bytes: File content as bytes
        max_mb: Maximum file size in megabytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_mb:
        return False, f"File size ({size_mb:.2f} MB) exceeds maximum allowed size ({max_mb} MB)"
    return True, ""


def parse_pdf(file_bytes: bytes) -> Tuple[bool, str, str]:
    """
    Extract text from PDF file.
    
    Args:
        file_bytes: PDF file content as bytes
        
    Returns:
        Tuple of (success, extracted_text, status_message)
    """
    try:
        pdf_file = BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF has pages
        if len(pdf_reader.pages) == 0:
            return False, "", "PDF file is empty (no pages found)"
        
        # Extract text from all pages
        text_parts = []
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            except Exception as e:
                # Continue with other pages if one fails
                print(f"Warning: Failed to extract text from page {page_num + 1}: {e}")
        
        if not text_parts:
            return False, "", "No text could be extracted from PDF. It may be a scanned image."
        
        full_text = "\n\n".join(text_parts)
        return True, full_text, f"Successfully extracted text from {len(pdf_reader.pages)} pages"
        
    except PyPDF2.errors.PdfReadError:
        return False, "", "Invalid or corrupted PDF file"
    except Exception as e:
        return False, "", f"Error parsing PDF: {str(e)}"


def parse_html(file_bytes: bytes) -> Tuple[bool, str, str]:
    """
    Parse HTML file and extract text.
    
    Args:
        file_bytes: HTML file content as bytes
        
    Returns:
        Tuple of (success, extracted_text, status_message)
    """
    try:
        # Try UTF-8 first, then fall back to latin-1
        try:
            html_content = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            html_content = file_bytes.decode('latin-1')
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script, style, nav, footer, header elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        if not text or len(text) < 100:
            return False, "", "HTML file contains insufficient text content"
        
        return True, text, f"Successfully extracted {len(text)} characters from HTML"
        
    except Exception as e:
        return False, "", f"Error parsing HTML: {str(e)}"


def parse_text(file_bytes: bytes) -> Tuple[bool, str, str]:
    """
    Parse plain text or markdown file.
    
    Args:
        file_bytes: Text file content as bytes
        
    Returns:
        Tuple of (success, extracted_text, status_message)
    """
    try:
        # Try multiple encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                text = file_bytes.decode(encoding)
                
                if not text or len(text) < 100:
                    return False, "", "File contains insufficient text content (minimum 100 characters)"
                
                return True, text, f"Successfully loaded {len(text)} characters"
            except UnicodeDecodeError:
                continue
        
        return False, "", "Unable to decode file. Unsupported text encoding."
        
    except Exception as e:
        return False, "", f"Error parsing text file: {str(e)}"


def parse_file(file_bytes: bytes, filename: str, max_mb: int = 5) -> Tuple[bool, str, str]:
    """
    Parse uploaded file based on extension.
    
    Args:
        file_bytes: File content as bytes
        filename: Original filename
        max_mb: Maximum file size in megabytes
        
    Returns:
        Tuple of (success, extracted_text, status_message)
    """
    # Validate file size first
    is_valid, error_msg = validate_file_size(file_bytes, max_mb)
    if not is_valid:
        return False, "", error_msg
    
    # Determine file type from extension
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return parse_pdf(file_bytes)
    elif filename_lower.endswith(('.html', '.htm')):
        return parse_html(file_bytes)
    elif filename_lower.endswith(('.txt', '.md', '.markdown')):
        return parse_text(file_bytes)
    else:
        return False, "", f"Unsupported file type. Supported formats: PDF, HTML, TXT, MD"


def get_file_info(file_bytes: bytes, filename: str) -> dict:
    """
    Get information about the uploaded file.
    
    Args:
        file_bytes: File content as bytes
        filename: Original filename
        
    Returns:
        Dictionary with file information
    """
    size_bytes = len(file_bytes)
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    
    # Determine file type
    file_type = "Unknown"
    if filename.lower().endswith('.pdf'):
        file_type = "PDF"
    elif filename.lower().endswith(('.html', '.htm')):
        file_type = "HTML"
    elif filename.lower().endswith(('.txt', '.md', '.markdown')):
        file_type = "Text/Markdown"
    
    return {
        "filename": filename,
        "type": file_type,
        "size_bytes": size_bytes,
        "size_kb": round(size_kb, 2),
        "size_mb": round(size_mb, 2),
        "size_display": f"{size_mb:.2f} MB" if size_mb >= 1 else f"{size_kb:.2f} KB"
    }
