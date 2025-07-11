import streamlit as st
import json

# Simulated credentials
USER_CREDENTIALS = {"farmer1": "pass123", "farmer2": "farm456"}

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "step" not in st.session_state:
    st.session_state.step = "home"
if "personal_info" not in st.session_state:
    st.session_state.personal_info = {}
if "cultivation_info" not in st.session_state:
    st.session_state.cultivation_info = {}

# --- Login Page ---
def login_page():
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
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.step = "home"  # Navigate to home page
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

# --- Home Page ---
def home_page():
    st.title("👨‍🌾 Farmer Dashboard")
    st.subheader(f"Welcome, {st.session_state.username}")
    st.image("https://cdn.britannica.com/83/215583-050-A59FA03A/man-uses-garden-hoe-weed-plants-garden.jpg", use_container_width=True)

    uploaded_image = st.file_uploader("Upload your profile image", type=["jpg", "png"])
    if uploaded_image:
        st.image(uploaded_image, caption="Your Profile Image", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Update Personal Information"):
            st.session_state.step = "personal_info"
    with col2:
        if st.button("Show Carbon Credit Score"):
            st.info("Carbon Credit Score feature coming soon!")
    with col3:
        if st.button("Show Information"):
            st.session_state.step = "show_info"

# --- Show Information Page ---
def show_information():
    st.title("📄 Preview Information")
    if st.session_state.personal_info:
        st.subheader("Personal Information")
        st.json(st.session_state.personal_info)
    else:
        st.warning("No personal information available.")

    if st.session_state.cultivation_info:
        st.subheader("Cultivation Details")
        st.json(st.session_state.cultivation_info)
    else:
        st.warning("No cultivation details available.")

    # Combine all information into a single dictionary
    all_info = {
        "personal_info": st.session_state.personal_info,
        "cultivation_info": st.session_state.cultivation_info,
    }

    # Provide a download button for the JSON file
    json_data = json.dumps(all_info, indent=4)
    st.download_button(
        label="Download Information as JSON",
        data=json_data,
        file_name="farmer_information.json",
        mime="application/json",
    )

    if st.button("Back to Dashboard"):
        st.session_state.step = "home"

# --- Personal Info Form ---
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

# --- Cultivation Details ---
def cultivation_form():
    st.title("🌱 Cultivation Details")

    # Initialize cultivation details list in session state
    if "cultivation_details" not in st.session_state:
        st.session_state.cultivation_details = []

    # Display existing cultivation details
    if st.session_state.cultivation_details:
        st.subheader("Existing Cultivation Details")
        for idx, detail in enumerate(st.session_state.cultivation_details):
            st.write(f"**Cultivation {idx + 1}:**")
            st.json(detail)

    # Add new cultivation details
    st.subheader("Add New Cultivation Details")
    crop_type = st.selectbox("Type of Cultivation", ["Vegetables", "Tree", "Both"])
    area_size = st.text_input("Area Size (e.g., 5 acres)")
    
    # Use a different key for the geo-location input field
    geo_location_input = st.text_input("Geo-location (latitude, longitude)", key="geo_location_input")

    # Button to select geo-location
    if st.button("Select Geo-location"):
        # Simulate geo-location selection (replace this with actual map integration if needed)
        selected_lat = 12.971598
        selected_lon = 77.594566
        geo_location = f"{selected_lat}, {selected_lon}"
        st.session_state.geo_location_input = geo_location  # Update the input field value
        st.success(f"Geo-location selected: {geo_location}")

    # Add new row to cultivation details
    if st.button("Add Cultivation Details"):
        if crop_type and area_size and geo_location_input:
            new_detail = {
                "crop_type": crop_type,
                "area_size": area_size,
                "geo_location": geo_location_input,
            }
            st.session_state.cultivation_details.append(new_detail)
            st.success("Cultivation details added successfully!")
        else:
            st.error("Please fill in all fields and select a geo-location.")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = "personal_info"
    with col2:
        if st.button("Submit"):
            st.session_state.cultivation_info = st.session_state.cultivation_details
            st.success("All cultivation details submitted successfully!")
            st.session_state.step = "home"  # Navigate to home page

# --- App Flow ---
if not st.session_state.authenticated:
    login_page()
else:
    if st.session_state.step == "home":
        home_page()
    elif st.session_state.step == "personal_info":
        personal_info_form()
    elif st.session_state.step == "cultivation":
        cultivation_form()
    elif st.session_state.step == "show_info":
        show_information()
