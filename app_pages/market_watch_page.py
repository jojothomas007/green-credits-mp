import pandas as pd
import streamlit as st

def render():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "market_watch"

    if st.session_state["current_page"] == "market_watch":
        # st.set_page_config(page_title="Buy Carbon Credits", layout="wide")
        st.title("🌿 Manage Your Carbon Credit Listings")
        
        # Add a welcome message for sellers
        st.write("Welcome to your seller dashboard! Here you can manage your existing listings or create new ones.")

        # Top deals in last month
        st.subheader("🔥 Top Deals in Last Month")
        
        top_deals = [
            {
                "buyer": "Tata Consultancy",
                "project": "SunPower Renewables",
                "credits_purchased": "800 tons",
                "price": "₹400/ton",
                "date": "2023-05-15"
            },
            {
                "buyer": "Infosys Green Initiative",
                "project": "Green Forest Initiative",
                "credits_purchased": "750 tons",
                "price": "₹350/ton",
                "date": "2023-05-12"
            },
            {
                "buyer": "Wipro Sustainability",
                "project": "SunPower Renewables",
                "credits_purchased": "400 tons",
                "price": "₹370/ton",
                "date": "2023-05-08"
            },
            {
                "buyer": "Amazon India",
                "project": "Green Forest Initiative",
                "credits_purchased": "650 tons",
                "price": "₹385/ton",
                "date": "2023-04-30"
            },
            {
                "buyer": "Mahindra Group",
                "project": "Green Forest Initiative",
                "credits_purchased": "500 tons",
                "price": "₹389/ton",
                "date": "2023-04-25"
            }
        ]
        
        # Convert list of dicts to DataFrame
        top_deals_df = pd.DataFrame(top_deals)
        
        # Display the top deals table
        st.dataframe(top_deals_df, use_container_width=True)
        
        # Sample Seller Listings (the seller's inventory)
        st.subheader("📋 Your Current Listings")

        projects = [
            {
                "id": "101",
                "price": "₹400/ton",
                "quantity": "2,500 tons",
                "status": "Active",
            },
            {
                "id": "102",
                "price": "₹350/ton",
                "quantity": "1,200 tons",
                "status": "Active",
            },
        ]

        # Convert list of dicts to DataFrame
        df = pd.DataFrame(projects)

        # Display in Streamlit
        st.dataframe(df)
        
        # Add button for creating new listings
        if st.button("➕ Create New Listing", type="primary"):
            st.session_state["current_page"] = "NewListing"
            st.rerun()
                    
    elif st.session_state["current_page"] == "NewListing":
        render_new_listing_ui()

def render_new_listing_ui():
    st.title("Create New Carbon Credit Listing")
    
    # Form for new project details
    with st.form("new_listing_form"):
        available_credits = st.text_input("Available Credits (tons)")
        credits = st.text_input("Credits to be sold (tons)")
        price = st.text_input("Price per Ton (₹)")
        submit = st.form_submit_button("Create Listing")
        
        if submit:
            if credits and price:
                st.session_state["current_page"] = "market_watch"
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    if st.button("Cancel"):
        st.session_state["current_page"] = "market_watch"
        st.rerun()