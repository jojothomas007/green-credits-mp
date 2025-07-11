import streamlit as st
import json

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
