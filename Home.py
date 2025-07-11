import streamlit as st
import json
import os
import sys

# Add the app's directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import pages
from app_pages.login_page import login_page
from app_pages.home_page import home_page
from app_pages.information_page import show_information
from app_pages.personal_info_page import personal_info_form
from app_pages.cultivation_page import cultivation_form

# Simulated credentials
USER_CREDENTIALS = {"farmer": "farmer", "farmer2": "farmer2"}

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "step" not in st.session_state:
    st.session_state.step = "home"
if "personal_info" not in st.session_state:
    st.session_state.personal_info = {}
if "cultivation_info" not in st.session_state:
    st.session_state.cultivation_info = {}

# --- App Flow ---
if not st.session_state.authenticated:
    login_page(USER_CREDENTIALS)
else:
    if st.session_state.step == "home":
        home_page()
    elif st.session_state.step == "personal_info":
        personal_info_form()
    elif st.session_state.step == "cultivation":
        cultivation_form()
    elif st.session_state.step == "show_info":
        show_information()
