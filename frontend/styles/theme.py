import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        /* Glassmorphism theme */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        
        /* Hide Streamlit anchor links */
        .stMarkdown a.header-anchor {
            display: none !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            width: 250px !important;
            min-width: 250px !important;
            max-width: 250px !important;
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Hide default Streamlit navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Metric cards custom HTML */
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
            height: 100%;
            min-height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .metric-label {
            font-size: 0.95rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            white-space: normal;
        }
        
        .metric-value {
            font-size: clamp(1.2rem, 2vw, 1.8rem); /* Prevent truncation */
            font-weight: 700;
            background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            white-space: normal;
            word-wrap: break-word;
            line-height: 1.2;
        }

        /* Base Global Button Styles for Glassmorphism */
        .stButton>button {
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #f8fafc;
            font-weight: 600;
            white-space: pre-wrap;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: flex-start;
        }
        .stButton>button:hover {
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.08);
            color: white;
        }
        
        /* 1. Sidebar Buttons (56px) */
        [data-testid="stSidebar"] .stButton>button {
            height: 56px !important;
            min-height: 56px !important;
            padding: 0 1rem !important;
            margin-bottom: 0.2rem !important;
            font-size: 0.95rem !important;
        }
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(90deg, rgba(96, 165, 250, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
            border-left: 4px solid #60a5fa;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 0 15px rgba(96, 165, 250, 0.2);
            color: #ffffff;
        }
        
        /* 2. Quick Actions (50-54px) */
        [data-testid="stAppViewContainer"] button[kind="secondary"] {
            height: 54px !important;
            min-height: 54px !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.95rem !important;
        }
        
        /* 3. Navigation Hub Cards (Large) */
        [data-testid="stAppViewContainer"] button[kind="primary"] {
            min-height: 130px !important;
            padding: 1.5rem !important;
            font-size: 1.05rem !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            justify-content: flex-start !important;
            gap: 0.5rem !important;
        }
        [data-testid="stAppViewContainer"] button[kind="primary"]:hover {
            transform: scale(1.02) translateY(-4px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
        }

        /* Reduce Hero Height */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            padding-top: 0rem !important;
            gap: 0.2rem !important;
        }
        
        h1 {
            margin-top: -1.5rem !important;
            margin-bottom: 0.2rem;
            padding-bottom: 0;
            background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif;
            font-size: 2.8rem !important;
        }
        h2, h3 {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            background: -webkit-linear-gradient(45deg, #60a5fa, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif;
        }
        
        /* Icons */
        @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css");

        /* Status Colors */
        .status-green { color: #4ade80 !important; font-weight: bold; }
        .status-yellow { color: #facc15 !important; font-weight: bold; }
        .status-red { color: #f87171 !important; font-weight: bold; }
        
        /* --- NEW GLOBAL DESIGN SYSTEM CSS --- */

        /* Forms Styling */
        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #f8fafc !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > div:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
        }

        /* Standard Streamlit Button overrides */
        [data-testid="stAppViewContainer"] button[kind="primary"] {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
            border: none !important;
            color: white !important;
        }
        [data-testid="stAppViewContainer"] button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        [data-testid="stAppViewContainer"] button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4) !important;
        }

        /* Custom HTML Buttons */
        .btn-danger {
            background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
            border: none;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(239, 68, 68, 0.4);
        }

        /* Tables */
        [data-testid="stTable"] table, [data-testid="stDataFrame"] table {
            background: rgba(15, 23, 42, 0.6) !important;
            border-collapse: collapse;
            border-radius: 8px;
            overflow: hidden;
            width: 100%;
        }
        [data-testid="stTable"] th, [data-testid="stDataFrame"] th {
            background: rgba(255, 255, 255, 0.1) !important;
            color: #f8fafc !important;
            padding: 1rem !important;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stTable"] td, [data-testid="stDataFrame"] td {
            padding: 0.75rem 1rem !important;
            color: #cbd5e1 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        [data-testid="stTable"] tr:nth-child(even), [data-testid="stDataFrame"] tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02) !important;
        }
        [data-testid="stTable"] tr:hover, [data-testid="stDataFrame"] tr:hover {
            background: rgba(255, 255, 255, 0.08) !important;
        }

        /* Responsive Breakpoints */
        @media (max-width: 1920px) {
            .block-container { max-width: 1600px !important; }
        }
        @media (max-width: 1440px) {
            .block-container { max-width: 1200px !important; }
        }
        @media (max-width: 1366px) {
            .block-container { max-width: 1100px !important; }
        }
        @media (max-width: 768px) {
            .block-container { max-width: 100% !important; padding: 1rem !important; }
            h1 { font-size: 2rem !important; }
        }

        </style>
    """,
        unsafe_allow_html=True,
    )
