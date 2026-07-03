import streamlit as st

def render_error_state(title: str, exception: Exception = None, message: str = None):
    """Render a premium error state card instead of a raw traceback."""
    st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.05); padding: 1.5rem; margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <h3 style="margin: 0; font-size: 1.2rem; color: #f87171;">{title}</h3>
            </div>
            <p style="color: #cbd5e1; margin-bottom: {'1rem' if exception else '0'}; font-size: 0.95rem;">
                {message or "An unexpected error occurred during processing."}
            </p>
            {f'<div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 0.85rem; color: #94a3b8; overflow-x: auto;">{str(exception)}</div>' if exception else ''}
        </div>
    """, unsafe_allow_html=True)
