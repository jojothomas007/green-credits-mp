import streamlit as st

def render():
    st.set_page_config(page_title="Personal Registration", layout="centered")
    st.title("🌱 Carbon Credit Buyer Registration")

    # Initialize session state to track if registration was successful
    if "registration_successful" not in st.session_state:
        st.session_state.registration_successful = False
        st.session_state.registered_name = ""

    # Show welcome message
    st.markdown("Welcome! Register to start buying verified carbon credits and offset your emissions. 🌍")
    st.markdown("**Note:** All fields are mandatory")

    # Only show the form if registration was not successful yet
    if not st.session_state.registration_successful:
        with st.form("registration_form"):
            # Personal Information
            st.subheader("Personal Information")
            name = st.text_input("Full Name *")
            age = st.number_input("Age *", min_value=1, max_value=120, value=25)
            country = st.selectbox("Country *", ["India", "USA", "Germany", "France", "Other"])
            state = st.text_input("State *")
            zip_code = st.text_input("Postal Zip Code *")
            
            # Contact Information
            st.subheader("Contact Information")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")

            # Cultivation Details
            st.subheader("Cultivation Details (if applicable)")
            has_cultivation = st.checkbox("I have cultivation details to add")
            cultivation_type = st.text_input("Cultivation Type", disabled=not has_cultivation)
            cultivation_area = st.number_input("Cultivation Area (acres)", min_value=0.0, disabled=not has_cultivation)
            
            # Account Information
            st.subheader("Account Information")
            username = st.text_input("Username *")
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            
            terms = st.checkbox("I accept the Terms & Conditions *")

            submitted = st.form_submit_button("Register Now")

            if submitted:
                # Check if any field is empty
                required_fields = {
                    "Full Name": name,
                    "State": state,
                    "Zip Code": zip_code,
                    "Email": email,
                    "Phone": phone,
                    "Username": username,
                    "Password": password
                }
                
                empty_fields = [field for field, value in required_fields.items() if not value and not (isinstance(value, (int, float)))]
                
                if empty_fields:
                    st.error(f"❗ Please fill in all required fields: {', '.join(empty_fields)}")
                elif password != confirm_password:
                    st.error("❗ Passwords do not match")
                elif not terms:
                    st.warning("📜 Please accept the Terms & Conditions to proceed")
                else:
                    # Prepare data to store in session state
                    st.session_state.personal_info = {
                        "name": name,
                        "age": age,
                        "country": country,
                        "state": state,
                        "zip_code": zip_code,
                        "email": email,
                        "phone": phone
                    }
                    
                    # Store cultivation info if provided
                    if has_cultivation:
                        st.session_state.cultivation_info = {
                            "type": cultivation_type,
                            "area": cultivation_area
                        }
                    else:
                        st.session_state.cultivation_info = {}
                    
                    # Set session state to mark successful registration
                    st.session_state.registration_successful = True
                    st.session_state.registered_name = name
                    st.rerun()  # Rerun to update the UI immediately
    else:
        # Display success message after successful registration
        st.success(f"✅ Registration successful for {st.session_state.registered_name}!")
        st.markdown("Refresh the browser to proceed to login.")
        
        # Show a preview of the registered information
        st.subheader("Registered Information")
        if hasattr(st.session_state, 'personal_info'):
            st.json(st.session_state.personal_info)
        
        if hasattr(st.session_state, 'cultivation_info') and st.session_state.cultivation_info:
            st.subheader("Cultivation Details")
            st.json(st.session_state.cultivation_info)
            
        if st.button("Register Another Account"):
            st.session_state.registration_successful = False
            st.rerun()
