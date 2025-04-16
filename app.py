import streamlit as st
import pandas as pd
from datetime import datetime, timezone

# Logo URL
logo_url = "https://raw.githubusercontent.com/bradbishop1978/store-search-app/16a6f28ccce5db3711f78c060c1f29b98a84f8c1/Primary%20Logo.jpg"

# Create a single column for the logo and title
col = st.container()

with col:
    # Use HTML to align the logo and title
    st.markdown(
        f"""
        <div style="display: flex; align-items: center;">
            <img src="{logo_url}" width="150" height="60" style="margin-right: 50px;">
            <h1 style="margin: 0;">Store Information Search</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load CSV data
try:
    data = pd.read_csv('merged_df.csv')
except FileNotFoundError:
    st.error("Store data file not found. Please ensure 'merged_df.csv' is in the correct path.")
    st.stop()

# Load additional CSV data
try:
    order_details = pd.read_csv('orderdetails.csv')
except FileNotFoundError:
    st.error("Order details file not found. Please ensure 'orderdetails.csv' is in the correct path.")
    st.stop()

# Initialize session state for selected store and input
if 'selected_store' not in st.session_state:
    st.session_state.selected_store = ""
if 'store_name_input' not in st.session_state:
    st.session_state.store_name_input = ""
if 'full_address_input' not in st.session_state:
    st.session_state.full_address_input = ""

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", value=st.session_state.store_name_input)

# Additional input for full address
full_address = st.text_input("Enter Full Address (case insensitive):", value=st.session_state.full_address_input)

# Clear button functionality
if st.button("Clear"):
    st.session_state.selected_store = ""
    st.session_state.store_name_input = ""
    st.session_state.full_address_input = ""
    store_name = ""
    full_address = ""

# Reset the selected store if either the store name or full address is typed
if store_name != st.session_state.store_name_input or full_address != st.session_state.full_address_input:
    st.session_state.selected_store = ""
    st.session_state.store_name_input = store_name
    st.session_state.full_address_input = full_address

# Check if the user input matches any store name exactly
if store_name:
    input_lower = store_name.lower()
    exact_match = data[data['store_name'].str.lower() == input_lower]

    if not exact_match.empty:
        st.session_state.selected_store = exact_match['store_name'].iloc[0]  # Update selected store

    # Suggest stores if there's no exact match
    if st.session_state.selected_store == "":
        matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]
        if not matching_stores.empty:
            st.subheader("Suggested Stores:")
            for index, row in matching_stores.iterrows():
                if st.button(f"{row['store_name']}", key=f"store_button_{index}"):
                    st.session_state.selected_store = row['store_name']
                    st.session_state.store_name_input = row['store_name']
                    st.session_state.full_address_input = ""  # Clear address input
                    break  # Reset suggestions on selection

# Check if the user input matches any full address
if full_address:
    input_full_address_lower = full_address.lower()
    matching_addresses = data[data['full_address'].str.lower().str.contains(input_full_address_lower)]

    if not matching_addresses.empty:
        st.subheader("Suggested Addresses:")
        for index, row in matching_addresses.iterrows():
            if st.button(f"{row['full_address']}", key=f"address_button_{index}"):
                # When an address is selected, set the corresponding store
                st.session_state.selected_store = row['store_name']
                st.session_state.store_name_input = row['store_name']
                st.session_state.full_address_input = ""  # Clear address input
                break  # Reset suggestions on selection

# Assign values for the text inputs from the session state
store_name = st.session_state.store_name_input
full_address = st.session_state.full_address_input

# Helper functions for formatting
def format_value(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def format_price(value):
    if pd.isna(value):
        return "$0.00"
    try:
        return f"${value / 100:.2f}"  # Divide by 100 for cents
    except ValueError:
        return "$0.00"

def format_date(date_value):
    if pd.isna(date_value):
        return "-"
    date_value = pd.to_datetime(date_value, errors='coerce')  # Convert to datetime
    return date_value.strftime('%m/%d/%Y') if date_value else "-"

def time_elapsed(order_date):
    if pd.isna(order_date):
        return "-"
    order_date = pd.to_datetime(order_date)  # Convert to datetime
    now = datetime.now(timezone.utc)  # Current UTC time
    delta = now - order_date

    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
    elif delta.seconds // 3600 > 0:
        return f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 != 1 else ''} ago"
    elif delta.seconds // 60 > 0:
        return f"{delta.seconds // 60} minute{'s' if delta.seconds // 60 != 1 else ''} ago"
    else:
        return "Just now"

def format_store_status(status):
    if status == "Offboard":
        return "<span style='color:red; font-style:italic;'>Offboard</span>"
    return status if status and status != "-" else "LSM Active"

# Create the "Location Status" column by concatenating the necessary columns
def get_location_status(row):
    return f"{row.get('store_location_pipeline_stage', '')} | {row.get('onboarding_status', '')} | {row.get('company_classification', '')} | {row.get('account_manager', '')} | {format_date(row.get('date_live', ''))} | {format_date(row.get('churned_date', ''))}"

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        col1, col2, col3, col4 = st.columns(4)  # Modify columns to include 4th column for Location Status

        with col1:
            st.write("### Store Info")
            st.write("**Company:**", format_value(filtered_data['company_name'].iloc[0] if 'company_name' in filtered_data.columns else '-'))
            st.write("**LSM ID:**", f"[{format_value(filtered_data['store_id'].iloc[0])}](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})" if 'store_id' in filtered_data.columns else '-')
            st.write("**Comp ID:**", format_value(filtered_data['company_id'].iloc[0] if 'company_id' in filtered_data.columns else '-'))
            st.write("**Store Add:**", format_value(filtered_data['full_address'].iloc[0] if 'full_address' in filtered_data.columns else '-'))

        with col2:
            st.write("### Location Status")
            location_status = get_location_status(filtered_data.iloc[0])  # Get combined status
            st.write(location_status)

        with col3:
            st.write("### DSP Info")
            st.write("**UberEats ID:**", format_value(filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-'))
            st.write("**DoorDash ID:**", format_value(filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-'))
            st.write("**GrubHub ID:**", format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'))

        # Add your existing code below for Last Order Info, Add'l Info, Subscription, Device Info
        # (Ensure you do not alter the bottom part of the code you already have)

    else:
        st.write("No matching store found.")
