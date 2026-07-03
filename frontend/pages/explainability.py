import streamlit as st
from frontend.components.empty_state import render_empty_state
from frontend.state import get_state


def render():
    st.markdown("<h1>🔍 Decision Explainability</h1>", unsafe_allow_html=True)
    st.write(
        "Understand why the system made its recommendation based on the AI Agent consensus."
    )

    results = get_state("analysis_results")
    if not results:
        st.toast("?? " + str("No analysis results found. Please run a simulation first."))
        return

    metrics = results.get("metrics", {})

    st.subheader(
        f"Analysis Outcome: {'Proceed' if metrics.get('confidence', 0) > 70 else 'Re-evaluate'}"
    )
    st.markdown(
        f"> **Rationale**: The decision engine scored this analysis at {metrics.get('confidence', 0)}/100, largely driven by a projected ROI of {metrics.get('roi', 0)}% and a risk score of {metrics.get('risk_score', 0)}/100."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Supporting Evidence")
        st.success(
            f"✔ **Finance**: Projected profit of ${metrics.get('profit', 0):,.2f}."
        )
        st.toast("? " + str("✔ **Market**: Positive growth potential identified."))
        if metrics.get("confidence", 0) > 80:
            st.toast("? " + str("✔ **Decision**: Overwhelming consensus among agents."))

    with col2:
        st.markdown("### Risks & Trade-offs")
        if metrics.get("risk_score", 0) > 50:
            st.toast("?? " + str("⚠ **Risk**: Risk score is elevated. Proceed with caution."))
        else:
            st.info(
                "ℹ **Risk**: No major critical risks identified, but standard market risks apply."
            )

    st.divider()

    st.subheader("Key Parameters Used")
    profile = get_state("business_profile_data", {})

    if profile:
        st.table(
            [
                {
                    "Parameter": "Initial Investment",
                    "Value": f"${profile.get('investment', 0):,.2f}",
                },
                {
                    "Parameter": "Location Target",
                    "Value": profile.get("location", "N/A"),
                },
                {
                    "Parameter": "Team Size",
                    "Value": str(profile.get("team_size", "N/A")),
                },
            ]
        )
