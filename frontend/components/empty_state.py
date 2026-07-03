import streamlit as st

def render_empty_state(icon: str, title: str, description: str, button_text: str = None, button_key: str = None):
    """Render a premium glassmorphism empty state card."""
    st.markdown(f"""
        <div class="metric-card" style="text-align: center; padding: 3rem; margin: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="margin-top: 0; font-size: 1.5rem; color: #f8fafc;">{title}</h3>
            <p style="font-size: 1.1rem; color: #94a3b8; margin-bottom: 1.5rem;">{description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if button_text and button_key:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button(button_text, key=button_key, use_container_width=True, type="primary")
    return False
