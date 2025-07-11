import streamlit as st

st.set_page_config(page_title="Buy Carbon Credits", layout="centered")

st.title("🛒 Buy Carbon Credits")

# Simulate user selecting a project to buy from
selected_project = st.session_state.get("selected_project", "Green Forest Initiative")

# Show summary
st.subheader(f"Buying from: 🌿 {selected_project}")
st.write("Credits Available: 10,000 tons")
st.write("Price per Credit: ₹400")
st.write("Verified by: VCS")

# Credit selection
credits_to_buy = st.number_input("Enter number of credits to purchase", min_value=1, max_value=10000, step=100)
total_cost = credits_to_buy * 400

st.markdown(f"💰 **Total Cost:** ₹{total_cost:,}")

# Confirm button
if st.button("Proceed to Payment"):
    st.session_state["pending_purchase"] = {
        "project": selected_project,
        "credits": credits_to_buy,
        "cost": total_cost
    }
    st.success(f"✅ You are purchasing {credits_to_buy} credits for ₹{total_cost:,}. Redirecting to payment gateway...")

    # Simulated redirect placeholder (replace with payment URL logic)
    st.markdown("🔗 [Click here to continue to secure payment gateway](https://example-payment.com)")
