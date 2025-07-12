import pandas as pd
import streamlit as st
from app_pages.Payment import render_payment_ui

def render():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "market_watch"

    if st.session_state["current_page"] == "market_watch":
        # st.set_page_config(page_title="Buy Carbon Credits", layout="wide")
        st.title("🛒 Browse Carbon Credits from Verified Sellers")

        # # Filters
        # st.sidebar.header("🔍 Filter Listings")
        # location = st.sidebar.selectbox("Location", ["All", "India", "Brazil", "Kenya", "USA"])
        # credit_type = st.sidebar.multiselect("Project Type", ["Afforestation", "Solar", "Wind", "Methane Capture"])
        # verification = st.sidebar.radio("Verified By", ["All", "Gold Standard", "VCS"])

        # Sample Listings
        st.subheader("📋 Top Deals on Carbon Credit Listings")

        projects = [
            {
                "id": "101",
                "name": "Green Forest Initiative",
                "type": "Afforestation",
                "location": "Assam, India",
                "credits": "10,000 tons",
                "price": "₹400/ton",
                "verified_by": "VCS",
                "rating": "⭐⭐⭐⭐☆"
            },
            {
                "id": "102",
                "name": "SunPower Renewables",
                "type": "Solar",
                "location": "Rajasthan, India",
                "credits": "8,000 tons",
                "price": "₹350/ton",
                "verified_by": "Gold Standard",
                "rating": "⭐⭐⭐⭐⭐"
            }
        ]

        # Convert list of dicts to DataFrame
        df = pd.DataFrame(projects)

        # Display in Streamlit
        st.dataframe(df)

        # Let user select a project
        project_names = [f"{p['id']} - {p['name']}" for p in projects]
        selected_value = st.selectbox("🌿 Select a project to buy credits from", project_names)

        # Common Buy button
        if st.button("Buy Selected Credits"):
            selected_project = next(p for p in projects if f"{p['id']} - {p['name']}" == selected_value)
            # st.success(f"You bought credits from **{selected_project['name']}** located in {selected_project['location']} 🌱")
            st.session_state["selected_project"] = selected_project
            # st.switch_page("pages/Payment.py")  # Navigates to payment page
            st.session_state["current_page"] = "Payment"
            # render_payment_ui(selected_project)
            st.rerun()
    else:
        # st.session_state["current_page"] = "Payment"
        render_payment_ui(st.session_state["selected_project"])