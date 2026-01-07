"""Streamlit UI components for Step 4: SDK Configuration."""

import streamlit as st
from typing import Optional
from ..models import SDKConfig, RetryConfig, RateLimitConfig, License


def render_step4_sdk_config() -> Optional[SDKConfig]:
    """
    Render Step 4: SDK Configuration UI.
    
    Returns:
        SDK configuration or None
    """
    st.markdown("## ⚙️ Step 4: Configure SDK")
    st.markdown("Customize the generated SDK with your preferences:")
    
    # Package Metadata
    st.markdown("### 📦 Package Metadata")
    
    col1, col2 = st.columns(2)
    
    with col1:
        package_name = st.text_input(
            "Package Name",
            value="my-api-sdk",
            help="NPM package name (lowercase, hyphens allowed)"
        )
        
        version = st.text_input(
            "Version",
            value="1.0.0",
            help="Semantic version (e.g., 1.0.0)"
        )
    
    with col2:
        author = st.text_input(
            "Author",
            value="",
            help="Package author (optional)"
        )
        
        license_type = st.selectbox(
            "License",
            ["MIT", "Apache-2.0", "ISC", "BSD-3-Clause"],
            help="Open source license"
        )
    
    # Feature Toggles
    st.markdown("---")
    st.markdown("### ✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        enable_retry = st.checkbox(
            "🔄 Retry Logic",
            value=True,
            help="Automatic retry with exponential backoff"
        )
    
    with col2:
        enable_rate_limit = st.checkbox(
            "⏱️ Rate Limiting",
            value=True,
            help="Token bucket rate limiting"
        )
    
    with col3:
        enable_error_handling = st.checkbox(
            "❌ Error Handling",
            value=True,
            help="Comprehensive error classes"
        )
    
    # Retry Configuration
    retry_config = None
    if enable_retry:
        with st.expander("🔄 Retry Configuration"):
            col1, col2 = st.columns(2)
            
            with col1:
                max_retries = st.slider(
                    "Max Retries",
                    min_value=1,
                    max_value=10,
                    value=3,
                    help="Maximum number of retry attempts"
                )
                
                base_delay = st.slider(
                    "Base Delay (seconds)",
                    min_value=0.5,
                    max_value=5.0,
                    value=1.0,
                    step=0.5,
                    help="Initial delay before first retry"
                )
            
            with col2:
                max_delay = st.slider(
                    "Max Delay (seconds)",
                    min_value=5.0,
                    max_value=60.0,
                    value=30.0,
                    step=5.0,
                    help="Maximum delay between retries"
                )
            
            retry_config = RetryConfig(
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                retryable_status_codes=[408, 429, 500, 502, 503, 504]
            )
    
    # Rate Limit Configuration
    rate_limit_config = None
    if enable_rate_limit:
        with st.expander("⏱️ Rate Limit Configuration"):
            col1, col2 = st.columns(2)
            
            with col1:
                requests_per_second = st.slider(
                    "Requests per Second",
                    min_value=1,
                    max_value=100,
                    value=10,
                    help="Maximum requests per second"
                )
            
            with col2:
                burst_allowance = st.slider(
                    "Burst Allowance",
                    min_value=1,
                    max_value=50,
                    value=5,
                    help="Number of requests that can burst"
                )
            
            rate_limit_config = RateLimitConfig(
                requests_per_second=requests_per_second,
                burst_allowance=burst_allowance,
                algorithm="token_bucket"
            )
    
    # Configuration Preview
    st.markdown("---")
    st.markdown("### 👀 Configuration Preview")
    
    config_summary = f"""
**Package:** `{package_name}@{version}`  
**Author:** {author or "Not specified"}  
**License:** {license_type}  

**Features:**
- Retry Logic: {"✅ Enabled" if enable_retry else "❌ Disabled"}
- Rate Limiting: {"✅ Enabled" if enable_rate_limit else "❌ Disabled"}
- Error Handling: {"✅ Enabled" if enable_error_handling else "❌ Disabled"}
"""
    
    st.markdown(config_summary)
    
    # Create SDK config
    try:
        sdk_config = SDKConfig(
            package_name=package_name,
            version=version,
            author=author if author else None,
            license=License(license_type),
            enable_retry_logic=enable_retry,
            enable_rate_limiting=enable_rate_limit,
            enable_error_handling=enable_error_handling,
            retry_config=retry_config,
            rate_limit_config=rate_limit_config,
        )
        
        return sdk_config
    except Exception as e:
        st.error(f"❌ Configuration error: {str(e)}")
        return None
