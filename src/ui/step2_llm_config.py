"""Streamlit UI components for Step 2: LLM Configuration."""

import streamlit as st
from typing import Tuple, Optional, Dict


def render_step2_llm_config() -> Tuple[bool, Optional, Dict]:
    """
    Render Step 2: LLM Configuration UI.
    
    Returns:
        Tuple of (is_configured, llm_provider, config_dict)
    """
    st.markdown("## 🤖 Step 2: Configure LLM")
    st.markdown("Configure the AI model that will extract API specifications:")
    
    # Provider selection
    st.markdown("### Provider")
    provider_choice = st.selectbox(
        "LLM Provider",
        ["OpenAI (GPT-4-turbo)", "Google Gemini (Gemini 1.5 Pro)"],
        help="Select which AI provider to use for extraction"
    )
    
    # Determine which provider was selected
    is_openai = "OpenAI" in provider_choice
    provider_name = "OpenAI" if is_openai else "Google Gemini"
    
    # API Key input
    st.markdown("### API Key")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if is_openai:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-...",
                help="Your OpenAI API key. Get one at https://platform.openai.com/api-keys"
            )
        else:
            api_key = st.text_input(
                "Google Gemini API Key",
                type="password",
                placeholder="AIza...",
                help="Your Google API key. Get one at https://aistudio.google.com/app/apikey"
            )
    
    with col2:
        validate_button = st.button("🔍 Validate", use_container_width=True)
    
    # Validation
    is_valid = False
    if validate_button and api_key:
        with st.spinner(f"Validating {provider_name} API key..."):
            try:
                if is_openai:
                    from ..llm import OpenAIProvider
                    provider_instance = OpenAIProvider(api_key)
                else:
                    from ..llm import GeminiProvider
                    provider_instance = GeminiProvider(api_key)
                
                is_valid, message = provider_instance.validate_api_key()
                
                if is_valid:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        st.markdown("#### Model Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.1,
                help="Lower = more deterministic, Higher = more creative. Recommended: 0.2 for extraction"
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="Maximum tokens for LLM response"
            )
        
        with col2:
            timeout = st.slider(
                "Timeout (seconds)",
                min_value=30,
                max_value=300,
                value=120,
                step=30,
                help="Request timeout in seconds"
            )
    
    # Configuration summary
    config = {
        "model": "gpt-4-turbo",
        "temperature": temperature,
        "max_tokens": max_tokens,
        "timeout": timeout,
    }
    
    # Create provider if API key is provided
    provider_instance = None
    if api_key:
        try:
            if is_openai:
                from ..llm import OpenAIProvider
                provider_instance = OpenAIProvider(api_key, config)
            else:
                from ..llm import GeminiProvider
                provider_instance = GeminiProvider(api_key, config)
            is_configured = True
        except Exception as e:
            st.error(f"Error creating provider: {str(e)}")
            is_configured = False
    else:
        is_configured = False
        st.info(f"💡 Please provide your {provider_name} API key to continue")
    
    return is_configured, provider_instance, config


def render_cost_estimation(documentation_text: str, provider: OpenAIProvider):
    """Render cost estimation for processing."""
    st.markdown("---")
    st.markdown("### 💰 Cost Estimation")
    
    estimated_cost = provider.estimate_cost(documentation_text)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Extraction", f"${estimated_cost:.4f}")
    
    with col2:
        # Estimate for code generation (roughly 2x extraction)
        generation_cost = estimated_cost * 2
        st.metric("Code Generation", f"${generation_cost:.4f}")
    
    with col3:
        total_cost = estimated_cost + generation_cost
        st.metric("Total Estimated", f"${total_cost:.4f}")
    
    st.caption("💡 Actual costs may vary based on API response length")
