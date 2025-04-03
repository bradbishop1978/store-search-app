import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", "")

if store_name:
    # Get the lowercase version of the input for case insensitive search
    input_lower = store_name.lower()
    
    # Filter store names based on the current input
    matching_stores = data[data['store_name'].str.lower().str.contains(input_lower)]
    
    # Suggest store names as a user types
    if not matching_stores.empty:
        st.subheader("Suggested Stores:")
        for index, row in matching_stores.iterrows():
            # Display matching store names for user to choose
            st.write(f"- {row['store_name']}", unsafe_allow_html=True)
    
    # Further filtering
    filtered_data = matching_stores[matching_stores['store_name'].str.lower() == input_lower]
    
    if not filtered_data.empty:
        # Store information display
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
