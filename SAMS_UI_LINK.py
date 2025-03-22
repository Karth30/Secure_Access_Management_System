import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Define Admin Credentials
ADMIN_USERNAME = "SAMS"
ADMIN_PASSWORD = "SAMS"  # Change this!

# 🔹 Initialize Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Default: Not logged in

# 🔹 Login Page
st.title("Admin Login")

if not st.session_state.logged_in:  # Show login form only if not logged in
    username = st.text_input("Username", "")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True  # Store login state
            st.success("Logged in successfully!")
            st.rerun()  # Refresh to show content
        else:
            st.error("Incorrect username or password!")
else:
    # 🔹 Show Google Sheets Data (Only After Login)
    try:
        st.write("🔹 Loading Google Credentials...")
        creds_dict = dict(st.secrets["google_credentials"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        client = gspread.authorize(creds)

        # Fetch Data
        SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"  # Replace with your Sheet ID
        sheet = client.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_values()

        if data:
            df = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame

            # 🔹 Column Selection for Filtering
            selected_column = st.selectbox("Select Column to Filter", df.columns)
            unique_values = df[selected_column].unique()
            filter_value = st.selectbox(f"Filter by {selected_column}", unique_values)

            # 🔹 Apply Filter
            filtered_data = df[df[selected_column] == filter_value]
            st.write("### Filtered Data")
            st.table(filtered_data)

        else:
            st.warning("No data found in the sheet.")

    except Exception as e:
        st.error(f"Error Fetching Google Sheets: {e}")

    # 🔹 Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False  # Reset login state
        st.rerun()  # Refresh to show login page
