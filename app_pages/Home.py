import streamlit as st

def render():
    st.set_page_config(page_title="Carbon Credit Hub", layout="wide")
    st.title("🌿 Carbon Credit Marketplace - Home")

    # Hero Section
    st.markdown("""
    ## Welcome to Your Carbon Credit Seller Dashboard
    Monetize your sustainability initiatives and help industries go green 🌍
    """)

    # Highlight Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Credits Generated", "4,500 tons", delta="+500 this month")
        st.progress(0.45)

    with col2:
        st.metric("Credits Sold", "₹18,00,000")
        st.success("🌟 Verified Seller Status")

    with col3:
        st.metric("Total Impact", "4,500 tons CO₂")
        st.caption("Your projects have offset emissions equal to 7,200 trees 🌲")

    # Recent Activity
    st.subheader("📊 Recent Sales")
    st.table([
        {"Date": "2025-07-10", "Buyer": "EcoTech Industries", "Credits": 1000, "Revenue": "₹4,00,000"},
        {"Date": "2025-06-22", "Buyer": "GreenManufacturing Ltd", "Credits": 800, "Revenue": "₹2,80,000"},
    ])

    # Marketplace Stats
    st.subheader("🌐 Marketplace Stats")
    st.markdown("""
    - 🏷 Your Verified Projects: **3**
    - 💰 Your Average Selling Price: **₹410 per Credit**
    - 🌎 Potential Buyers: **120+ Industrial Companies**
    """)

    # Call-to-Action
    st.markdown("---")
    st.markdown("🎯 **Ready to list more carbon credits?** [Create New Project →](#)")
