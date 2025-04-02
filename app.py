import streamlit as st
import pandas as pd

# Load the CSV data (ensure 'merged_df.csv' is in the same directory as this script)
data = pd.read_csv('merged_df.csv')

# Print the column names for debugging (you can remove this line once everything works)
st.write("Columns available in the dataset:", data.columns.tolist())

# Title of the app
st.title("Store Information Search")

# Search input
store_name = st.text_input("Enter Store Name:", "")

# Displaying related information
if store_name:
    # Filter data based on the search input in the store_name column
    filtered_data = data[data['store_name'].str.contains(store_name, case=False, na=False)]

    if not filtered_data.empty:
        st.subheader(f"Results for '{store_name}':")

        # Selecting the relevant columns: store_id and company_name
        results = filtered_data[['store_id', 'company_name', 'last_login_at', 'role_name']]  # Using the correct column names
        st.dataframe(results)  # Show the filtered data for columns A and B
    else:
        st.write("No matching stores found.")
