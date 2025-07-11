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

    # Variable to store farmer data
    farmer_data = None

    if uploaded_file:
        try:
            # Load JSON data into a variable
            farmer_data = json.load(uploaded_file)
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    # Search Farmer Section
    if farmer_data:
        st.subheader("🔍 Search Farmer")
        search_query = st.text_input("Enter Farmer Name")
        search_button = st.button("Search")

        if search_button:
            # Extract personal_info and cultivation_info
            personal_info = farmer_data.get("personal_info", {})
            cultivation_info = farmer_data.get("cultivation_info", [])

            # Normalize both the search query and the farmer's name to lowercase and strip spaces
            search_query_normalized = search_query.strip().lower()
            farmer_name_normalized = personal_info.get("name", "").strip().lower()

            # Check if the search query matches the farmer's name
            if search_query_normalized == farmer_name_normalized:
                # Display Personal Information
                st.subheader("👤 Personal Information")
                st.write(f"**Name:** {personal_info.get('name', 'N/A')}")
                st.write(f"**Age:** {personal_info.get('age', 'N/A')}")
                st.write(f"**Country:** {personal_info.get('country', 'N/A')}")
                st.write(f"**State:** {personal_info.get('state', 'N/A')}")
                st.write(f"**Zip Code:** {personal_info.get('zip_code', 'N/A')}")

                # Display Cultivation Information
                st.subheader("🌱 Cultivation Information")
                for idx, crop in enumerate(cultivation_info, start=1):
                    st.write(f"**Crop {idx}:**")
                    st.write(f"- **Crop Type:** {crop.get('crop_type', 'N/A')}")
                    st.write(f"- **Area Size:** {crop.get('area_size', 'N/A')} acres")
                    st.write(f"- **Geo Location:** {crop.get('geo_location', 'N/A')}")

                    # Add Verify Geo Location Button
                    if f"geo_verified_{idx}" not in st.session_state:
                        st.session_state[f"geo_verified_{idx}"] = False

                    # Display Geo Location Verification Button and Status
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"Verify Geo Location for Crop {idx}"):
                            st.session_state[f"geo_verified_{idx}"] = True
                    with col2:
                        if st.session_state[f"geo_verified_{idx}"]:
                            st.success("✅ Verified")
                        else:
                            st.warning("⚠️ Not Verified")

                    # Add Quarterly Check-in Button
                    if st.button(f"Quarterly Check-in for Crop {idx}"):
                        st.session_state[f"geo_verified_{idx}"] = False
                        st.warning(f"Geo Location for Crop {idx} Not Verified ⚠️")
            else:
                st.warning("No matching farmer found. Displaying dummy data.")
                # Display Dummy Data
                st.subheader("👤 Personal Information")
                st.write("**Name:** shinoj mp")
                st.write("**Age:** 1")
                st.write("**Country:** N/A")
                st.write("**State:** N/A")
                st.write("**Zip Code:** N/A")

                # Display Dummy Cultivation Information
                st.subheader("🌱 Cultivation Information")
                dummy_cultivation_info = [
                    {
                        "crop_type": "Vegetables",
                        "area_size": "4",
                        "geo_location": "8.542374766613205, 76.86709373844825"
                    },
                    {
                        "crop_type": "Vegetables",
                        "area_size": "4",
                        "geo_location": "8.542374766613205, 76.86709373844825"
                    }
                ]
                for idx, crop in enumerate(dummy_cultivation_info, start=1):
                    st.write(f"**Crop {idx}:**")
                    st.write(f"- **Crop Type:** {crop['crop_type']}")
                    st.write(f"- **Area Size:** {crop['area_size']} acres")
                    st.write(f"- **Geo Location:** {crop['geo_location']}")

                    # Add Verify Geo Location Button
                    if f"geo_verified_dummy_{idx}" not in st.session_state:
                        st.session_state[f"geo_verified_dummy_{idx}"] = False

                    # Display Geo Location Verification Button and Status
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"Verify Geo Location for Dummy Crop {idx}"):
                            st.session_state[f"geo_verified_dummy_{idx}"] = True
                    with col2:
                        if st.session_state[f"geo_verified_dummy_{idx}"]:
                            st.success("✅ Verified")
                        else:
                            st.warning("⚠️ Not Verified")

                    # Add Quarterly Check-in Button
                    if st.button(f"Quarterly Check-in for Dummy Crop {idx}"):
                        st.session_state[f"geo_verified_dummy_{idx}"] = False
                        st.warning(f"Geo Location for Dummy Crop {idx} Not Verified ⚠️")
else:
    st.warning("Please log in to access the portal.")