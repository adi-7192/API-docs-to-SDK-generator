"""Streamlit UI components for Step 3: Review & Edit."""

import streamlit as st
from typing import Optional
from ..models import APISpecification, Endpoint
from ..llm import calculate_api_confidence, get_confidence_level, get_confidence_color


def render_step3_review_edit(api_spec: Optional[APISpecification]) -> Optional[APISpecification]:
    """
    Render Step 3: Review & Edit UI.
    
    Args:
        api_spec: Extracted API specification
        
    Returns:
        Edited API specification or None
    """
    st.markdown("## ✏️ Step 3: Review & Edit API Specification")
    
    if api_spec is None:
        st.info("⏳ Waiting for API specification extraction...")
        return None
    
    # Calculate confidence score
    confidence = calculate_api_confidence(api_spec)
    confidence_level = get_confidence_level(confidence)
    confidence_color = get_confidence_color(confidence)
    
    # Show overall confidence
    st.markdown("### 📊 Extraction Quality")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.metric("Confidence Score", f"{confidence:.1%}")
    
    with col2:
        if confidence_color == "green":
            st.success(confidence_level)
        elif confidence_color == "yellow":
            st.warning(confidence_level)
        else:
            st.error(confidence_level)
    
    with col3:
        st.metric("Endpoints Found", len(api_spec.endpoints))
    
    # API Metadata
    st.markdown("---")
    st.markdown("### 🔧 API Metadata")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_name = st.text_input("API Name", value=api_spec.api_name)
        base_url = st.text_input("Base URL", value=str(api_spec.base_url))
    
    with col2:
        auth_type = st.selectbox(
            "Authentication Type",
            ["api_key", "bearer", "oauth2", "basic", "none"],
            index=["api_key", "bearer", "oauth2", "basic", "none"].index(api_spec.auth_type.value)
        )
    
    # Endpoints
    st.markdown("---")
    st.markdown("### 📍 Endpoints")
    
    if len(api_spec.endpoints) == 0:
        st.warning("⚠️ No endpoints were extracted. You can add them manually below.")
    else:
        # Display endpoints in expandable sections
        for idx, endpoint in enumerate(api_spec.endpoints):
            render_endpoint_editor(endpoint, idx)
    
    # Add new endpoint button
    if st.button("➕ Add New Endpoint"):
        st.info("🚧 Endpoint editor coming soon! For now, please edit the extracted endpoints.")
    
    # Update API spec with edited values
    # (In a real implementation, we'd track changes and update the model)
    # For now, return the original spec
    return api_spec


def render_endpoint_editor(endpoint: Endpoint, index: int):
    """Render editor for a single endpoint."""
    # Calculate endpoint confidence
    from ..llm import calculate_endpoint_confidence
    confidence = calculate_endpoint_confidence(endpoint)
    
    # Color code based on confidence
    if confidence >= 0.9:
        icon = "✅"
    elif confidence >= 0.7:
        icon = "⚠️"
    else:
        icon = "❌"
    
    with st.expander(f"{icon} {endpoint.method.value} {endpoint.path} ({confidence:.0%})"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input(f"Path #{index}", value=endpoint.path, key=f"path_{index}")
            st.selectbox(
                f"Method #{index}",
                ["GET", "POST", "PUT", "DELETE", "PATCH"],
                index=["GET", "POST", "PUT", "DELETE", "PATCH"].index(endpoint.method.value),
                key=f"method_{index}"
            )
        
        with col2:
            st.text_area(
                f"Description #{index}",
                value=endpoint.description,
                height=100,
                key=f"desc_{index}"
            )
        
        # Parameters
        if endpoint.parameters:
            st.markdown("**Parameters:**")
            for param_idx, param in enumerate(endpoint.parameters):
                st.text(f"• {param.name} ({param.type.value}, {param.location.value})" + 
                       (" - required" if param.required else " - optional"))
        else:
            st.caption("No parameters")
        
        # Response schema
        if endpoint.response_schema:
            st.markdown("**Response Type:**")
            st.code(endpoint.response_schema.type.value, language="text")


def render_extraction_warnings(api_spec: APISpecification):
    """Render warnings about extraction quality."""
    warnings = []
    
    # Check for low confidence endpoints
    from ..llm import calculate_endpoint_confidence
    
    low_confidence_endpoints = [
        e for e in api_spec.endpoints
        if calculate_endpoint_confidence(e) < 0.7
    ]
    
    if low_confidence_endpoints:
        warnings.append(
            f"⚠️ {len(low_confidence_endpoints)} endpoint(s) have low confidence scores. "
            "Please review and edit them carefully."
        )
    
    # Check for missing descriptions
    missing_desc = [e for e in api_spec.endpoints if len(e.description) < 20]
    if missing_desc:
        warnings.append(
            f"⚠️ {len(missing_desc)} endpoint(s) have very short descriptions."
        )
    
    # Check for endpoints without parameters
    no_params = [e for e in api_spec.endpoints if not e.parameters]
    if no_params:
        warnings.append(
            f"💡 {len(no_params)} endpoint(s) have no parameters. "
            "This might be correct, but please verify."
        )
    
    # Check for suspiciously low endpoint count
    # If we have very few endpoints, it might indicate incomplete extraction
    if len(api_spec.endpoints) <= 2:
        warnings.append(
            f"⚠️ Only {len(api_spec.endpoints)} endpoint(s) were extracted. "
            "If your API has more endpoints, the extraction may be incomplete. "
            "Try re-running the extraction or check your documentation."
        )

    
    if warnings:
        st.markdown("---")
        st.markdown("### ⚠️ Extraction Warnings")
        for warning in warnings:
            st.warning(warning)
