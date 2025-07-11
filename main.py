import streamlit as st
from src.transcribe_test.utils.auth import validate_user
import app_pages.Home as home
import app_pages.Market_Watch as market
import app_pages.Registration as registration

def show_login():
    st.title("Carbon Credit Buyer Application")
    
    # Create two columns: one for the image and one for login fields
    col_img, col_login = st.columns(2)
    
    # Add image to the left column with increased height
    with col_img:
        st.image("resources/Industry.jpg", use_container_width=True)
    # Add login fields to the right column
    with col_login:
        st.header("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Create two columns for the buttons
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            login_clicked = st.button("Login")
        with btn_col2:
            register_clicked = st.button("Register")
        
        if login_clicked:
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")
        if register_clicked:
            st.session_state.registration = True
            st.rerun()

def show_menu():
    choice = st.sidebar.radio("Navigate to", ["Home", "Market_Watch"])
    if choice == "Home":
        home.render()
    elif choice == "Market_Watch":
        market.render()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "registration" not in st.session_state:
    st.session_state.registration = False

if st.session_state.logged_in:
    st.sidebar.success(f"Welcome, {st.session_state.username}")
    show_menu()
else:
    if st.session_state.registration:
        registration.render()
    else:
        show_login()