
# Load CSV data
data = pd.read_csv('merged_df.csv')
orders_data = pd.read_csv('orderdetails.csv')  # Load order details data

# Initialize session state for selected store and input
if 'selected_store' not in st.session_state:
@@ -47,54 +48,8 @@
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
# Helper functions (same as above)...
# [Include all the previously defined helper functions here]

# Display information if a specific store has been chosen
if st.session_state.selected_store:
@@ -104,7 +59,6 @@ def format_price(value):
if not filtered_data.empty:
# Create first row of columns (1-3)
col1, col2, col3 = st.columns(3)

with col1:
st.write("### Store Info")
st.write("**Company:**", format_value(filtered_data['company_name'].iloc[0]))
@@ -127,7 +81,7 @@ def format_price(value):
st.write("**GrubHub ID:**", format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'))

# Create second row of columns (4-6)
        col4, col5, col6 = st.columns(3)
        col4, col5, col6, col7 = st.columns(4)  # Change to 4 columns for new column

with col4:
st.write("### Add'l info")
@@ -183,5 +137,22 @@ def format_price(value):
st.write("**Device Name:**", f"[{format_value(device_name)}](https://ozrlk.esper.cloud/devices/{esper_id})" if esper_id != '-' else '-')
st.write("**Serial No:**", format_value(serial_number))
st.write("**Model:**", format_value(brand))  # Updated to display Brand instead of Model

        # Create the new column (7) for latest order information
        with col7:
            st.write("### Latest Order Info")

            # Filter the orders based on the selected store
            orders_filtered = orders_data[orders_data['store_name'].str.lower() == selected_store.lower()]

            if not orders_filtered.empty:
                latest_order = orders_filtered.loc[orders_filtered['order_date'].idxmax()]  # Get the latest order by date
                st.write("**Latest Order Date:**", format_date(latest_order['order_date']))
                st.write("**Order Status:**", format_value(latest_order['status']))
                st.write("**DSP:**", format_value(latest_order['dsp']))  # Replace with the actual column name for DSP
                st.write("**Amount:**", format_price(latest_order['amount']))  # Replace with the actual column name for amount
            else:
                st.write("No orders found for this store.")

else:
st.write("No matching store found.")
