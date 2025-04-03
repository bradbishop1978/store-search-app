import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Input for store name with an empty value to manage selected store
store_name = st.text_input("Enter Store Name (case insensitive):", "")

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
            # Create a button for each suggested store
            if st.button(f"{row['store_name']}"):
                store_name = row['store_name']  # Set the store_name to the selected store

        # Clear displayed suggestions if a suggestion is chosen
        # This is done through re-running the script with the current `store_name`
        st.session_state.selected_store = store_name  # Save selected store
            
# Display information if a specific store has been chosen
if 'selected_store' in st.session_state and st.session_state.selected_store:
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
