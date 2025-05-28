# PantryPal MVP - Web App (Mobile-Optimized) using Streamlit + Supabase

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

# --- Session State Setup ---
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# --- App Header ---
st.set_page_config(page_title="PantryPal", layout="centered")
st.title("🥫 PantryPal")
st.markdown("Track your home supplies, get low-stock reminders, and stay organized.")

# --- Add Item Form ---
st.subheader("📋 Add Item")
with st.form("add_item"):
    item_name = st.text_input("Item name")
    quantity = st.number_input("Quantity", min_value=0, value=1)
    low_threshold = st.number_input("Low stock alert at", min_value=0, value=1)
    category = st.selectbox("Category", ["Groceries", "Cleaning", "Medicine", "Other"])
    submit = st.form_submit_button("Add")

if submit and item_name:
    item = {
        "id": str(uuid.uuid4()),
        "name": item_name,
        "qty": quantity,
        "low": low_threshold,
        "category": category,
        "timestamp": datetime.now()
    }
    st.session_state.inventory.append(item)
    st.success(f"✅ {item_name} added!")

# --- Display Inventory ---
st.subheader("📦 Your Inventory")
if not st.session_state.inventory:
    st.info("No items yet. Start by adding something above.")
else:
    df = pd.DataFrame(st.session_state.inventory)
    df_display = df[["name", "qty", "low", "category"]]
    df_display.columns = ["Item", "Quantity", "Low Alert", "Category"]

    for index, row in df_display.iterrows():
        is_low = row["Quantity"] <= row["Low Alert"]
        color = "#ffe6e6" if is_low else "#f0f0f0"
        st.markdown(f"""
        <div style='padding:10px;margin:5px;background-color:{color};border-radius:10px;'>
        <strong>{row['Item']}</strong> ({row['Category']})<br>
        Quantity: {row['Quantity']} | Alert at: {row['Low Alert']}
        </div>
        """, unsafe_allow_html=True)

# --- Download Button ---
st.subheader("⬇️ Download Your Inventory")
download_df = pd.DataFrame(st.session_state.inventory)
download_df = download_df[["name", "qty", "low", "category", "timestamp"]]  # Remove 'id' before download
download_csv = download_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=download_csv,
    file_name="pantry_inventory.csv",
    mime="text/csv"
)

# --- Future Features ---
st.markdown("""
---
### 🔜 Coming Soon:
- Email alerts for low-stock items
- Shared family/roommate accounts
- Mobile app version
- Smart suggestions and shopping list integration
""")
