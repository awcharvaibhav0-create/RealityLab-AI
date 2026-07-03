import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from frontend.styles.theme import apply_theme
from frontend.router import route_page
from frontend.session import init_session


def main():
    st.set_page_config(page_title="RealityLab AI", page_icon="🧬", layout="wide")
    init_session()
    apply_theme()
    route_page()


if __name__ == "__main__":
    main()
