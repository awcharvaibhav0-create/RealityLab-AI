import streamlit as st


def get_navigation():
    return [
        {"name": "Home", "icon": "🏠", "page": "home"},
        {"name": "Dashboard", "icon": "📊", "page": "dashboard"},
        {"name": "New Analysis", "icon": "➕", "page": "new_analysis"},
    ]


def render_sidebar_nav():
    with st.sidebar:
        st.title("RealityLab AI")
        st.markdown("---")
        nav_items = get_navigation()
        for item in nav_items:
            # Active page highlighting
            is_active = st.session_state.get("current_page", "home") == item["page"]
            button_type = "primary" if is_active else "secondary"
            if st.button(
                f"{item['icon']} {item['name']}",
                key=f"nav_{item['page']}",
                use_container_width=True,
                type=button_type,
            ):
                st.session_state["current_page"] = item["page"]
                st.rerun()
