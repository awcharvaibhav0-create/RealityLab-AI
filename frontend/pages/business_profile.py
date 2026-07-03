import streamlit as st
import json
import time
from frontend.state import get_state, set_state
from frontend.components.empty_state import render_empty_state
from frontend.components.error_state import render_error_state
from frontend.components.loading_state import render_loading_state

def render():
    st.markdown("<h1>🏢 Business Profile</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;'>Manage your current business profiles, import/export, and edit them dynamically based on knowledge schemas.</p>",
        unsafe_allow_html=True
    )

    profile = get_state("business_profile_data")

    tab1, tab2, tab3 = st.tabs(["Current Profile", "Import / Export", "Schemas"])

    with tab1:
        if profile:
            st.markdown(f"### Active Profile: <span style='color: #60a5fa;'>{profile.get('name')}</span>", unsafe_allow_html=True)
            with st.form("edit_profile_form"):
                
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Business Name", value=profile.get("name", ""))
                    loc = st.text_input("Location", value=profile.get("location", ""))
                with c2:
                    btype = st.text_input("Business Type", value=profile.get("type", ""))
                    inv = st.number_input(
                        "Initial Investment ($)", value=float(profile.get("investment", 0)), step=1000.0
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                        profile["name"] = name
                        profile["type"] = btype
                        profile["location"] = loc
                        profile["investment"] = inv
                        set_state("business_profile_data", profile)
                        st.toast("✅ Profile updated successfully!")
                        time.sleep(0.5)
                        st.rerun()
                with col2:
                    if st.form_submit_button("Delete", use_container_width=True):
                        set_state("business_profile_data", None)
                        st.toast("⚠️ Profile deleted.")
                        time.sleep(0.5)
                        st.rerun()
        else:
            if render_empty_state(
                icon="🏢",
                title="No Active Profile",
                description="You don't have an active business profile selected. Start a new analysis to create one.",
                button_text="Start Analysis",
                button_key="bp_start_analysis"
            ):
                st.session_state["current_page"] = "new_analysis"
                st.rerun()

    with tab2:
        st.markdown("### Import / Export JSON")
        if profile:
            json_str = json.dumps(profile, indent=2)
            st.download_button(
                "⬇️ Export Profile (JSON)",
                data=json_str,
                file_name=f"profile_{profile.get('id', 'export')}.json",
                mime="application/json",
                type="primary"
            )
        else:
            st.markdown("<p style='color: #94a3b8;'>Export requires an active profile.</p>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown("#### Import Profile")
        uploaded_file = st.file_uploader("Upload JSON profile", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                if st.button("Apply Imported Profile", type="primary"):
                    set_state("business_profile_data", data)
                    st.toast("✅ Profile imported successfully!")
                    time.sleep(0.5)
                    st.rerun()
            except Exception as e:
                render_error_state("Invalid JSON Upload", e, "The uploaded file is not a valid JSON business profile.")

    with tab3:
        st.markdown("### JSON Schemas")
        st.write("Dynamic form schemas pulled from `knowledge/` engine.")
        st.json(
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["Cafe", "Restaurant", "Retail", "Tech Startup"],
                    },
                    "location": {"type": "string"},
                    "investment": {"type": "number"},
                },
                "required": ["name", "type", "investment"],
            }
        )

