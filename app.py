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

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        # Create a full-width container for columns
        with st.container():
            # Create columns that span full width
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])  # Adjust proportions as needed

            with col1:
                st.write("### Store Information")
                st.write(f"**Company Name:** {filtered_data['company_name'].iloc[0]}")
                st.write(f"**Store ID:** [**{filtered_data['store_id'].iloc[0]}**](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})")
                st.write(f"**Company ID:** {filtered_data['company_id'].iloc[0]}")
                st.write(f"**Full Address:** {filtered_data['full_address'].iloc[0]}")

            with col2:
                st.write("### LSP Login Info")
                st.write(f"**Email:** {filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else 'Not available'}")
                st.write(f"**Last Login At:** {filtered_data['last_login_at'].iloc[0] if 'last_login_at' in filtered_data.columns else 'Not available'}")
                st.write(f"**Role Name:** {filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else 'Not available'}")
                st.write(f"**Phone Number:** {filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else 'Not available'}")

            with col3:
                st.write("### DSP Info")
                st.write(f"**UberEats ID:** {filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else 'Not available'}")
                st.write(f"**DoorDash ID:** {filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else 'Not available'}")
                st.write(f"**GrubHub ID:** {filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else 'Not available'}")

            with col4:
                st.write("### Additional Details")
                st.write(f"**Store Email:** {filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else 'Not available'}")
                st.write(f"**Store Phone:** {filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else 'Not available'}")
                st.write(f"**Created Date:** {filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else 'Not available'}")
                st.write(f"**Store Status:** {filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns else 'Not available'}")
    else:
        st.write("No matching store found.")
