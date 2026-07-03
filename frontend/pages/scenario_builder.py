import streamlit as st
from frontend.components.error_state import render_error_state
import uuid
import time
from frontend.state import get_state, set_state


def render():
    st.markdown("<h1>🧪 Scenario Builder</h1>", unsafe_allow_html=True)

    profile = get_state("business_profile_data")
    if not profile:
        st.warning(
            "No business profile found. Please create one in 'New Analysis' first."
        )
        if st.button("Go to New Analysis"):
            set_state("current_page", "new_analysis")
            st.rerun()
        return

    st.markdown(f"### Scenarios for: **{profile['name']}**")
    st.markdown(
        "Define alternative 'what-if' scenarios to simulate different market conditions."
    )

    scenarios = get_state("scenarios", [])

    with st.expander("➕ Add New Scenario", expanded=len(scenarios) == 0):
        with st.form("add_scenario_form"):
            s_name = st.text_input(
                "Scenario Name*",
                placeholder="e.g., Best Case, Worst Case, High Inflation",
            )
            s_desc = st.text_area(
                "Description", placeholder="What happens in this scenario?"
            )

            st.markdown("##### Adjustments")
            col1, col2, col3 = st.columns(3)
            with col1:
                cost_adj = st.slider("Cost Adjustment (%)", -50, 50, 0)
            with col2:
                demand_adj = st.slider("Demand Adjustment (%)", -50, 50, 0)
            with col3:
                price_adj = st.slider("Price Adjustment (%)", -50, 50, 0)

            submitted = st.form_submit_button("Save Scenario")
            if submitted:
                if not s_name:
                    render_error_state("Error", None, "Scenario name is required.")
                else:
                    new_s = {
                        "id": str(uuid.uuid4()),
                        "name": s_name,
                        "description": s_desc,
                        "adjustments": {
                            "cost": cost_adj,
                            "demand": demand_adj,
                            "price": price_adj,
                        },
                    }
                    scenarios.append(new_s)
                    set_state("scenarios", scenarios)
                    st.toast("? " + str("Scenario added!"))
                    st.rerun()

    if scenarios:
        st.markdown("### Configured Scenarios")
        for i, sc in enumerate(scenarios):
            with st.container():
                st.markdown(f"**{i+1}. {sc['name']}**")
                st.write(f"*{sc['description']}*")
                st.write(
                    f"Costs: {sc['adjustments']['cost']}%, Demand: {sc['adjustments']['demand']}%, Price: {sc['adjustments']['price']}%"
                )
                st.divider()

    st.markdown("### Run Full Simulation")
    if st.button("🚀 Execute Analysis", type="primary", use_container_width=True):
        analysis_id = get_state("current_analysis_id")
        if not analysis_id:
            render_error_state("Error", None, "No active analysis found. Please start a New Analysis.")
        else:
            set_state("pending_execution", True)
            set_state("current_page", "results")
            st.rerun()
