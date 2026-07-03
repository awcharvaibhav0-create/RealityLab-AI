import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from frontend.components.metric_card import render_metric_card

API_URL = os.environ.get("API_URL", "http://localhost:8000")


def fetch_data(endpoint, default_val):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=2)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return default_val


from streamlit_autorefresh import st_autorefresh

def render():
    st_autorefresh(interval=5000, key="dashboard_refresh")

    # Hero Section
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">RealityLab AI</h1>
            <p style="font-size: 1.2rem; color: #94a3b8;">Enterprise Multi-Agent Business Intelligence Platform</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Fetch Data
    metrics = fetch_data(
        "/api/v1/dashboard/metrics",
        {
            "analyses_completed": 0,
            "active_scenarios": 0,
            "average_processing_time": "0s",
            "success_rate": "0%",
            "risk_level": "Unknown",
        },
    )

    # Top Metrics Row
    st.markdown("### Platform Metrics")
    m1, m2, m3, m4, m5 = st.columns(5)

    val_completed = str(metrics.get("analyses_completed", 0))
    val_scenarios = str(metrics.get("active_scenarios", 0))
    val_time = str(metrics.get("average_processing_time", "--"))
    val_success = str(metrics.get("success_rate", "--"))
    val_risk = str(metrics.get("risk_level", "Unknown"))

    with m1:
        st.markdown(
            render_metric_card("📊", "Analyses Completed", val_completed),
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            render_metric_card("📈", "Active Scenarios", val_scenarios),
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            render_metric_card("⏱", "Average Processing", val_time),
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            render_metric_card("✅", "Success Rate", val_success),
            unsafe_allow_html=True,
        )
    with m5:
        st.markdown(
            render_metric_card("🛡", "System Risk Level", val_risk),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    from frontend.components.action_card import render_action_card

    # Quick Actions
    st.markdown("### Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        render_action_card(
            "Start New Analysis", "➕", page_target="new_analysis", key="qa_new"
        )
    with qa2:
        render_action_card(
            "View Business Profile",
            "🏢",
            page_target="business_profile",
            key="qa_profile",
        )
    with qa3:
        render_action_card(
            "Generate Report", "📄", page_target="reports", key="qa_report"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Hub
    st.markdown("### Navigation Hub")

    # Grid 4x3
    nav_items = [
        {
            "name": "Scenario Builder",
            "icon": "🧪",
            "page": "scenario_builder",
            "desc": "Model different business outcomes",
        },
        {
            "name": "Comparison",
            "icon": "⚖️",
            "page": "comparison",
            "desc": "Compare scenarios side-by-side",
        },
        {
            "name": "Results",
            "icon": "✅",
            "page": "results",
            "desc": "View analysis recommendations",
        },
        {
            "name": "Reports",
            "icon": "📄",
            "page": "reports",
            "desc": "Generate PDF and CSV reports",
        },
        {
            "name": "History",
            "icon": "🕰️",
            "page": "history",
            "desc": "Review past analyses",
        },
        {
            "name": "Explainability",
            "icon": "🔍",
            "page": "explainability",
            "desc": "Understand AI decision making",
        },
        {
            "name": "Knowledge Base",
            "icon": "📚",
            "page": "knowledge",
            "desc": "Manage business context",
        },
        {
            "name": "Live Monitor",
            "icon": "📈",
            "page": "live_monitor",
            "desc": "Real-time system monitoring",
        },
        {
            "name": "Trust Center",
            "icon": "🛡️",
            "page": "trust_center",
            "desc": "Data privacy and security",
        },
        {
            "name": "Settings",
            "icon": "⚙️",
            "page": "settings",
            "desc": "Platform configuration",
        },
        {
            "name": "Developer",
            "icon": "💻",
            "page": "developer",
            "desc": "API access and webhooks",
        },
    ]

    # Display in rows of 4
    for i in range(0, len(nav_items), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(nav_items):
                item = nav_items[i + j]
                with col:
                    render_action_card(
                        title=item["name"],
                        icon=item["icon"],
                        desc=item["desc"],
                        page_target=item["page"],
                        key=f"hub_{item['page']}",
                        is_primary=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard Activity & Charts
    activity = fetch_data(
        "/api/v1/dashboard/activity",
        {"recent_analyses": [], "recent_scenarios": [], "recent_reports": []},
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### Activity & Charts")
        charts = fetch_data("/api/v1/dashboard/charts", {})

        has_any_data = any(
            [
                charts.get("analysis_count_over_time"),
                charts.get("risk_distribution"),
                charts.get("success_rate"),
                charts.get("scenario_categories"),
                charts.get("agent_execution"),
            ]
        )

        if not has_any_data:
            st.markdown(
                """
            <div class="metric-card" style="text-align: center; padding: 3rem;">
                <h3 style="margin-top: 0; font-size: 1.5rem;">📈 Analytics</h3>
                <p style="font-size: 1.1rem; color: #f8fafc; margin-bottom: 0.5rem; font-weight: 600;">No analyses have been performed yet.</p>
                <p style="color: #94a3b8;">Run your first analysis to automatically generate<br>charts, reports and performance metrics.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            if charts.get("analysis_count_over_time"):
                st.markdown("#### Analysis Over Time")
                df_time = pd.DataFrame(charts["analysis_count_over_time"])
                if not df_time.empty and "date" in df_time.columns:
                    df_time.set_index("date", inplace=True)
                    st.line_chart(df_time)

            if charts.get("risk_distribution"):
                st.markdown("#### Risk Distribution")
                df_risk = pd.DataFrame(charts["risk_distribution"])
                if not df_risk.empty and "level" in df_risk.columns:
                    df_risk.set_index("level", inplace=True)
                    st.bar_chart(df_risk)

            if charts.get("success_rate"):
                st.markdown("#### Success Rate")
                df_success = pd.DataFrame(charts["success_rate"])
                if not df_success.empty and "date" in df_success.columns:
                    df_success.set_index("date", inplace=True)
                    st.bar_chart(df_success)

            if charts.get("scenario_categories"):
                st.markdown("#### Scenario Categories")
                df_cat = pd.DataFrame(charts["scenario_categories"])
                if not df_cat.empty and "category" in df_cat.columns:
                    df_cat.set_index("category", inplace=True)
                    st.bar_chart(df_cat)

            if charts.get("agent_execution"):
                st.markdown("#### Agent Execution Stats")
                df_agent = pd.DataFrame(charts["agent_execution"])
                if not df_agent.empty and "agent" in df_agent.columns:
                    df_agent.set_index("agent", inplace=True)
                    st.bar_chart(df_agent)

    with c2:
        st.markdown("### Recent Activity")
        if not activity.get("recent_analyses"):
            st.markdown(
                """
            <div class="metric-card" style="padding: 1.5rem; text-align: center; min-height: 100px;">
                <p style="margin: 0; color: #94a3b8;">No analyses have been performed yet.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            for act in activity["recent_analyses"]:
                st.markdown(
                    f"""
                    <div style="background-color: #1e293b; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border: 1px solid #334155;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <strong>{act['business_name']}</strong>
                            <span style="color: {'#4ade80' if act['status'] == 'completed' else '#fbbf24'};">{act['status'].title()}</span>
                        </div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">
                            Scenarios: {act.get('scenario_count', 0)}<br>
                            Risk: {act['risk_level']}<br>
                            Time: {act['processing_time']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### Recent Reports")
        if not activity.get("recent_reports"):
            st.markdown(
                """
            <div class="metric-card" style="padding: 1.5rem; text-align: center; min-height: 100px;">
                <p style="margin: 0; color: #94a3b8;">No reports generated.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            for rep in activity["recent_reports"]:
                st.markdown(f"**Report:** `{rep['id'][:8]}`")

    st.markdown("<hr>", unsafe_allow_html=True)

    # System Health
    st.markdown("### System Health")
    health = fetch_data(
        "/api/v1/health",
        {
            "fastapi": "error",
            "sqlite": "error",
            "docker": "offline",
            "streamlit": "error",
        },
    )
    system = fetch_data(
        "/api/v1/system",
        {"agent_coordinator": "Offline", "knowledge_base_status": "offline"},
    )

    def render_health_card(label, val):
        val_lower = str(val).lower()
        if val_lower in ["healthy", "online", "running", "connected", "active"]:
            status_html = "🟢 <span class='status-green'>Healthy</span>"
        elif val_lower in ["warning"]:
            status_html = "🟡 <span class='status-yellow'>Warning</span>"
        else:
            status_html = "🔴 <span class='status-red'>Offline</span>"

        st.markdown(
            f"""
        <div class="metric-card" style="min-height: 90px; padding: 1.25rem;">
            <div class="metric-label" style="font-size: 0.85rem; margin-bottom: 0.2rem;">{label}</div>
            <div style="font-size: 1.1rem; font-weight: 600;">{status_html}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    hc1, hc2, hc3 = st.columns(3)
    with hc1:
        render_health_card("Docker", health.get("docker", "offline"))
        render_health_card("SQLite", health.get("sqlite", "offline"))
    with hc2:
        render_health_card("FastAPI", health.get("fastapi", "offline"))
        render_health_card("Streamlit", health.get("streamlit", "offline"))
    with hc3:
        render_health_card("Coordinator", system.get("agent_coordinator", "offline"))
        render_health_card(
            "Knowledge Base", system.get("knowledge_base_status", "offline")
        )
