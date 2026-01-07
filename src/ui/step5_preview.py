"""Streamlit UI components for Step 5: Preview & Download."""

import streamlit as st
from typing import Dict, Optional
from ..generators import get_file_tree_display, calculate_total_size, format_size


def render_step5_preview_download(
    file_structure: Optional[Dict[str, str]],
    zip_bytes: Optional[bytes],
    api_name: str
) -> None:
    """
    Render Step 5: Preview & Download UI.
    
    Args:
        file_structure: Dictionary mapping file paths to content
        zip_bytes: ZIP file as bytes
        api_name: API name for download filename
    """
    st.markdown("## 🎉 Step 5: Preview & Download")
    
    if file_structure is None or zip_bytes is None:
        st.info("⏳ Generating SDK...")
        return
    
    st.success("✅ SDK generated successfully!")
    
    # Generation Summary
    st.markdown("### 📊 Generation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Files Generated", len(file_structure))
    
    with col2:
        total_size = calculate_total_size(file_structure)
        st.metric("Total Size", format_size(total_size))
    
    with col3:
        st.metric("ZIP Size", format_size(len(zip_bytes)))
    
    # File Tree
    st.markdown("---")
    st.markdown("### 📁 File Structure")
    
    tree = get_file_tree_display(file_structure)
    st.code(tree, language="text")
    
    # Code Preview
    st.markdown("---")
    st.markdown("### 👀 Code Preview")
    
    # File selector
    file_list = sorted(file_structure.keys())
    selected_file = st.selectbox(
        "Select file to preview",
        file_list,
        help="Choose a file to view its contents"
    )
    
    if selected_file:
        content = file_structure[selected_file]
        
        # Determine language for syntax highlighting
        if selected_file.endswith('.ts'):
            language = "typescript"
        elif selected_file.endswith('.json'):
            language = "json"
        elif selected_file.endswith('.md'):
            language = "markdown"
        else:
            language = "text"
        
        st.code(content, language=language, line_numbers=True)
    
    # Download Section
    st.markdown("---")
    st.markdown("### 📥 Download SDK")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Download button
        download_filename = f"{api_name.lower().replace(' ', '-')}-sdk.zip"
        
        st.download_button(
            label="⬇️ Download ZIP",
            data=zip_bytes,
            file_name=download_filename,
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown(f"""
**Next Steps:**
1. Extract the ZIP file
2. Run `npm install` to install dependencies
3. Run `npm run build` to compile TypeScript
4. Import and use in your project!
        """)
    
    # Usage Instructions
    with st.expander("📖 Usage Instructions"):
        st.markdown(f"""
### Building the SDK

```bash
# Extract the ZIP
unzip {download_filename}
cd {api_name.lower().replace(' ', '-')}-sdk

# Install dependencies
npm install

# Build TypeScript
npm run build
```

### Using the SDK

```typescript
import {{ {api_name.replace(' ', '')} }} from './{api_name.lower().replace(' ', '-')}-sdk';

const client = new {api_name.replace(' ', '')}({{
  apiKey: 'your-api-key',
  baseURL: 'https://api.example.com/v1'
}});

// Use the client
const result = await client.someMethod();
```

### Testing

```bash
# Run the example
npm run example
```
        """)
    
    # Start Over Button
    st.markdown("---")
    
    if st.button("🔄 Start Over", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
