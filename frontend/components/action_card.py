import streamlit as st
from frontend.state import set_state


def render_action_card(
    title: str,
    icon: str = "",
    desc: str = "",
    page_target: str = "",
    key: str = "",
    is_primary: bool = False,
):
    button_text = f"{icon} {title}" if not desc else f"{icon} {title}\n\n{desc}"
    if st.button(
        button_text,
        key=key,
        use_container_width=True,
        type="primary" if is_primary else "secondary",
    ):
        if page_target:
            set_state("current_page", page_target)
            st.rerun()
