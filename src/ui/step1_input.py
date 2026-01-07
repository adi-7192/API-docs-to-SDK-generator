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
    st.markdown("### 📁 Upload Documentation Files")
    st.markdown("Upload one or more PDF, HTML, TXT, or Markdown files:")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "html", "htm", "txt", "md", "markdown"],
        help="Maximum file size: 5 MB per file. You can upload multiple files to combine documentation.",
        accept_multiple_files=True  # Enable multiple file upload
    )
    
    if uploaded_files:
        all_texts = []
        file_names = []
        
        with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.read()
                
                success, text, message = parse_file(file_bytes, uploaded_file.name)
                
                if success:
                    all_texts.append(text)
                    file_names.append(uploaded_file.name)
                    st.success(f"✅ {uploaded_file.name}: {message}")
                else:
                    st.error(f"❌ {uploaded_file.name}: {message}")
        
        if all_texts:
            # Combine all documents with clear separators
            combined_text = "\n\n" + "="*80 + "\n\n".join([
                f"=== Document: {name} ===\n\n{text}" 
                for name, text in zip(file_names, all_texts)
            ])
            
            cleaned_text = sanitize_for_llm(combined_text)
            
            # Show summary
            st.info(f"📚 **Combined {len(all_texts)} document(s)**")
            
            # Show preview
            with st.expander("📖 Preview (first 500 characters of combined text)"):
                st.text(cleaned_text[:500] + "...")
            
            file_list = ", ".join(file_names)
            return True, cleaned_text, f"Files: {file_list}"
        else:
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
    
    from pathlib import Path
    
    # Get the project root directory
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    examples_dir = project_root / "examples"
    
    examples = {
        "Stripe Payments API": {
            "description": "Payment processing API with charges, customers, and subscriptions",
            "file": examples_dir / "stripe" / "stripe_api_docs.md"
        },
        "GitHub REST API": {
            "description": "Repository management, issues, pull requests, and more",
            "file": examples_dir / "github" / "github_api_docs.md"
        },
        "Twilio Messaging API": {
            "description": "SMS and messaging API for sending and receiving messages",
            "file": examples_dir / "twilio" / "twilio_api_docs.md"
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
            try:
                # Load the example file
                example_file = example['file']
                
                if example_file.exists():
                    with open(example_file, 'r', encoding='utf-8') as f:
                        documentation_text = f.read()
                    
                    cleaned_text = sanitize_for_llm(documentation_text)
                    
                    st.success(f"✅ Loaded {selected_example} example!")
                    
                    # Show preview
                    with st.expander("📖 Preview (first 500 characters)"):
                        st.text(cleaned_text[:500] + "...")
                    
                    return True, cleaned_text, f"Example: {selected_example}"
                else:
                    st.error(f"❌ Example file not found: {example_file}")
                    return False, "", ""
                    
            except Exception as e:
                st.error(f"❌ Error loading example: {str(e)}")
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
