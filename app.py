import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Initialize selected_store in session state
if 'selected_store' not in st.session_state:
    st.session_state.selected_store = ""  # Initialize the selected store

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", value=st.session_state.selected_store)

# Check to see if there are matching stores based on user input
if store_name:  # Check if the search box is not empty
    input_lower = store_name.lower()
    
    # Suggest stores as the user types
    matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]
    
    # Check if there are any matching stores
    if not matching_stores.empty:
        # Show suggested stores
        st.subheader("Suggested Stores:")
        for index, row in matching_stores.iterrows():
            # Create a button for each suggested store with a unique key
            if st.button(f"{row['store_name']}", key=f"store_button_{index}"):
                # Update session state with selected store
                st.session_state.selected_store = row['store_name']
                # Update the input field directly with the selected store name
                st.session_state.store_name_input = row['store_name']
                # Use rerun to refresh the UI
                st.experimental_rerun()

# Set the input value from session state
if 'store_name_input' in st.session_state:
    store_name = st.session_state.store_name_input

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        # Display store information
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Store Information")
            store_id = filtered_data['store_id'].values[0]
            store_url = f"https://www.lulastoremanager.com/stores/{store_id}"
            st.markdown(f"**Store ID:** [**{store_id}**]({store_url})")
            st.write(f"**Company Name:** {filtered_data['company_name'].values[0]}")
            st.write(f"**Full Address:** {filtered_data['full_address'].values[0]}")

        with col2:
            st.write("### Additional Information")
            st.write(f"**Email:** {filtered_data['email'].values[0]}")
            st.write(f"**Last Login At:** {filtered_data['last_login_at'].values[0]}")
            st.write(f"**Role Name:** {filtered_data['role_name'].values[0]}")
    else:
        st.write("No matching store found.")
else:
    # Reset the selected store if nothing is in the input
    if 'selected_store' in st.session_state:
        del st.session_state.selected_store
