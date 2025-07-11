import streamlit as st

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
