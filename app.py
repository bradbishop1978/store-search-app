import streamlit as st
import pandas as pd

# Load the CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Search input for a specific store name (case insensitive)
store_name = st.text_input("Enter Store Name (case insensitive):", "")

# Displaying related information
if store_name:
    # Filter data based on the entered store name (case insensitive)
    filtered_data = data[data['store_name'].str.lower() == store_name.lower()]
    
        # Create two columns for layout
        col1, col2 = st.columns(2)

        # Left Column: Display store_id, company_name, full_address with a hyperlink
        with col1:
            st.write("### Store Information")
            store_id = filtered_data['store_id'].values[0]  # Get the store ID
            store_url = f"https://www.lulastoremanager.com/stores/{store_id}"  # Construct the URL
            st.markdown(f"**Store ID:** [**{store_id}**]({store_url})")  # Create a clickable link with bold text
            st.write(f"**Company Name:** {filtered_data['company_name'].values[0]}")
            st.write(f"**Full Address:** {filtered_data['full_address'].values[0]}")

        # Right Column: Display email, last_login_at, role_name
        with col2:
            st.write("### Additional Information")
            st.write(f"**Email:** {filtered_data['email'].values[0]}")
            st.write(f"**Last Login At:** {filtered_data['last_login_at'].values[0]}")
            st.write(f"**Role Name:** {filtered_data['role_name'].values[0]}")
            
    else:
        st.write("No matching store found.")
