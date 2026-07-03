import streamlit as st
import pandas as pd
import datetime
import requests
import os
from frontend.components.empty_state import render_empty_state
from frontend.state import set_state

def render():
    st.markdown("<h1>??? Analysis History</h1>", unsafe_allow_html=True)
    st.write("Review past analyses stored in the RealityLab AI database.")

    API_URL = os.environ.get("API_URL", "http://localhost:8000")

    # Fetch History
    def fetch_history():
        try:
            res = requests.get(f"{API_URL}/api/v1/history", timeout=5)
            if res.status_code == 200 and res.json().get("status") == "success":
                return res.json().get("data", [])
        except Exception:
            pass
        return []

    history_data = fetch_history()

    if not history_data:
        render_empty_state("??", "No History", "No past analyses found. Start a new analysis to see it here.")
        return

    # Filters
    col1, col2, col3 = st.columns(3)
    search_term = col1.text_input("?? Search Business Name")
    status_filter = col2.selectbox("Filter by Status", ["All", "completed", "failed", "initialized"])
    sort_order = col3.selectbox("Sort By", ["Newest First", "Oldest First"])

    # Apply filters
    filtered_data = history_data
    if search_term:
        filtered_data = [d for d in filtered_data if search_term.lower() in (d.get("business_name") or "").lower()]
    if status_filter != "All":
        filtered_data = [d for d in filtered_data if d.get("status") == status_filter]
    if sort_order == "Oldest First":
        filtered_data = list(reversed(filtered_data))

    if not filtered_data:
        render_empty_state("??", "No Results", "No analyses match your search criteria.")
        return

    # Convert to DataFrame for Export
    df = pd.DataFrame(filtered_data)
    
    st.download_button(
        label="?? Export History to CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"realitylab_history_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    st.markdown("### Recent Records")

    # Display Glassmorphism Cards
    for record in filtered_data:
        with st.container():
            st.markdown("""<div class="glass-container" style="margin-bottom: 15px; padding: 15px;">""", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            with c1:
                st.markdown(f"**{record.get('business_name', 'Unknown')}** ({record.get('business_type', 'N/A')})")
                
                # Format start_time nicely if present
                st_time = record.get('start_time', '')
                if st_time:
                    try:
                        # Handle both 'T' and space separators gracefully
                        clean_time = st_time.split('.')[0].replace('T', ' ')
                        dt = datetime.datetime.strptime(clean_time, "%Y-%m-%d %H:%M:%S")
                        st_time_fmt = dt.strftime("%b %d, %Y %I:%M %p")
                    except:
                        st_time_fmt = st_time
                else:
                    st_time_fmt = "Unknown"
                    
                st.caption(f"Started: {st_time_fmt}")
                
                rec = record.get('recommendation')
                if rec:
                    st.write(f"Recommendation: **{rec}**")
            with c2:
                status = record.get("status", "unknown")
                color = "green" if status == "completed" else "red" if status == "failed" else "orange"
                st.markdown(f"Status: <span style='color:{color}; font-weight:bold;'>{status.upper()}</span>", unsafe_allow_html=True)
                st.write(f"Time: {record.get('processing_time')}")
            with c3:
                sc = record.get('decision_score')
                st.write(f"Decision Score: **{sc}/100**" if sc else "Decision Score: **--**")
                st.write(f"Scenarios: **{record.get('scenario_count', 0)}**")
            with c4:
                # Delete action
                if st.button("🗑️ Delete", key=f"del_{record['id']}", help="Delete this analysis"):
                    try:
                        requests.delete(f"{API_URL}/api/v1/history/{record['id']}", timeout=5)
                        st.rerun()
                    except:
                        st.toast("Error deleting record")
            st.markdown("</div>", unsafe_allow_html=True)
