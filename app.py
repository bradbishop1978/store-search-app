import streamlit as st
import pandas as pd
from datetime import datetime, timezone

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

# Helper function to format values
def format_value(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

# Helper function to format prices in dollar format
def format_price(value):
    if pd.isna(value):
        return "$0.00"
    try:
        return f"${value / 100:.2f}"  # Divide by 100 for cents
    except ValueError:
        return "$0.00"

# Helper function to format dates to MM/DD/YYYY
def format_date(date_value):
    if pd.isna(date_value):
        return "-"
    date_value = pd.to_datetime(date_value, errors='coerce')  # Convert to datetime
    return date_value.strftime('%m/%d/%Y') if date_value else "-"

# Helper function to calculate relative time since order
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

# Helper function to format the store status
def format_store_status(status):
    return status if status and status != "-" else "LSM Active"

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        col1, col2, col3, col7 = st.columns(4)

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
            st.write("**Login since:**", last_login_at)
            st.write("**Role Name:**", format_value(filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else '-'))
            st.write("**Phone No:**", format_value(filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else '-'))

        with col3:
            st.write("### D S P Info")
            st.write("**UberEats ID:**", format_value(filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-'))
            st.write("**DoorDash ID:**", format_value(filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-'))
            st.write("**GrubHub ID:**", format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'))

        # Extract order details based on the selected store
        store_orders = order_details[order_details['store_name'].str.lower() == selected_store.lower()]

        if not store_orders.empty:
            # Sort orders by date to get the latest one
            store_orders['order_date'] = pd.to_datetime(store_orders['order_date'], errors='coerce')  # Ensure date column is parsed
            latest_order = store_orders.loc[store_orders['order_date'].idxmax()]
        
            # Extract the latest order details
            elapsed_time = time_elapsed(latest_order['order_date'])  # Calculate elapsed time
            order_status = latest_order.get('status', "N/A")
            order_amount = latest_order.get('order_total', 0)  # Get the actual order total value
            order_amount_str = f"${order_amount:.2f}" if order_amount else "$0.00"  # Show as dollar amount
            dsp = format_value(latest_order.get('delivery_platform', '-'))

            with col7:
                st.write("### Last Order Info")
                st.write("**Order since:**", elapsed_time)  # Display time since order
                st.write("**Status:**", format_value(order_status))
                st.write("**Amount:**", order_amount_str)  # Show correct amount directly
                st.write("**DSP:**", format_value(dsp))
        else:
            with col7:
                st.write("### Last Order Info")
                st.write("No orders found for this store within 30 days.")

        # Create second row of columns (4-6)
        col4, col5, col6 = st.columns(3)

        with col4:
            st.write("### Add'l info")
            st.write("**Store Email:**", format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-'))
            st.write("**Store Phone:**", format_value(filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else '-'))
            st.write("**Created Date:**", format_date(filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else '-'))
            
            # Use the modified format_store_status function
            store_status = filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns else None
            st.markdown("**Store Status:** " + format_store_status(store_status), unsafe_allow_html=True)

        with col5:
            st.write("### Subscription")
            st.write("**Stripe ID:**", f"[{format_value(filtered_data['stripe_customer_id'].iloc[0])}](https://dashboard.stripe.com/customers/{filtered_data['stripe_customer_id'].iloc[0]})")
            
            # Handle subscription status
            subs_status = filtered_data['subscription_status'].iloc[0] if 'subscription_status' in filtered_data.columns else None
            if subs_status and isinstance(subs_status, str) and subs_status.lower() == "canceled":
                st.markdown("**Subs Status:** <span style='color:red; font-style:italic;'>Canceled</span>", unsafe_allow_html=True)
            else:
                st.write("**Subs Status:**", format_value(subs_status if subs_status is not None else '-'))

            st.write("**Payment:**", format_value(filtered_data['payment_method'].iloc[0] if 'payment_method' in filtered_data.columns else '-'))
            st.write("**Pay Period:**", format_date(filtered_data['current_period_start'].iloc[0] if 'current_period_start' in filtered_data.columns else '-'))
            st.write("**Subs Name:**", format_value(filtered_data['product_name'].iloc[0] if 'product_name' in filtered_data.columns else '-'))
            st.write("**Amount:**", format_price(filtered_data['price_amount'].iloc[0] if 'price_amount' in filtered_data.columns else '-'))

        with col6:
            st.write("### Device Info")
            device_status = filtered_data['status'].iloc[0] if 'status' in filtered_data.columns else None
            if device_status and isinstance(device_status, str):
                if device_status.lower() == "online":
                    st.markdown("**Status:** <span style='color:green; font-weight:bold;'>Online</span>", unsafe_allow_html=True)
                elif device_status.lower() == "offline":
                    st.markdown("**Status:** <span style='color:red; font-style:italic;'>Offline</span>", unsafe_allow_html=True)
                else:
                    st.write("**Status:**", device_status)
            else:
                st.write("**Status:**", "-")

            # Remaining device info
            esper_id = filtered_data['esper_id'].iloc[0] if 'esper_id' in filtered_data.columns else '-'
            device_name = filtered_data['device_name'].iloc[0] if 'device_name' in filtered_data.columns else '-'
            serial_number = filtered_data['serial_number'].iloc[0] if 'serial_number' in filtered_data.columns else '-'
            brand = filtered_data['brand'].iloc[0] if 'brand' in filtered_data.columns else '-'  # Assuming you meant to display brand

            st.write("**Device Name:**", f"[{format_value(device_name)}](https://ozrlk.esper.cloud/devices/{esper_id})" if esper_id != '-' else '-')
            st.write("**Serial No:**", format_value(serial_number))
            st.write("**Model:**", format_value(brand))  # Updated to display Brand instead of Model
    else:
        st.write("No matching store found.")
