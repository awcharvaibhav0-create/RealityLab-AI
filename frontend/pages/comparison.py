import streamlit as st
import pandas as pd
from frontend.state import get_state


def render():
    st.markdown("<h1>⚖️ Scenario Comparison</h1>", unsafe_allow_html=True)
    st.write("Compare different scenarios side-by-side to make the best decision.")

    scenarios = get_state("scenarios", [])
    if not scenarios:
        from frontend.components.empty_state import render_empty_state
        render_empty_state("📊", "No Scenarios", "No scenarios exist to compare. Create them in the 'Scenario Builder'.")
        return

    st.markdown("### Metrics Comparison")

    # Load metrics from persisted execution results
    results = get_state("analysis_results")
    scenario_outputs = []
    if results and "metrics" in results and "scenario_outputs" in results["metrics"]:
        scenario_outputs = results["metrics"]["scenario_outputs"]
        
    data = []
    for sc in scenarios:
        # Find matching scenario in backend results using unique UUID
        matching_output = next((out for out in scenario_outputs if out.get("scenario_id") == sc.get("id")), None)
        true_roi = matching_output.get("metrics", {}).get("roi") if matching_output else None
        roi_display = f"{true_roi:.1f}%" if true_roi is not None else "N/A"
        
        data.append(
            {
                "Scenario": sc["name"],
                "Cost Adj": f"{sc['adjustments']['cost']}%",
                "Demand Adj": f"{sc['adjustments']['demand']}%",
                "Price Adj": f"{sc['adjustments']['price']}%",
                "ROI": roi_display
            }
        )

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    st.markdown("### Visual Comparison")

    results = get_state("analysis_results")
    if not results or "metrics" not in results or "scenario_outputs" not in results["metrics"]:
        st.warning("No analysis results found. Run an analysis to view visual comparisons.")
    else:
        import plotly.express as px
        scenario_outputs = results["metrics"]["scenario_outputs"]
        
        # Enforce unique scenario names for the bar charts so identical names don't stack/collide
        chart_data = []
        seen_names = {}
        for sc in scenario_outputs:
            base_name = sc.get("strategy_id", "Unknown")
            if base_name in seen_names:
                seen_names[base_name] += 1
                unique_name = f"{base_name} ({seen_names[base_name]})"
            else:
                seen_names[base_name] = 0
                unique_name = base_name
                
            chart_data.append({
                "Scenario": unique_name,
                "ROI": sc.get("metrics", {}).get("roi", 0),
                "Profit": sc.get("metrics", {}).get("profit", 0),
                "Revenue": sc.get("metrics", {}).get("revenue", 0),
                "Risk": sc.get("metrics", {}).get("risk", 0),
                "Decision Score": sc.get("metrics", {}).get("decision_score", 0)
            })
        chart_df = pd.DataFrame(chart_data)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.bar(chart_df, x="Scenario", y="Revenue", title="Revenue Comparison", color="Scenario"), use_container_width=True)
            st.plotly_chart(px.bar(chart_df, x="Scenario", y="ROI", title="ROI Comparison", color="Scenario"), use_container_width=True)
            st.plotly_chart(px.bar(chart_df, x="Scenario", y="Decision Score", title="Decision Score Comparison", color="Scenario"), use_container_width=True)
        with col2:
            st.plotly_chart(px.bar(chart_df, x="Scenario", y="Profit", title="Profit Comparison", color="Scenario"), use_container_width=True)
            st.plotly_chart(px.bar(chart_df, x="Scenario", y="Risk", title="Risk Comparison", color="Scenario"), use_container_width=True)

    st.toast("✅ Comparison complete. Use these insights in the Decision Engine.")
