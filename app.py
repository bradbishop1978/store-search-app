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
if 'search_input' not in st.session_state:
    st.session_state.search_input = ""

# Input for search (store name or full address)
search_input = st.text_input("Enter Store Name or Full Address (case insensitive):", value=st.session_state.search_input)

# Clear button functionality
if st.button("Clear"):
    st.session_state.selected_store = ""
    st.session_state.search_input = ""
    search_input = ""

# Reset the selected store if search input is updated
if search_input != st.session_state.search_input:
    st.session_state.selected_store = ""
    st.session_state.search_input = search_input

# Check if the user input matches any store name or full address
if search_input:
    input_lower = search_input.lower()
    
    # Find matching stores by name
    matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]
    
    # Find matching addresses
    matching_addresses = data[data['full_address'].str.lower().str.contains(input_lower)]

    if not matching_stores.empty or not matching_addresses.empty:
        st.subheader("Suggested Matches:")

        # Combine store names and addresses into one list for suggestions
        suggestions = []

        for index, row in matching_stores.iterrows():
            suggestions.append((row['store_name'], 'store'))

        for index, row in matching_addresses.iterrows():
            suggestions.append((row['full_address'], 'address'))

        # Display suggestions with buttons
        for suggestion, suggestion_type in suggestions:
            if st.button(f"{suggestion}", key=f"{suggestion_type}_button_{suggestion}"):
                if suggestion_type == 'store':
                    st.session_state.selected_store = suggestion
                else:  # It must be an address
                    store_row = data[data['full_address'].str.lower() == suggestion.lower()].iloc[0]
                    st.session_state.selected_store = store_row['store_name']
                st.session_state.search_input = ""  # Clear input after selection
                break  # Reset suggestions on selection

    # Check if the selected store exists
    if st.session_state.selected_store:
        selected_store = st.session_state.selected_store
        filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

        if not filtered_data.empty:
            col1, col2, col3, col7 = st.columns(4)

            with col1:
                st.write("### Store Info")
                st.write("**Company:**", filtered_data['company_name'].iloc[0] if 'company_name' in filtered_data.columns else '-')
                st.write("**LSM ID:**", f"[{filtered_data['store_id'].iloc[0]}](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})" if 'store_id' in filtered_data.columns else '-')
                st.write("**Comp ID:**", filtered_data['company_id'].iloc[0] if 'company_id' in filtered_data.columns else '-')
                st.write("**Store Add:**", filtered_data['full_address'].iloc[0] if 'full_address' in filtered_data.columns else '-')

            with col2:
                st.write("### Login Info")
                st.write("**Email:**", filtered_data['email'].iloc[0] if 'email' in filtered_data.columns else '-')
                last_login_at = filtered_data['last_login_at'].iloc[0] if 'last_login_at' in filtered_data.columns else '-'
                if pd.notna(last_login_at):  # Check for valid datetime
                    login_date = pd.to_datetime(last_login_at)
                    days_since_login = (datetime.now(timezone.utc) - login_date).days
                    st.write("**Login since:**", f"{days_since_login} day{'s' if days_since_login != 1 else ''} ago")
                else:
                    st.write("**Login since:**", "-")

                st.write("**Role Name:**", filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else '-')
                st.write("**Phone No:**", filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else '-')

            with col3:
                st.write("### D S P Info")
                st.write("**UberEats ID:**", filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-')
                st.write("**DoorDash ID:**", filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-')
                st.write("**GrubHub ID:**", filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-')

            # Extract order details based on the selected store
            store_orders = order_details[order_details['store_name'].str.lower() == selected_store.lower()]

            if not store_orders.empty:
                store_orders['order_date'] = pd.to_datetime(store_orders['order_date'], errors='coerce')  # Ensure date column is parsed
                latest_order = store_orders.loc[store_orders['order_date'].idxmax()]
                elapsed_time = time_elapsed(latest_order['order_date'])  # Calculate elapsed time
                order_status = latest_order.get('status', "N/A")
                order_amount = latest_order.get('order_total', 0)
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
                    st.markdown("<span style='color:red; font-style:italic;'>No orders found for this store within 30 days.</span>", unsafe_allow_html=True)

            # Create second row of columns (4-6)
            col4, col5, col6 = st.columns(3)

            with col4:
                st.write("### Add'l info")
                st.write("**Store Email:**", filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-')
                st.write("**Store Phone:**", filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else '-')
                st.write("**Created Date:**", format_date(filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else '-'))
                store_status = filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns else None
                if store_status and isinstance(store_status, str):
                    st.markdown("**Store Status:** " + format_store_status(store_status), unsafe_allow_html=True)
                else:
                    st.markdown("**Store Status:** LSM Active", unsafe_allow_html=True)

            with col5:
                st.write("### Subscription")
                st.write("**Stripe ID:**", f"[{filtered_data['stripe_customer_id'].iloc[0]}](https://dashboard.stripe.com/customers/{filtered_data['stripe_customer_id'].iloc[0]})" if 'stripe_customer_id' in filtered_data.columns else '-')
                subs_status = filtered_data['subscription_status'].iloc[0] if 'subscription_status' in filtered_data.columns else None
                if subs_status and isinstance(subs_status, str) and subs_status.lower() == "canceled":
                    st.markdown("**Subs Status:** <span style='color:red; font-style:italic;'>Canceled</span>", unsafe_allow_html=True)
                else:
                    st.write("**Subs Status:**", format_value(subs_status if subs_status is not None else '-'))
                st.write("**Payment:**", filtered_data['payment_method'].iloc[0] if 'payment_method' in filtered_data.columns else '-')
                st.write("**Pay Period:**", format_date(filtered_data['current_period_start'].iloc[0] if 'current_period_start' in filtered_data.columns else '-'))
                st.write("**Subs Name:**", filtered_data['product_name'].iloc[0] if 'product_name' in filtered_data.columns else '-')
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

                esper_id = filtered_data['esper_id'].iloc[0] if 'esper_id' in filtered_data.columns else '-'
                device_name = filtered_data['device_name'].iloc[0] if 'device_name' in filtered_data.columns else '-'
                serial_number = filtered_data['serial_number'].iloc[0] if 'serial_number' in filtered_data.columns else '-'
                brand = filtered_data['brand'].iloc[0] if 'brand' in filtered_data.columns else '-'

                st.write("**Device Name:**", f"[{device_name}](https://ozrlk.esper.cloud/devices/{esper_id})" if esper_id != '-' else '-')
                st.write("**Serial No:**", serial_number)
                st.write("**Model:**", brand)
        else:
            st.write("No matching store found.")
