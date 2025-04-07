import streamlit as st
import pandas as pd
from datetime import datetime

# Correct raw URL of your logo
logo_url = "https://raw.githubusercontent.com/bradbishop1978/store-search-app/main/Primary%20Logo.jpg"

# Use Markdown with HTML for inline logo
st.markdown(
    f"<div style='display: flex; align-items: center;'>"
    f"<h1 style='margin-right: 10px;'>Store Information Search</h1>"
    f"<img src='{logo_url}' style='height:50px;'>"
    f"</div>",
    unsafe_allow_html=True
)

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Initialize session state for selected store and input
if 'selected_store' not in st.session_state:
    st.session_state.selected_store = ""
if 'store_name_input' not in st.session_state:
    st.session_state.store_name_input = ""

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", value=st.session_state.store_name_input)

# Reset the session state if the user starts typing a new query
if store_name != st.session_state.store_name_input:
    st.session_state.selected_store = ""
    st.session_state.store_name_input = store_name

# Suggest stores as the user types
if store_name:
    input_lower = store_name.lower()
    matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]

    if st.session_state.selected_store == "":
        if not matching_stores.empty:
            st.subheader("Suggested Stores:")
            for index, row in matching_stores.iterrows():
                if st.button(f"{row['store_name']}", key=f"store_button_{index}"):
                    st.session_state.selected_store = row['store_name']
                    st.session_state.store_name_input = row['store_name']

# Set the input value from session state
store_name = st.session_state.store_name_input

# Helper function to replace NaN with '-'
def format_value(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

# Helper function to handle store status display
def format_store_status(status):
    if pd.isna(status) or status == "":
        return "LSM Active"
    return status

# Helper function to format dates
def format_date(date_str):
    try:
        dt = pd.to_datetime(date_str)
        return dt.strftime('%m/%d/%Y')
    except Exception:
        return "-"

# Helper function to calculate days since last login
def days_since_last_login(last_login_str):
    if pd.isna(last_login_str) or last_login_str == "-":
        return "Not logged in"
    try:
        last_login = pd.to_datetime(last_login_str)
        last_login_naive = last_login.tz_localize(None)
        delta = datetime.now() - last_login_naive
        return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
    except Exception as e:
        st.write(f"Error parsing last login date: {e}")
        return "Not logged in"

# Helper function to format price in dollar format
def format_price(value):
    if pd.isna(value):
        return "$0.00"
    try:
        if value >= 100:
            dollars = value / 100
        else:
            dollars = value / 10

        return f"${dollars:,.2f}"
    except ValueError:
        return "$0.00"

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        # Create first row of columns (1-3)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("### Store Info")
            st.write("**Company:**", format_value(filtered_data['company_name'].iloc[0]))
            st.write("**LSM ID:**", f"[{format_value(filtered_data['store_id'].iloc[0])}](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})")
            st.write("**Comp ID:**", format_value(filtered_data['company_id'].iloc[0]))
            st.write("**Store Add:**", format_value(filtered_data['full_address'].iloc[0]))

        with col2:
            st.write("### Login Info")
            st.write("**Email:**", format_value(filtered_data['email'].iloc[0] if 'email' in filtered_data.columns else '-'))
            last_login_at = filtered_data['last_login_at'].iloc[0] if 'last_login_at' in filtered_data.columns else '-'
            st.write("**Login since:**", days_since_last_login(last_login_at))
            st.write("**Role Name:**", format_value(filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else '-'))
            st.write("**Phone No:**", format_value(filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else '-'))

        with col3:
            st.write("### D S P Info")
            st.write("**UberEats ID:**", format_value(filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-'))
            st.write("**DoorDash ID:**", format_value(filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-'))
            st.write("**GrubHub ID:**", format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'))

        # Create second row of columns (4-6)
        col4, col5, col6 = st.columns(3)

        with col4:
            st.write("### Add'l info")
            st.write("**Store Email:**", format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-'))
            st.write("**Store Phone:**", format_value(filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else '-'))
            st.write("**Created Date:**", format_date(filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else '-'))
            
            # Get store_status with error handling
            store_status = filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns and not filtered_data['store_status'].empty else None
            if store_status is not None and isinstance(store_status, str) and store_status.lower() == "offboard":
                st.markdown("**Store Status:** <span style='color:red; font-style:italic;'>Offboard</span>", unsafe_allow_html=True)
            else:
                st.write("**Store Status:**", format_store_status(store_status if store_status is not None else '-'))
        
        with col5:
            st.write("### Subscription")
            st.write("**Stripe ID:**", f"[{format_value(filtered_data['stripe_customer_id'].iloc[0])}](https://dashboard.stripe.com/customers/{filtered_data['stripe_customer_id'].iloc[0]})")
        
            # Get subs_status with error handling
            subs_status = filtered_data['subscription_status'].iloc[0] if 'subscription_status' in filtered_data.columns and not filtered_data['subscription_status'].empty else None
            if subs_status is not None and isinstance(subs_status, str) and subs_status.lower() == "canceled":
                st.markdown("**Subs Status:** <span style='color:red; font-style:italic;'>Canceled</span>", unsafe_allow_html=True)
            else:
                st.write("**Subs Status:**", format_value(subs_status if subs_status is not None else '-'))
        
            st.write("**Payment:**", format_value(filtered_data['payment_method'].iloc[0] if 'payment_method' in filtered_data.columns else '-'))
            st.write("**Pay Period:**", format_date(filtered_data['current_period_start'].iloc[0] if 'current_period_start' in filtered_data.columns else '-'))
            st.write("**Subs Name:**", format_value(filtered_data['product_name'].iloc[0] if 'product_name' in filtered_data.columns else '-'))
            st.write("**Amount:**", format_price(filtered_data['price_amount'].iloc[0] if 'price_amount' in filtered_data.columns else '-'))

         with col6:
            st.write("### Device Info")  # Header for the new column
            
            # Get device status with error handling
            device_status = filtered_data['status'].iloc[0] if 'status' in filtered_data.columns and not filtered_data['status'].empty else None
            if device_status is not None and isinstance(device_status, str):
                if device_status.lower() == "online":
                    st.markdown("**Status:** <span style='color:green;'>Online</span>", unsafe_allow_html=True)
                elif device_status.lower() == "offline":
                    st.markdown("**Status:** <span style='color:red; font-style:italic;'>Offline</span>", unsafe_allow_html=True)
                else:
                    st.write("**Status:**", device_status)  # Fallback for any other status
            else:
                st.write("**Status:**", "-")  # Handle case when status is None or not available
        
            # Remaining device info
            st.write("**Device Name:**", f"[{format_value(device_name)}](https://ozrlk.esper.cloud/devices/{esper_id})" if esper_id != '-' else '-')
            st.write("**Serial No:**", format_value(serial_number))
            st.write("**Model:**", format_value(brand))  # Updated to display Brand instead of Model

    else:
        st.write("No matching store found.")
