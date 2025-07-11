import streamlit as st

# Login Page functionality
def login_page(credentials):
    # Display the image at the top
    st.image(
        "https://i.etsystatic.com/32486242/r/il/961434/5428907342/il_fullxfull.5428907342_rin0.jpg",
        use_container_width=True,
    )
    
    # Center-align the login form
    st.markdown("<h2 style='text-align: center;'>🌾 Farmer Login</h2>", unsafe_allow_html=True)
    
    # Create a centered form for login
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            if username in credentials and credentials[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.step = "home"  # Navigate to home page
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")
