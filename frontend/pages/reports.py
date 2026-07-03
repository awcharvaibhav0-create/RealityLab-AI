import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from backend.services.engines.report.report_engine import ReportEngine
from frontend.state import get_state


def render():
    st.markdown("<h1>📄 Reports & Export</h1>", unsafe_allow_html=True)
    st.write(
        "Generate and download comprehensive analysis reports based on real results."
    )

    engine = ReportEngine()

    results = get_state("analysis_results")
    if not results:
        st.toast("?? " + str("No analysis results found to generate reports from."))
        return

    st.toast("? " + str("Reports are ready for download!"))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.download_button(
            label="Download JSON",
            data=engine.generate_json(results),
            file_name="report.json",
            mime="application/json",
        )

    with col2:
        st.download_button(
            label="Download CSV",
            data=engine.generate_csv(results),
            file_name="report.csv",
            mime="text/csv",
        )

    with col3:
        st.download_button(
            label="Download HTML",
            data=engine.generate_html(results),
            file_name="report.html",
            mime="text/html",
        )

    with col4:
        pdf_bytes = engine.generate_pdf(results)
        with open("debug_streamlit.pdf", "wb") as f:
            f.write(pdf_bytes)
            
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="report.pdf",
            mime="application/pdf",
        )
