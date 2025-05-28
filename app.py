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
st.markdown("""
    <style>
        .section {
            background-color: #ffffff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .inventory-card {
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🥫 PantryPal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Track your home supplies, get low-stock reminders, and stay organized.</p>", unsafe_allow_html=True)

# --- Add Item Form ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📋 Add Item")
with st.form("add_item"):
    item_name = st.text_input("Item name")
    quantity = st.number_input("Quantity", min_value=0, value=1)
    low_threshold = st.number_input("Low stock alert at", min_value=0, value=1)
    category = st.selectbox("Category", ["Groceries", "Cleaning", "Medicine", "Other"])
    submit = st.form_submit_button("Add")
st.markdown("</div>", unsafe_allow_html=True)

if submit and item_name:
    item = {
        "id": str(uuid.uuid4()),
        "name": item_name,
        "qty": quantity,
        "low": low_threshold,
        "category": category,
        "timestamp": datetime.now().strftime('%m/%d/%Y %H:%M')
    }
    st.session_state.inventory.append(item)
    st.success(f"✅ {item_name} added!")

# --- Display Inventory ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📦 Your Inventory")
if not st.session_state.inventory:
    st.info("No items yet. Start by adding something above.")
else:
    df = pd.DataFrame(st.session_state.inventory)
    df_display = df[["name", "qty", "low", "category", "timestamp"]]
    df_display.columns = ["Item", "Quantity", "Low Alert", "Category", "Date Added"]

    for index, row in df_display.iterrows():
        is_low = row["Quantity"] <= row["Low Alert"]
        bg_color = "#ffe6e6" if is_low else "#f0f0f0"
        st.markdown(f"""
        <div class='inventory-card' style='background-color:{bg_color};'>
        <strong>{row['Item']}</strong> ({row['Category']})<br>
        Quantity: {row['Quantity']} | Alert at: {row['Low Alert']}<br>
        <small>Added: {row['Date Added']}</small>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Download Button ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("⬇️ Download Your Inventory")
if st.session_state.inventory:
    download_df = pd.DataFrame(st.session_state.inventory)
    download_df = download_df[["name", "qty", "low", "category", "timestamp"]]
    download_df.columns = ["Item", "Quantity", "Low Alert", "Category", "Date Added"]
    download_csv = download_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=download_csv,
        file_name="pantry_inventory.csv",
        mime="text/csv"
    )
st.markdown("</div>", unsafe_allow_html=True)

# --- Future Features ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("""
### 🔜 Coming Soon:
- Email alerts for low-stock items
- Shared family/roommate accounts
- Mobile app version
- Smart suggestions and shopping list integration
""")
st.markdown("</div>", unsafe_allow_html=True)
