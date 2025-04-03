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
        # Display store information in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("### Store Information")
            st.write(f"**Company Name:** {filtered_data['company_name'].values[0]}")
            st.write(f"**Store ID:** [**{filtered_data['store_id'].values[0]}**](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].values[0]})")
            st.write(f"**Company ID:** {filtered_data['company_id'].values[0]}")
            st.write(f"**Full Address:** {filtered_data['full_address'].values[0]}")

        with col2:
            st.write("### LSP Login Info")
            st.write(f"**Email:** {filtered_data['store_email'].values[0]}")
            st.write(f"**Password:** (Sensitive Info)")  # If applicable, add a field here.
        
        with col3:
            st.write("### DSP Info")
            # Debugging outputs to check for missing fields
            if 'ubereats_id' in filtered_data.columns:
                st.write(f"**UberEats ID:** {filtered_data['ubereats_id'].values[0]}")
            else:
                st.write("**UberEats ID:** Not available")
            
            if 'doordash_id' in filtered_data.columns:
                st.write(f"**DoorDash ID:** {filtered_data['doordash_id'].values[0]}")
            else:
                st.write("**DoorDash ID:** Not available")
            
            if 'grubhub_id' in filtered_data.columns:
                st.write(f"**GrubHub ID:** {filtered_data['grubhub_id'].values[0]}")
            else:
                st.write("**GrubHub ID:** Not available")

        with col4:
            st.write("### Additional Details")
            # Debugging outputs to check for missing fields
            if 'store_email' in filtered_data.columns:
                st.write(f"**Store Email:** {filtered_data['store_email'].values[0]}")
            else:
                st.write("**Store Email:** Not available")
            
            if 'store_phone' in filtered_data.columns:
                st.write(f"**Store Phone:** {filtered_data['store_phone'].values[0]}")
            else:
                st.write("**Store Phone:** Not available")
            
            if 'created_date' in filtered_data.columns:
                st.write(f"**Created Date:** {filtered_data['created_date'].values[0]}")
            else:
                st.write("**Created Date:** Not available")
                
            if 'store_status' in filtered_data.columns:
                st.write(f"**Store Status:** {filtered_data['store_status'].values[0]}")
            else:
                st.write("**Store Status:** Not available")
    else:
        st.write("No matching store found.")
