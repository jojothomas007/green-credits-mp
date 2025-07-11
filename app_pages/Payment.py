import streamlit as st
import app_pages.Market_Watch as market

def render_payment_ui(project):
    st.set_page_config(page_title="Buy Carbon Credits", layout="centered")

    st.title("🛒 Buy Carbon Credits")

    # Simulate user selecting a project to buy from
    selected_project = st.session_state.get("selected_project", "Green Forest Initiative")

    # Show summary
    st.subheader(f"Buying from: 🌿 {selected_project["name"]}")
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
        st.success(f"✅ Payment debited successfully. You have purchased {credits_to_buy} credits for ₹{total_cost:,}.")

        st.info("⚠️ Note: In real application, you will be taken to payment gateway.")
    
    if st.button("Return to Market Watch", key="return_btn", type="primary"):
        st.session_state["current_page"] = "market_watch"
        st.rerun()
