import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Initialize selected_store and input in session state
if 'selected_store' not in st.session_state:
    st.session_state.selected_store = ""  # Initialize the selected store

if 'store_name_input' not in st.session_state:
    st.session_state.store_name_input = ""  # Initialize input

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", value=st.session_state.store_name_input)

# Reset the session state if the user starts typing a new query
if store_name != st.session_state.store_name_input:
    st.session_state.selected_store = ""  # Clear previous selection
    st.session_state.store_name_input = store_name  # Update current input

# Suggest stores as the user types
if store_name:  # Check if the search box is not empty
    input_lower = store_name.lower()
    
    # Suggest stores
    matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]
    
    # Only show suggested stores if no selection has been made
    if st.session_state.selected_store == "":
        if not matching_stores.empty:
            st.subheader("Suggested Stores:")
            for index, row in matching_stores.iterrows():
                # Create a button for each suggested store with a unique key
                if st.button(f"{row['store_name']}", key=f"store_button_{index}"):
                    # Update session state with selected store and input
                    st.session_state.selected_store = row['store_name']
                    st.session_state.store_name_input = row['store_name']  # Update input field

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
