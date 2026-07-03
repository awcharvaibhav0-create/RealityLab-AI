import streamlit as st


def init_session():
    defaults = {
        "current_page": "home",
        "user_profile": {},
        "current_analysis_id": None,
        "business_profile_data": None,
        "scenarios": [],
        "analysis_results": None,
        "notifications": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
