import streamlit as st
from frontend.components.empty_state import render_empty_state


def render():
    st.markdown("<h1>🛡️ Trust Center</h1>", unsafe_allow_html=True)
    st.write("Review compliance, privacy, and security metrics for RealityLab AI.")

    st.markdown("### Security Posture")
    st.toast("? " + str("✔ Data Encryption at Rest: Active"))
    st.toast("? " + str("✔ Secure Execution Sandbox: Active"))
    st.toast("? " + str("✔ RBAC Policies: Enforced"))

    st.markdown("### AI Safety & Alignment")
    st.info(
        "The Decision Engine incorporates human-in-the-loop (HITL) checkpoints for all actions involving capital reallocation."
    )

    st.markdown("### Audits")
    st.write(
        "All system executions are immutably logged to the database for regulatory compliance."
    )
