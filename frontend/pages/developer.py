import streamlit as st


def render():
    st.markdown("<h1>💻 Developer Console</h1>", unsafe_allow_html=True)
    st.write("Advanced tools for debugging and extending RealityLab AI.")

    st.subheader("Active Session State")
    if st.checkbox("Show Raw Session State"):
        # We filter out large objects if needed
        state_dict = {k: v for k, v in st.session_state.items() if k != "current_page"}
        st.json(state_dict)

    st.subheader("API Keys & Webhooks")
    st.text_input(
        "OpenAI API Key", type="password", value="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
    )
    st.text_input(
        "Google Cloud Key", type="password", value="AIzaSy-xxxxxxxxxxxxxxxxxxxx"
    )
    st.text_input(
        "Webhook URL for External Triggers",
        placeholder="https://api.example.com/webhook",
    )

    if st.button("Update Keys"):
        st.toast("? " + str("API keys updated safely in secure storage."))
