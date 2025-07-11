import streamlit as st
import json

# Set up the page
st.set_page_config(page_title="Farmer Data Portal", layout="wide")
st.title("🌾 Farmer Data Management Portal")

# Login Section
st.sidebar.title("🔒 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

if login_button:
    if username == "admin" and password == "password":  # Replace with proper authentication
        st.sidebar.success("Login successful!")
        st.session_state["logged_in"] = True
    else:
        st.sidebar.error("Invalid credentials")

# Check if logged in
if st.session_state.get("logged_in", False):
    # Farmer Page
    st.subheader("📂 Upload Farmer Data")
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

    if uploaded_file:
        try:
            farmer_data = json.load(uploaded_file)
            st.success("File uploaded successfully!")
            st.json(farmer_data)
        except Exception as e:
            st.error(f"Error reading file: {e}")

    # Search Farmer Section
    st.subheader("🔍 Search Farmer")
    search_query = st.text_input("Enter Farmer Name or ID")
    search_button = st.button("Search")

    if search_button and uploaded_file:
        results = [
            farmer for farmer in farmer_data.get("farmers", [])
            if search_query.lower() in farmer.get("name", "").lower()
        ]
        if results:
            for farmer in results:
                st.write(f"**Name:** {farmer['name']}")
                st.write(f"**Area Size:** {farmer['area_size']} acres")
                st.write(f"**Geo Location:** {farmer['geo_location']}")
                verify_button = st.button(f"Verify Geo Location for {farmer['name']}")
                if verify_button:
                    st.success("Geo Location Verified ✅")
                quarterly_button = st.button(f"Quarterly Check-in for {farmer['name']}")
                if quarterly_button:
                    st.warning("Geo Location Not Verified ⚠️")
        else:
            st.warning("No matching farmers found.")
else:
    st.warning("Please log in to access the portal.")