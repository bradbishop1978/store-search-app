import streamlit as st
import pandas as pd

# Load the CSV data (make sure merged_df.csv is in the same directory as your app.py)
data = pd.read_csv('merged_df.csv')

# Title of the app
st.title("Store Information Search")

# Search input
store_name = st.text_input("Enter Store Name:", "")

# Displaying related information
if store_name:
    # Filter data based on the search input (look in the 'store_name' column)
    filtered_data = data[data['store_name'].str.contains(store_name, case=False, na=False)]

    if not filtered_data.empty:
        st.subheader(f"Results for '{store_name}':")

        # Displaying the values in columns A and B (assuming they are the first two columns)
        results = filtered_data[['ColumnA', 'ColumnB']]  # Replace 'ColumnA' and 'ColumnB' with the actual names of those columns
        st.dataframe(results)  # Show the filtered data for columns A and B
    else:
        st.write("No matching stores found.")
