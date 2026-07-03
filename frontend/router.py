import streamlit as st
from frontend.pages import (
    home,
    new_analysis,
    dashboard,
    business_profile,
    scenario_builder,
    results,
    comparison,
    history,
    reports,
    settings,
    developer,
    knowledge,
    live_monitor,
    trust_center,
    explainability,
)
from frontend.navigation import render_sidebar_nav


def route_page():
    render_sidebar_nav()
    page = st.session_state.get("current_page", "home")

    routes = {
        "home": home.render,
        "new_analysis": new_analysis.render,
        "dashboard": dashboard.render,
        "business_profile": business_profile.render,
        "scenario_builder": scenario_builder.render,
        "results": results.render,
        "comparison": comparison.render,
        "history": history.render,
        "reports": reports.render,
        "settings": settings.render,
        "developer": developer.render,
        "knowledge": knowledge.render,
        "live_monitor": live_monitor.render,
        "trust_center": trust_center.render,
        "explainability": explainability.render,
    }

    if page in routes:
        routes[page]()
    else:
        st.error(f"Page {page} not found.")
