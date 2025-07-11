import streamlit as st

st.set_page_config(page_title="Industrialist Registration", layout="centered")
st.title("🏭 Carbon Credit Buyer Registration")

st.markdown("Welcome! Register your organization to start buying verified carbon credits and offset your emissions. 🌍")

with st.form("registration_form"):
    company_name = st.text_input("Company Name")
    industry = st.selectbox("Industry Type", ["Manufacturing", "Energy", "Transportation", "Construction", "Other"])
    reg_number = st.text_input("Company Registration Number")
    website = st.text_input("Company Website")
    country = st.selectbox("Country", ["India", "USA", "Germany", "France", "Other"])
    
    contact_name = st.text_input("Contact Person")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")

    credit_types = st.multiselect("Preferred Carbon Credit Types", ["Afforestation", "Renewable Energy", "Methane Capture", "Waste Management"])
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    terms = st.checkbox("I accept the Terms & Conditions")

    submitted = st.form_submit_button("Register Now")

    if submitted:
        if password != confirm_password:
            st.error("❗ Passwords do not match")
        elif not terms:
            st.warning("📜 Please accept the Terms & Conditions to proceed")
        else:
            st.success(f"✅ Registration successful for {company_name}!")