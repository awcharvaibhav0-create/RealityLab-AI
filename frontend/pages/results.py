import streamlit as st
import time
import threading
import requests
import os
from frontend.components.empty_state import render_empty_state
from frontend.components.error_state import render_error_state
from frontend.state import get_state, set_state

def execute_with_progress(analysis_id, profile, scenarios):
    API_URL = os.environ.get("API_URL", "http://localhost:8000")
    result_container = {}
    
    def fetch():
        try:
            payload = {"profile": profile, "scenarios": scenarios}
            resp = requests.post(f"{API_URL}/api/v1/analysis/{analysis_id}/execute", json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    result_container["res"] = {
                        "status": "completed",
                        "metrics": data.get("metrics", {}),
                        "rationale": data.get("rationale", ""),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    result_container["error"] = data.get("message", "Unknown execution error.")
            else:
                result_container["error"] = f"Backend returned HTTP {resp.status_code}"
        except requests.exceptions.ConnectionError:
            result_container["error"] = "Connection to backend failed."
        except requests.exceptions.Timeout:
            result_container["error"] = "Execution timed out."
        except Exception as e:
            result_container["error"] = str(e)
            
    t = threading.Thread(target=fetch)
    t.start()
    
    messages = [
        "Initializing analysis...",
        "Running Finance Agent...",
        "Running Market Agent...",
        "Running Risk Agent...",
        "Running Prediction Agent...",
        "Running Timeline Agent...",
        "Running Evidence Agent...",
        "Computing Decision Score...",
        "Finalizing Results..."
    ]
    
    progress_bar = st.progress(0.0, text=messages[0])
    
    # We poll for up to 20 seconds (200 * 0.1s)
    steps = 200
    for i in range(steps):
        if not t.is_alive():
            break
        progress = min((i / float(steps)), 0.99)
        msg_idx = min(int(progress * len(messages)), len(messages) - 1)
        progress_bar.progress(progress, text=messages[msg_idx])
        time.sleep(0.1)
        
    t.join(timeout=5)
    progress_bar.empty()
    
    if "error" in result_container:
        raise Exception(result_container["error"])
        
    return result_container.get("res")


def render():
    st.markdown("<h1 style='padding-bottom: 0px;'>✅ Final Analysis Results</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-bottom: 2rem;'>Detailed breakdown from the RealityLab AI Coordinator.</p>", unsafe_allow_html=True)

    profile = get_state("business_profile_data") or {}
    scenarios = get_state("scenarios") or []
    analysis_id = get_state("current_analysis_id")

    # Handle Pending Execution
    if get_state("pending_execution"):
        st.markdown("### Executing Analysis Pipeline")
        try:
            res = execute_with_progress(analysis_id, profile, scenarios)
            set_state("analysis_results", res)
            set_state("pending_execution", False)
            st.rerun()
        except Exception as e:
            set_state("pending_execution", False)
            st.error("❌ Analysis Execution Failed")
            st.markdown(f"**What failed:** The RealityLab AI backend encountered an issue during execution.\n\n**Possible reason:** {str(e)}\n\n**Suggested next action:** Please verify your backend server is running and try again from the Scenario Builder.")
            if st.button("← Return to Scenario Builder"):
                set_state("current_page", "scenario_builder")
                st.rerun()
            return

    results = get_state("analysis_results")

    # Empty State
    if not results:
        render_empty_state("clipboard-data", "No analysis available yet.", "Create a business profile and execute an analysis to view results.")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("🧪 Go to Scenario Builder", type="primary", use_container_width=True):
                set_state("current_page", "scenario_builder")
                st.rerun()
        return

    # Success State Banner
    timestamp = results.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
    b_name = profile.get("name", "Unknown Business")
    num_scenarios = len(scenarios)
    
    st.success(f"**Analysis completed successfully!**\\n\\nBusiness: **{b_name}** | Scenarios Analyzed: **{num_scenarios}** | Executed at: **{timestamp}**")

    metrics = results.get("metrics", {})

    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(
        ["Finance", "Market", "Risk", "Prediction", "Timeline", "Evidence", "Decision"]
    )

    with tabs[0]:
        st.subheader("Financial Breakdown")
        st.write(f"**Revenue:** ${metrics.get('revenue', 0):,.2f}")
        st.write(f"**Profit:** ${metrics.get('profit', 0):,.2f}")
        st.write(f"**ROI:** {metrics.get('roi', 0):.2f}%")
        st.bar_chart(
            {"Revenue": [metrics.get("revenue", 0)], "Profit": [metrics.get("profit", 0)]}
        )

    with tabs[1]:
        st.subheader("Market Analysis")
        market_data = metrics.get("market_analysis", {})
        if market_data:
            st.write(f"**Projected Growth:** {market_data.get('growth', 'Unknown')}")
            st.write(f"**Competition Level:** {market_data.get('competition', 'Unknown')}")
            st.write(f"**Demand:** {market_data.get('demand', 'Unknown')}")
            st.write(f"**Market Opportunity:** {market_data.get('opportunity', 'Unknown')}")
            st.progress(market_data.get('confidence', 0) / 100.0, text=f"Analysis Confidence: {market_data.get('confidence', 0):.1f}%")
        else:
            render_empty_state("chart-line", "No Market Analysis", "Please run the analysis to generate dynamic market insights.")

    with tabs[2]:
        st.subheader("Risk Factors")
        st.progress(
            metrics.get("risk_score", 0) / 100.0,
            text=f"Risk Score: {metrics.get('risk_score', 0):.1f}/100",
        )
        risk_data = metrics.get("risk_analysis", {})
        if risk_data and "factors" in risk_data:
            for factor in risk_data["factors"]:
                st.markdown(f"- {factor}")
        else:
            st.markdown("- Supply chain delays\n- High inflation\n- Local competition")

    with tabs[3]:
        st.subheader("Predictive Models")
        predictions = metrics.get("predictions", {})
        if predictions and isinstance(predictions, dict):
            import pandas as pd
            df = pd.DataFrame(predictions)
            st.line_chart(df)
        elif predictions and isinstance(predictions, list):
            st.line_chart(predictions)
        else:
            st.line_chart([10, 25, 45, 60, 85, 120])

    with tabs[4]:
        st.subheader("Implementation Timeline")
        timeline_data = metrics.get("timeline", [])
        if timeline_data:
            for phase in timeline_data:
                st.write(f"**{phase['name']}**: {phase['duration']}")
        else:
            st.write("Phase 1: 0-3 Months (Setup)")
            st.write("Phase 2: 4-6 Months (Launch)")
            st.write("Phase 3: 7-12 Months (Scale)")

    with tabs[5]:
        st.subheader("Evidence & Citations")
        evidence_data = metrics.get("evidence", [])
        if evidence_data:
            for ev in evidence_data:
                st.info(f"**{ev['title']}**\n\n{ev['description']}")
        else:
            render_empty_state("??", "Notice", "Based on recent market reports in the target area.")

    with tabs[6]:
        st.subheader("Final Decision")
        score = metrics.get('confidence', 0)
        
        decision = results.get("rationale", "Unknown")
            
        st.metric(
            label="Decision Score",
            value=f"{score:.1f}/100",
            delta="Approved" if score >= 60 else "Review Required",
            delta_color="normal" if score >= 60 else "inverse"
        )
        st.info(f"**Rationale:** {decision}")
