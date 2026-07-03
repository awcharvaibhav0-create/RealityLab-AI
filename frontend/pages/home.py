import streamlit as st
from frontend.components.metric_card import render_metric_card


def render():
    """
    Render the Home page.
    """
    st.markdown("<h1>Welcome to RealityLab AI</h1>", unsafe_allow_html=True)
    st.markdown("### Your Premier Business Analysis Platform")

    st.write(
        "RealityLab AI helps you build robust scenarios, analyze risks, and simulate outcomes."
    )

    col1, col2, col3 = st.columns(3)

    from frontend.components.action_card import render_action_card

    with col1:
        st.markdown(
            render_metric_card("📈", "Analyses Completed", "124"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_metric_card("⚡", "Active Scenarios", "8"), unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            render_metric_card("🛡️", "Risk Mitigation", "High"), unsafe_allow_html=True
        )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        render_action_card(
            "Start New Analysis",
            "➕",
            page_target="new_analysis",
            key="home_new",
            is_primary=True,
        )
    with col2:
        render_action_card(
            "View Dashboard", "📊", page_target="dashboard", key="home_dash"
        )
