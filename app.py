import streamlit as st
import pandas as pd

# Load CSV data
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Input for store name
store_name = st.text_input("Enter Store Name (case insensitive):", "")

if store_name:
    # Filtering based on store name
    filtered_data = data[data['store_name'].str.lower() == store_name.lower()]
    
    if not filtered_data.empty:
        st.subheader(f"Results for '{store_name}':")

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
