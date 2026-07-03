import streamlit as st
from frontend.components.error_state import render_error_state
import uuid
import time
import requests
import os
from frontend.state import set_state


def render():
    st.markdown("<h1>➕ New Analysis</h1>", unsafe_allow_html=True)
    st.markdown("Create a new business analysis by defining the core parameters.")

    with st.form("new_analysis_form"):
        col1, col2 = st.columns(2)

        with col1:
            business_name = st.text_input(
                "Business Name*", placeholder="e.g., Downtown Cafe"
            )
            business_type = st.selectbox(
                "Business Type*",
                ["Cafe", "Restaurant", "Retail", "Tech Startup", "Consulting", "Other"],
            )
            location = st.text_input(
                "Location*", placeholder="e.g., Urban, Suburban, or specific city"
            )

        with col2:
            investment = st.number_input(
                "Initial Investment ($)*", min_value=1000, value=50000, step=1000
            )
            team_size = st.number_input("Team Size", min_value=1, value=5)
            target_customers = st.text_input(
                "Target Customers", placeholder="e.g., Students, Professionals"
            )

        goal = st.text_area(
            "Business Goal*",
            placeholder="What are you trying to achieve? (e.g., 20% ROI in year 1)",
        )

        submitted = st.form_submit_button(
            "Save and Continue to Scenario Builder",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if (
                not business_name
                or not business_type
                or not location
                or not investment
                or not goal
            ):
                render_error_state("Error", None, "Please fill in all required fields marked with *.")
            else:
                with st.spinner("Saving business profile..."):
                    profile_id = str(uuid.uuid4())
                    profile_data = {
                        "id": profile_id,
                        "name": business_name,
                        "type": business_type,
                        "location": location,
                        "investment": investment,
                        "team_size": team_size,
                        "target_customers": target_customers,
                        "goal": goal,
                        "created_at": time.time(),
                    }

                    # Save to database (assuming generic save or direct sql if needed)
                    try:
                        API_URL = os.environ.get("API_URL", "http://localhost:8000")
                        response = requests.post(
                            f"{API_URL}/api/v1/analysis", json=profile_data, timeout=5
                        )

                        if (
                            response.status_code == 200
                            and response.json().get("status") == "success"
                        ):
                            analysis_id = response.json().get("analysis_id")
                            set_state("business_profile_data", profile_data)
                            set_state("current_analysis_id", analysis_id)

                            st.toast("? " + str("Business profile saved successfully!"))
                            time.sleep(0.5)
                            st.session_state["current_page"] = "scenario_builder"
                            st.rerun()
                        else:
                            render_error_state("Error", None, f"Error saving profile: {response.text}")
                    except Exception as e:
                        render_error_state("Error", None, f"Error connecting to backend: {str(e)}")
