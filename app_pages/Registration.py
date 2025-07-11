import streamlit as st

def render():
    st.set_page_config(page_title="Industrialist Registration", layout="centered")
    st.title("🏭 Carbon Credit Buyer Registration")

    # Initialize session state to track if registration was successful
    if "registration_successful" not in st.session_state:
        st.session_state.registration_successful = False
        st.session_state.registered_company = ""

    # Show welcome message
    st.markdown("Welcome! Register your organization to start buying verified carbon credits and offset your emissions. 🌍")
    st.markdown("**Note:** All fields are mandatory")

    # Only show the form if registration was not successful yet
    if not st.session_state.registration_successful:
        with st.form("registration_form"):
            company_name = st.text_input("Company Name *")
            industry = st.selectbox("Industry Type *", ["Manufacturing", "Energy", "Transportation", "Construction", "Other"])
            reg_number = st.text_input("Company Registration Number *")
            website = st.text_input("Company Website *")
            country = st.selectbox("Country *", ["India", "USA", "Germany", "France", "Other"])
            
            contact_name = st.text_input("Contact Person *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")

            username = st.text_input("Username *")
            
            password = st.text_input("Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            
            terms = st.checkbox("I accept the Terms & Conditions *")

            submitted = st.form_submit_button("Register Now")

            if submitted:
                # Check if any field is empty
                required_fields = {
                    "Company Name": company_name,
                    "Registration Number": reg_number,
                    "Website": website,
                    "Contact Person": contact_name,
                    "Email": email,
                    "Phone": phone,
                    "Username": username,
                    "Password": password
                }
                
                empty_fields = [field for field, value in required_fields.items() if not value.strip()]
                
                if empty_fields:
                    st.error(f"❗ Please fill in all required fields: {', '.join(empty_fields)}")
                elif password != confirm_password:
                    st.error("❗ Passwords do not match")
                elif not terms:
                    st.warning("📜 Please accept the Terms & Conditions to proceed")
                else:
                    # Set session state to mark successful registration
                    st.session_state.registration_successful = True
                    st.session_state.registered_company = company_name
                    st.rerun()  # Rerun to update the UI immediately
    else:
        # Display success message after successful registration
        st.success(f"✅ Registration successful for {st.session_state.registered_company}!")
        st.markdown("Refresh the browser to proceed to login.")
        if st.button("Register Another Company"):
            st.session_state.registration_successful = False
            st.rerun()
