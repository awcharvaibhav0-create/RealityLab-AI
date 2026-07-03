import streamlit as st

def render_loading_state(message: str = "Processing..."):
    """Render a premium loading state with skeleton cards."""
    with st.container():
        st.markdown(f"""
            <div class="metric-card" style="text-align: center; padding: 2rem; margin: 1rem 0;">
                <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                    <div style="width: 40px; height: 40px; border: 4px solid rgba(255, 255, 255, 0.1); border-left-color: #60a5fa; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                </div>
                <h3 style="margin-top: 0; font-size: 1.2rem; color: #f8fafc;">{message}</h3>
                
                <style>
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                .skeleton {{
                    background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%);
                    background-size: 200% 100%;
                    animation: skeleton-loading 1.5s infinite;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                }}
                @keyframes skeleton-loading {{
                    0% {{ background-position: 200% 0; }}
                    100% {{ background-position: -200% 0; }}
                }}
                </style>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; align-items: center; margin-top: 1.5rem;">
                    <div class="skeleton" style="width: 80%; height: 20px;"></div>
                    <div class="skeleton" style="width: 60%; height: 20px;"></div>
                    <div class="skeleton" style="width: 40%; height: 20px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
