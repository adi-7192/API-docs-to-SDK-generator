"""API SDK Generator - Main Streamlit Application."""

import streamlit as st
from pathlib import Path

# Import UI components
from src.ui import (
    render_step1_input_selection,
    render_documentation_analysis,
    render_analysis_error,
    render_step2_llm_config,
    render_cost_estimation,
    render_step3_review_edit,
    render_extraction_warnings,
    render_step4_sdk_config,
    render_step5_preview_download,
)
from src.generators import TemplateEngine, bundle_to_zip, assemble_client_class, format_code
from src.models import APISpecification

# Page configuration
st.set_page_config(
    page_title="API SDK Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .step-indicator {
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .step-active {
        background: #667eea;
        color: white;
    }
    .step-complete {
        background: #48bb78;
        color: white;
    }
    .step-pending {
        background: #e2e8f0;
        color: #718096;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

if 'documentation_text' not in st.session_state:
    st.session_state.documentation_text = ""

if 'input_source' not in st.session_state:
    st.session_state.input_source = ""

if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = None

if 'api_spec' not in st.session_state:
    st.session_state.api_spec = None

if 'sdk_config' not in st.session_state:
    st.session_state.sdk_config = None

if 'file_structure' not in st.session_state:
    st.session_state.file_structure = None

if 'zip_bytes' not in st.session_state:
    st.session_state.zip_bytes = None

if 'documentation_analysis' not in st.session_state:
    st.session_state.documentation_analysis = None

if 'skip_analysis' not in st.session_state:
    st.session_state.skip_analysis = False


def render_progress_sidebar():
    """Render progress sidebar with step indicators."""
    with st.sidebar:
        st.markdown('<h1 class="main-header">🚀 API SDK Generator</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        steps = [
            ("1️⃣", "Input Selection"),
            ("🔍", "Documentation Analysis"),
            ("2️⃣", "LLM Configuration"),
            ("3️⃣", "Review & Edit"),
            ("4️⃣", "SDK Configuration"),
            ("5️⃣", "Preview & Download"),
        ]
        
        for idx, (icon, name) in enumerate(steps, 1):
            if idx < st.session_state.current_step:
                st.markdown(f'<div class="step-indicator step-complete">{icon} {name} ✓</div>', unsafe_allow_html=True)
            elif idx == st.session_state.current_step:
                st.markdown(f'<div class="step-indicator step-active">{icon} {name}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-indicator step-pending">{icon} {name}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        
        if st.session_state.current_step == 1:
            st.info("📄 Start by providing your API documentation via URL, file upload, or text paste.")
        elif st.session_state.current_step == 2:
            st.info("🔑 Your API key is stored only in your session and never saved.")
        elif st.session_state.current_step == 3:
            st.info("✏️ Review the extracted API spec and edit any incorrect information.")
        elif st.session_state.current_step == 4:
            st.info("⚙️ Customize your SDK with retry logic, rate limiting, and more.")
        elif st.session_state.current_step == 5:
            st.info("🎉 Your SDK is ready! Preview the code and download the ZIP file.")


def main():
    """Main application entry point."""
    
    # Render sidebar
    render_progress_sidebar()
    
    # Hero section
    st.markdown('<h1 class="main-header">🚀 API SDK Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Transform unstructured API documentation into production-ready TypeScript SDKs in under 60 seconds</p>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Step 1: Input Selection
    if st.session_state.current_step == 1:
        has_input, documentation_text, input_source = render_step1_input_selection()
        
        # Update session state if new input is provided
        if has_input:
            st.session_state.documentation_text = documentation_text
            st.session_state.input_source = input_source
        
        # Show Next button if we have documentation (either new or from session)
        if st.session_state.documentation_text:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 3])
            with col2:
                if st.button("➡️ Next: Analyze Documentation", type="primary", use_container_width=True):
                    st.session_state.current_step = 1.5
                    st.rerun()
    
    # Step 1.5: Documentation Analysis
    elif st.session_state.current_step == 1.5:
        st.info(f"📄 **Input Source:** {st.session_state.input_source}")
        
        # Run analysis if not already done
        if not st.session_state.documentation_analysis:
            # Need to get LLM provider for analysis
            # For now, we'll ask user to configure LLM first, then analyze
            # OR we can use a default provider with user's key
            
            st.markdown("### 🔍 Analyzing Documentation Structure...")
            st.markdown("To analyze your documentation, we need an LLM provider.")
            
            # Quick LLM selection for analysis
            provider_choice = st.radio(
                "Select LLM Provider for Analysis",
                ["OpenAI (GPT-4o-mini)", "Google Gemini (Flash)"],
                help="Analysis uses cheaper, faster models (~$0.005 per analysis)"
            )
            
            api_key = st.text_input(
                "API Key",
                type="password",
                help="Your API key (not stored, used only for this session)"
            )
            
            if api_key:
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("⬅️ Back", use_container_width=True):
                        st.session_state.current_step = 1
                        st.rerun()
                
                with col2:
                    if st.button("🔍 Analyze", type="primary", use_container_width=True):
                        # Create temporary provider for analysis
                        with st.spinner("🔍 Analyzing documentation structure..."):
                            try:
                                if "OpenAI" in provider_choice:
                                    from src.llm import OpenAIProvider
                                    temp_provider = OpenAIProvider(api_key)
                                else:
                                    from src.llm import GeminiProvider
                                    temp_provider = GeminiProvider(api_key)
                                
                                # Run analysis
                                success, analysis, error = temp_provider.analyze_documentation(
                                    st.session_state.documentation_text
                                )
                                
                                if success:
                                    st.session_state.documentation_analysis = analysis
                                    # Store provider for later use
                                    st.session_state.llm_provider = temp_provider
                                    st.rerun()
                                else:
                                    st.error(f"❌ Analysis failed: {error}")
                                    st.warning("⚠️ Proceeding without analysis...")
                                    st.session_state.skip_analysis = True
                                    st.session_state.current_step = 2
                                    st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
        else:
            # Display analysis results
            should_proceed, action = render_documentation_analysis(
                st.session_state.documentation_analysis
            )
            
            if should_proceed:
                if action == "continue":
                    # Proceed to LLM configuration (or skip if provider already set)
                    if st.session_state.llm_provider:
                        st.session_state.current_step = 2
                    else:
                        st.session_state.current_step = 2
                    st.rerun()
                elif action == "add_more":
                    # Go back to input selection
                    st.session_state.documentation_analysis = None
                    st.session_state.current_step = 1
                    st.rerun()
                elif action == "retry":
                    # Clear analysis and retry
                    st.session_state.documentation_analysis = None
                    st.rerun()
    
    # Step 2: LLM Configuration
    elif st.session_state.current_step == 2:
        st.info(f"📄 **Input Source:** {st.session_state.input_source}")
        
        is_configured, llm_provider, config = render_step2_llm_config()
        
        if is_configured:
            st.session_state.llm_provider = llm_provider
            
            # Show cost estimation
            render_cost_estimation(st.session_state.documentation_text, llm_provider)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("⬅️ Back", use_container_width=True):
                    st.session_state.current_step = 1.5
                    st.rerun()
            with col2:
                if st.button("➡️ Next: Extract API Spec", type="primary", use_container_width=True):
                    # Extract API specification
                    with st.spinner("🤖 Extracting API specification with LLM..."):
                        success, api_spec, error = llm_provider.extract_api_specification(
                            st.session_state.documentation_text
                        )
                        
                        if success:
                            st.session_state.api_spec = api_spec
                            # Show success message with endpoint count
                            st.success(f"✅ Successfully extracted {len(api_spec.endpoints)} endpoint(s)!")
                            st.session_state.current_step = 3
                            st.rerun()
                        else:
                            st.error(f"❌ Extraction failed: {error}")
    
    # Step 3: Review & Edit
    elif st.session_state.current_step == 3:
        st.info(f"📄 **Input Source:** {st.session_state.input_source}")
        
        api_spec = render_step3_review_edit(st.session_state.api_spec)
        
        if api_spec:
            render_extraction_warnings(api_spec)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("⬅️ Back", use_container_width=True):
                    st.session_state.current_step = 2
                    st.rerun()
            with col2:
                if st.button("➡️ Next: Configure SDK", type="primary", use_container_width=True):
                    st.session_state.current_step = 4
                    st.rerun()
    
    # Step 4: SDK Configuration
    elif st.session_state.current_step == 4:
        st.info(f"🔧 **API:** {st.session_state.api_spec.api_name} ({len(st.session_state.api_spec.endpoints)} endpoints)")
        
        sdk_config = render_step4_sdk_config()
        
        if sdk_config:
            st.session_state.sdk_config = sdk_config
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("⬅️ Back", use_container_width=True):
                    st.session_state.current_step = 3
                    st.rerun()
            with col2:
                if st.button("🚀 Generate SDK", type="primary", use_container_width=True):
                    # Generate SDK
                    with st.spinner("⚙️ Generating SDK..."):
                        try:
                            # Generate endpoint methods and types using LLM
                            endpoint_methods_list = []
                            for endpoint in st.session_state.api_spec.endpoints:
                                success, method_code, error = st.session_state.llm_provider.generate_endpoint_method(
                                    endpoint,
                                    st.session_state.api_spec
                                )
                                if success:
                                    endpoint_methods_list.append(method_code)
                            
                            endpoint_methods = "\n\n".join(endpoint_methods_list)
                            
                            # Generate type definitions
                            success, types_code, error = st.session_state.llm_provider.generate_type_definitions(
                                st.session_state.api_spec
                            )
                            
                            # Render templates
                            engine = TemplateEngine()
                            base_files = engine.render_all_base_files(
                                st.session_state.api_spec,
                                st.session_state.sdk_config
                            )
                            
                            # Render client with endpoint methods
                            client_code = engine.render_client(
                                st.session_state.api_spec,
                                st.session_state.sdk_config,
                                endpoint_methods
                            )
                            
                            # Render index
                            index_code = engine.render_index(
                                st.session_state.api_spec,
                                st.session_state.sdk_config
                            )
                            
                            # Render README
                            readme_code = engine.render_readme(
                                st.session_state.api_spec,
                                st.session_state.sdk_config
                            )
                            
                            # Assemble all files
                            file_structure = {
                                **base_files,
                                "src/client.ts": format_code(client_code),
                                "src/types.ts": format_code(types_code) if success else "// Types generation failed",
                                "src/index.ts": format_code(index_code),
                                "README.md": readme_code,
                            }
                            
                            # Bundle to ZIP
                            zip_bytes = bundle_to_zip(file_structure, st.session_state.api_spec.api_name)
                            
                            st.session_state.file_structure = file_structure
                            st.session_state.zip_bytes = zip_bytes
                            st.session_state.current_step = 5
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Generation failed: {str(e)}")
    
    # Step 5: Preview & Download
    elif st.session_state.current_step == 5:
        render_step5_preview_download(
            st.session_state.file_structure,
            st.session_state.zip_bytes,
            st.session_state.api_spec.api_name
        )


if __name__ == "__main__":
    main()
