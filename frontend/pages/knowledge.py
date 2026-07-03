import streamlit as st
from frontend.components.empty_state import render_empty_state


def render():
    st.markdown("<h1>📚 Knowledge Base</h1>", unsafe_allow_html=True)
    st.write("Query the central RealityLab AI knowledge repository (RAG system).")

    query = st.text_input(
        "Ask a business question",
        placeholder="e.g., What is the typical ROI for a cafe in an urban area?",
    )

    if st.button("Search", type="primary"):
        if query:
            with st.spinner("Searching knowledge base..."):
                # Mock RAG response
                st.toast("? " + str("Search complete."))

                st.markdown("### Answer")
                st.write(
                    "Based on recent reports, the typical ROI for a cafe in a high-density urban area is between 15% to 22% in the first two years, depending heavily on initial lease costs and local competition."
                )

                st.markdown("### Sources")
                st.info(
                    "- 'Urban Retail Analytics 2025' (Relevance: 0.94)\n- 'Food & Beverage Industry Trends' (Relevance: 0.88)"
                )
        else:
            st.toast("?? " + str("Please enter a query."))
