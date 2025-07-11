import streamlit as st

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
