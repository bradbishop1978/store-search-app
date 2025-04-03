import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

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
                # Create a button for each suggested store with a unique key
                if st.button(f"{row['store_name']}", key=f"store_button_{index}"):
                    st.session_state.selected_store = row['store_name']
                    st.session_state.store_name_input = row['store_name']

# Set the input value from session state
store_name = st.session_state.store_name_input

# Helper function to replace NaN with '-'
def format_value(value):
    if pd.isna(value):
        return "-"
    if isinstance(value, float) and value.is_integer():  # Check if float is essentially an integer
        return str(int(value))  # Convert to int for no decimal
    return str(value)  # Return as string for all other types

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        st.write("### Store Details")

        # Create a data structure for display
        detailed_info = {
            "Company Name": format_value(filtered_data['company_name'].iloc[0]),
            "Store ID": f"[{format_value(filtered_data['store_id'].iloc[0])}](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})",
            "Company ID": format_value(filtered_data['company_id'].iloc[0]),
            "Full Address": format_value(filtered_data['full_address'].iloc[0]),
            "Email": format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-'),
            "Last Login At": format_value(filtered_data['last_login_at'].iloc[0] if 'last_login_at' in filtered_data.columns else '-'),
            "Role Name": format_value(filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else '-'),
            "Phone Number": format_value(filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else '-'),
            "UberEats ID": format_value(filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-'),
            "DoorDash ID": format_value(filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-'),
            "GrubHub ID": format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'),
            "Store Email": format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-'),
            "Store Phone": format_value(filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else '-'),
            "Created Date": format_value(filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else '-'),
            "Store Status": format_value(filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns else '-'),
        }

        # Create a formatted table
        st.write("| Field          | Value                                                   |")
        st.write("|----------------|---------------------------------------------------------|")
        for field, value in detailed_info.items():
            st.write(f"| **{field}:**      | {value}                                      |")

    else:
        st.write("No matching store found.")
