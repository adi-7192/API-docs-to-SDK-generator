"""Streamlit UI components for Step 1: Input Selection."""

import streamlit as st
from typing import Tuple, Optional
from ..processors import (
    fetch_url,
    extract_text_from_html,
    parse_file,
    get_text_statistics,
    sanitize_for_llm,
)


def render_step1_input_selection() -> Tuple[bool, str, str]:
    """
    Render Step 1: Input Selection UI.
    
    Returns:
        Tuple of (has_input, documentation_text, input_source)
    """
    st.markdown("## 📄 Step 1: Provide API Documentation")
    st.markdown("Choose how you'd like to provide the API documentation:")
    
    # Input method selector
    input_method = st.radio(
        "Input Method",
        ["🔗 URL", "📁 File Upload", "✍️ Text Paste", "🎨 Example Gallery"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    documentation_text = ""
    input_source = ""
    has_input = False
    
    if input_method == "🔗 URL":
        has_input, documentation_text, input_source = render_url_input()
    elif input_method == "📁 File Upload":
        has_input, documentation_text, input_source = render_file_upload()
    elif input_method == "✍️ Text Paste":
        has_input, documentation_text, input_source = render_text_paste()
    else:  # Example Gallery
        has_input, documentation_text, input_source = render_example_gallery()
    
    # Show statistics if we have input
    if has_input and documentation_text:
        render_input_statistics(documentation_text)
    
    return has_input, documentation_text, input_source


def render_url_input() -> Tuple[bool, str, str]:
    """Render URL input section."""
    st.markdown("### 🔗 Fetch from URL")
    st.markdown("Enter the URL of the API documentation page:")
    
    url = st.text_input(
        "Documentation URL",
        placeholder="https://docs.example.com/api",
        help="Enter the full URL including https://"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_button = st.button("🚀 Fetch", type="primary", use_container_width=True)
    
    if fetch_button and url:
        with st.spinner("Fetching documentation..."):
            success, content, message = fetch_url(url, timeout=10)
            
            if success:
                text = extract_text_from_html(content)
                cleaned_text = sanitize_for_llm(text)
                
                st.success(f"✅ {message}")
                
                # Show preview
                with st.expander("📖 Preview (first 500 characters)"):
                    st.text(cleaned_text[:500] + "...")
                
                return True, cleaned_text, f"URL: {url}"
            else:
                st.error(f"❌ {message}")
                return False, "", ""
    
    return False, "", ""


def render_file_upload() -> Tuple[bool, str, str]:
    """Render file upload section."""
    st.markdown("### 📁 Upload Documentation File")
    st.markdown("Upload a PDF, HTML, TXT, or Markdown file:")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "html", "htm", "txt", "md", "markdown"],
        help="Maximum file size: 5 MB"
    )
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        
        with st.spinner("Processing file..."):
            success, text, message = parse_file(file_bytes, uploaded_file.name)
            
            if success:
                cleaned_text = sanitize_for_llm(text)
                
                st.success(f"✅ {message}")
                
                # Show preview
                with st.expander("📖 Preview (first 500 characters)"):
                    st.text(cleaned_text[:500] + "...")
                
                return True, cleaned_text, f"File: {uploaded_file.name}"
            else:
                st.error(f"❌ {message}")
                return False, "", ""
    
    return False, "", ""


def render_text_paste() -> Tuple[bool, str, str]:
    """Render text paste section."""
    st.markdown("### ✍️ Paste Documentation Text")
    st.markdown("Paste your API documentation directly:")
    
    text = st.text_area(
        "Documentation Text",
        height=300,
        placeholder="Paste your API documentation here...\n\nExample:\n# My API\n\nBase URL: https://api.example.com/v1\n\n## Endpoints\n\n### GET /users\nRetrieve all users...",
        help="Paste the full API documentation"
    )
    
    if text and len(text) >= 100:
        cleaned_text = sanitize_for_llm(text)
        
        st.success(f"✅ Text received ({len(text)} characters)")
        
        return True, cleaned_text, "Text Paste"
    elif text and len(text) < 100:
        st.warning("⚠️ Please provide at least 100 characters of documentation")
        return False, "", ""
    
    return False, "", ""


def render_example_gallery() -> Tuple[bool, str, str]:
    """Render example gallery section."""
    st.markdown("### 🎨 Example Gallery")
    st.markdown("Choose from pre-built examples to see the SDK generator in action:")
    
    examples = {
        "Stripe Payments API": {
            "description": "Payment processing API with charges, customers, and subscriptions",
            "url": "https://stripe.com/docs/api",
            "file": "stripe_example.txt"
        },
        "GitHub REST API": {
            "description": "Repository management, issues, pull requests, and more",
            "url": "https://docs.github.com/en/rest",
            "file": "github_example.txt"
        },
        "Twilio Messaging API": {
            "description": "SMS and messaging API for sending and receiving messages",
            "url": "https://www.twilio.com/docs/sms/api",
            "file": "twilio_example.txt"
        }
    }
    
    selected_example = st.selectbox(
        "Select an example",
        options=list(examples.keys()),
        help="Choose an example to generate an SDK"
    )
    
    if selected_example:
        example = examples[selected_example]
        
        st.info(f"📚 **{selected_example}**\n\n{example['description']}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            load_button = st.button("📥 Load Example", type="primary", use_container_width=True)
        
        if load_button:
            # For now, show a placeholder message
            # In a real implementation, we'd load from examples/ directory
            st.warning("🚧 Example gallery coming soon! For now, please use URL, file upload, or text paste.")
            return False, "", ""
    
    return False, "", ""


def render_input_statistics(text: str):
    """Render statistics about the input."""
    stats = get_text_statistics(text)
    
    st.markdown("---")
    st.markdown("### 📊 Input Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Characters", f"{stats['characters']:,}")
    
    with col2:
        st.metric("Words", f"{stats['words']:,}")
    
    with col3:
        st.metric("Est. Tokens", f"{stats['estimated_tokens']:,}")
    
    with col4:
        st.metric("Est. Cost", f"${stats['estimated_cost_gpt4']}")
