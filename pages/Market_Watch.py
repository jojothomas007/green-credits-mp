import streamlit as st

st.set_page_config(page_title="Buy Carbon Credits", layout="wide")
st.title("🛒 Browse Carbon Credits from Verified Sellers")

# Filters
st.sidebar.header("🔍 Filter Listings")
location = st.sidebar.selectbox("Location", ["All", "India", "Brazil", "Kenya", "USA"])
credit_type = st.sidebar.multiselect("Project Type", ["Afforestation", "Solar", "Wind", "Methane Capture"])
verification = st.sidebar.radio("Verified By", ["All", "Gold Standard", "VCS"])

# Sample Listings
st.subheader("📋 Available Carbon Credit Listings")

projects = [
    {
        "name": "Green Forest Initiative",
        "type": "Afforestation",
        "location": "Assam, India",
        "credits": "10,000 tons",
        "price": "₹400/ton",
        "verified_by": "VCS",
        "rating": "⭐⭐⭐⭐☆"
    },
    {
        "name": "SunPower Renewables",
        "type": "Solar",
        "location": "Rajasthan, India",
        "credits": "8,000 tons",
        "price": "₹350/ton",
        "verified_by": "Gold Standard",
        "rating": "⭐⭐⭐⭐⭐"
    }
]

for project in projects:
    with st.container():
        st.markdown(f"### 🌱 {project['name']}")
        st.write(f"Type: {project['type']} | Location: {project['location']}")
        st.write(f"Credits Available: {project['credits']} | Price: {project['price']}")
        st.write(f"Verified by: {project['verified_by']} | Rating: {project['rating']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button(f"View Details - {project['name']}")
        with col2:
            st.button(f"Buy Credits - {project['name']}")

st.markdown("---")
st.info("⚠️ Note: Prices may vary based on market conditions. Credits are subject to evaluator verification.")