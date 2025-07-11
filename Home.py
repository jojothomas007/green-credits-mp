import streamlit as st

st.set_page_config(page_title="Carbon Credit Hub", layout="wide")
st.title("🌿 Carbon Credit Marketplace - Home")

# Hero Section
st.markdown("""
## Welcome to Your Carbon Offset Dashboard
Helping industries transition to a greener future 🌍
""")

# Highlight Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Credits Owned", "4,500 tons", delta="+500 this month")
    st.progress(0.45)

with col2:
    st.metric("Credits Purchased", "₹18,00,000")
    st.success("🌟 Verified Buyer Status")

with col3:
    st.metric("Total Offset", "4,500 tons CO₂")
    st.caption("Equivalent to planting 7,200 trees 🌲")

# Recent Activity
st.subheader("📊 Recent Transactions")
st.table([
    {"Date": "2025-07-10", "Project": "Green Forest Initiative", "Credits": 1000, "Cost": "₹4,00,000"},
    {"Date": "2025-06-22", "Project": "SunPower Renewables", "Credits": 800, "Cost": "₹2,80,000"},
])

# Marketplace Stats
st.subheader("🌐 Marketplace Stats")
st.markdown("""
- 🏷 Total Verified Projects: **42**
- 💰 Average Price per Credit: **₹410**
- 🌎 Global Participants: **120+ Industrial Buyers**
""")

# Call-to-Action
st.markdown("---")
st.markdown("🎯 **Ready to offset more emissions?** [Explore Projects →](#)")
