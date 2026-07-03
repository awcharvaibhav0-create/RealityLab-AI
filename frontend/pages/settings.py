import streamlit as st


def render():
    st.markdown("<h1>⚙️ System Settings</h1>", unsafe_allow_html=True)
    st.write("Configure your RealityLab AI workspace preferences.")

    st.subheader("Global Preferences")
    st.selectbox("Theme", ["System Default", "Dark Mode", "Light Mode"])
    st.selectbox("Language", ["English", "Spanish", "French", "German"])

    st.subheader("Notification Preferences")
    st.checkbox("Email Alerts for Completed Analysis", value=True)
    st.checkbox("Push Notifications", value=False)

    if st.button("Save Settings", type="primary"):
        st.toast("? " + str("Settings saved successfully!"))
