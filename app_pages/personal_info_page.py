import streamlit as st

def personal_info_form():
    st.title("📝 Personal Information")
    
    # Ensure default values are valid
    name = st.text_input("Full Name", value=st.session_state.personal_info.get("name", ""))
    
    # Set a valid default value for age
    default_age = st.session_state.personal_info.get("age", 1)  # Default to 1 if no value is set
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=default_age  # Ensure the default value is within the valid range
    )
    
    country = st.text_input("Country", value=st.session_state.personal_info.get("country", ""))
    state = st.text_input("State", value=st.session_state.personal_info.get("state", ""))
    zip_code = st.text_input("Postal Zip Code", value=st.session_state.personal_info.get("zip_code", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = "home"
    with col2:
        if st.button("Next"):
            # Save the entered values into session state
            st.session_state.personal_info = {
                "name": name,
                "age": age,
                "country": country,
                "state": state,
                "zip_code": zip_code,
            }
            st.session_state.step = "cultivation"
