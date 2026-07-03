import streamlit as st
from frontend.components.empty_state import render_empty_state
from frontend.state import get_state


def render():
    st.markdown("<h1>📈 Live Agent Monitor</h1>", unsafe_allow_html=True)
    st.write(
        "Real-time visibility into the Google ADK orchestrator and agent execution."
    )

    # In a real setup with background tasks, we would poll here.
    # For now, we mock the final state or read from the last execution state.

    st.subheader("Current Execution")

    results = get_state("analysis_results")
    if not results:
        render_empty_state("??", "Notice", "No execution currently running.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Agent Pipeline")

        # Display as completed if we have results
        st.progress(1.0, text="Execution 100% Complete")

        st.toast("? " + str("Coordinator - `Completed`"))
        st.toast("? " + str("Finance Agent - `Completed`"))
        st.toast("? " + str("Market Agent - `Completed`"))
        st.toast("? " + str("Risk Agent - `Completed`"))
        st.toast("? " + str("Prediction Agent - `Completed`"))
        st.toast("? " + str("Evidence Agent - `Completed`"))
        st.toast("? " + str("Decision Agent - `Completed`"))

    with col2:
        st.markdown("### Engine Metrics")
        st.metric(label="CPU Usage", value="14%")
        st.metric(label="Memory Usage", value="128 MB")
        st.metric(label="Active Threads", value="0")

    st.toast("? " + str("Analysis pipeline execution complete!"))
