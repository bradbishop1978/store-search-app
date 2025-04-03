# Existing imports and other parts of the code remain the same

# Helper function to handle store status
def format_store_status(status):
    if pd.isna(status) or status == "":
        return "LSM Active"
    return status  # Return the status as-is if it’s not blank

# Display information if a specific store has been chosen
if st.session_state.selected_store:
    selected_store = st.session_state.selected_store
    filtered_data = data[data['store_name'].str.lower() == selected_store.lower()]

    if not filtered_data.empty:
        # Create columns for aligned display with proper titles
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.write("### Store Info")
            st.write("**Company Name:**", format_value(filtered_data['company_name'].iloc[0]))
            st.write("**Store ID:**", f"[{format_value(filtered_data['store_id'].iloc[0])}](https://www.lulastoremanager.com/stores/{filtered_data['store_id'].iloc[0]})")
            st.write("**Company ID:**", format_value(filtered_data['company_id'].iloc[0]))
            st.write("**Full Address:**", format_value(filtered_data['full_address'].iloc[0]))

        with col2:
            st.write("### Login Details")
            st.write("**Email:**", format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-')) 
            last_login_at = filtered_data['last_login_at'].iloc[0] if 'last_login_at' in filtered_data.columns else '-'
            st.write("**Last Login At:**", days_since_last_login(last_login_at))
            st.write("**Role Name:**", format_value(filtered_data['role_name'].iloc[0] if 'role_name' in filtered_data.columns else '-'))
            st.write("**Phone Number:**", format_value(filtered_data['phone_number'].iloc[0] if 'phone_number' in filtered_data.columns else '-'))

        with col3:
            st.write("### DSP ID")
            st.write("**UberEats ID:**", format_value(filtered_data['ubereats_id'].iloc[0] if 'ubereats_id' in filtered_data.columns else '-'))
            st.write("**DoorDash ID:**", format_value(filtered_data['doordash_id'].iloc[0] if 'doordash_id' in filtered_data.columns else '-'))
            st.write("**GrubHub ID:**", format_value(filtered_data['grubhub_id'].iloc[0] if 'grubhub_id' in filtered_data.columns else '-'))

        with col4:
            st.write("### Additional Details")
            st.write("**Store Email:**", format_value(filtered_data['store_email'].iloc[0] if 'store_email' in filtered_data.columns else '-'))
            st.write("**Store Phone:**", format_value(filtered_data['store_phone'].iloc[0] if 'store_phone' in filtered_data.columns else '-'))
            st.write("**Created Date:**", format_date(filtered_data['created_date'].iloc[0] if 'created_date' in filtered_data.columns else '-'))  # Format the created date
            st.write("**Store Status:**", format_store_status(filtered_data['store_status'].iloc[0] if 'store_status' in filtered_data.columns else '-'))  # Check for status

    else:
        st.write("No matching store found.")
