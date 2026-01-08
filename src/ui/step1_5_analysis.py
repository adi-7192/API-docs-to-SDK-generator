"""Streamlit UI components for Step 1.5: Documentation Analysis."""

import streamlit as st
from typing import Tuple
from ..models.documentation_analysis import DocumentationAnalysis


def render_documentation_analysis(
    analysis: DocumentationAnalysis
) -> Tuple[bool, str]:
    """
    Render documentation analysis results.
    
    Args:
        analysis: DocumentationAnalysis object with results
        
    Returns:
        Tuple of (should_proceed, action: "continue" | "add_more" | "retry")
    """
    st.markdown("## 📊 Documentation Analysis")
    st.markdown("---")
    
    # Document type badge
    doc_type_badges = {
        "api_reference": ("🟢", "API Reference", "success"),
        "guide": ("🔵", "Guide/Tutorial", "info"),
        "setup_instructions": ("🟡", "Setup Instructions", "warning"),
        "mixed": ("🟣", "Mixed Content", "info")
    }
    
    icon, label, badge_type = doc_type_badges.get(
        analysis.document_type,
        ("⚪", "Unknown", "info")
    )
    
    st.markdown(f"### {icon} Document Type: {label}")
    
    # Findings section
    st.markdown("---")
    st.markdown("### 📋 Findings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Endpoints Found", analysis.endpoints_found["count"])
    
    with col2:
        if analysis.is_complete_api:
            st.success("✅ Complete API")
        else:
            st.warning("⚠️ Partial Documentation")
    
    with col3:
        if analysis.api_name:
            st.info(f"🔍 {analysis.api_name}")
        else:
            st.info("🔍 API Name Unknown")
    
    if analysis.base_url:
        st.markdown(f"**Base URL:** `{analysis.base_url}`")
    
    # Endpoints list
    if analysis.endpoints_found["count"] > 0:
        st.markdown("---")
        st.markdown("### 📍 Endpoints Extracted")
        
        endpoints_list = analysis.endpoints_found.get("list", [])
        if endpoints_list:
            for ep in endpoints_list:
                method = ep.get("method", "GET")
                path = ep.get("path", "/unknown")
                desc = ep.get("description", "No description")
                
                # Color code by method
                method_colors = {
                    "GET": "🟢",
                    "POST": "🔵",
                    "PUT": "🟡",
                    "DELETE": "🔴",
                    "PATCH": "🟣"
                }
                icon = method_colors.get(method, "⚪")
                
                st.markdown(f"{icon} **{method}** `{path}` - {desc}")
        else:
            st.caption(f"{analysis.endpoints_found['count']} endpoint(s) found")
    
    # Additional endpoints available
    if analysis.navigation_detected.has_more_endpoints:
        st.markdown("---")
        st.markdown("### 📚 Additional Endpoints Available")
        
        if analysis.navigation_detected.other_sections:
            st.markdown("The documentation site contains these other API sections:")
            for section in analysis.navigation_detected.other_sections:
                st.markdown(f"• {section}")
        
        if analysis.navigation_detected.reference_urls:
            st.markdown("**Suggested URLs:**")
            for url in analysis.navigation_detected.reference_urls:
                st.code(url, language="text")
    
    # User message
    st.markdown("---")
    st.markdown("### 💡 Analysis Summary")
    st.info(analysis.user_message)
    
    # Recommendations
    if analysis.recommendations:
        st.markdown("### 🎯 Recommendations")
        for idx, rec in enumerate(analysis.recommendations, 1):
            st.markdown(f"{idx}. {rec}")
    
    # Action buttons
    st.markdown("---")
    
    # Determine button layout based on endpoint count
    if analysis.endpoints_found["count"] == 0:
        # No endpoints found - suggest retry or add more
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 Try Suggested URLs", type="primary", use_container_width=True):
                return True, "retry"
        
        with col2:
            if st.button("⬅️ Provide Different URLs", use_container_width=True):
                return True, "add_more"
        
        return False, "none"
    
    elif analysis.endpoints_found["count"] <= 3 and not analysis.is_complete_api:
        # Partial documentation - allow continue or add more
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("✅ Continue with These", type="primary", use_container_width=True):
                return True, "continue"
        
        with col2:
            if st.button("➕ Add More URLs", use_container_width=True):
                return True, "add_more"
        
        return False, "none"
    
    else:
        # Good documentation - proceed
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("➡️ Continue to Extraction", type="primary", use_container_width=True):
                return True, "continue"
        
        with col2:
            if st.button("➕ Add More URLs", use_container_width=True):
                return True, "add_more"
        
        return False, "none"


def render_analysis_error(error_message: str):
    """Render error state when analysis fails."""
    st.warning("⚠️ Documentation Analysis Unavailable")
    st.markdown(
        "Couldn't analyze documentation structure. "
        "Proceeding with direct extraction..."
    )
    
    with st.expander("Error Details"):
        st.error(error_message)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("➡️ Continue Anyway", type="primary", use_container_width=True):
            return True
    
    with col2:
        if st.button("⬅️ Go Back", use_container_width=True):
            return False
    
    return None
