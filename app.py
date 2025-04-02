import streamlit as st
import pandas as pd

# Load the CSV data (with a relative path)
data = pd.read_csv('merged_df.csv')  # This assumes merged_df.csv is in the same folder as your app.py file

# Title of the app
st.title("Store Information Search")

# Search input
store_name = st.text_input("Enter Store Name:", "")

# Displaying related information
if store_name:
    # Filter data based on the search input
    filtered_data = data[data['store_name'].str.contains(store_name, case=False, na=False)]

    if not filtered_data.empty:
        st.subheader(f"Results for '{store_name}':")

        # Display grouped data
        grouped_data = filtered_data.groupby('category')

        for category, group in grouped_data:
            st.write(f"**Category: {category}**")
            st.dataframe(group)  # Show the filtered data for each category
    else:
        st.write("No matching stores found.")
