import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

#  Define Admin Credentials
ADMIN_USERNAME = "Karthi"
ADMIN_PASSWORD = "SAMS"  # Change this!

#  Login Page
st.title(" Admin Login")

# Input fields
username = st.text_input("Username", "")
password = st.text_input("Password", type="password")
login_btn = st.button("Login")

#  Authentication
if login_btn:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.success(" Logged in successfully!")

        # Debugging: Show that login is working
        st.write(" Login Successful! Now Fetching Google Sheets Data...")

        # Load Google Sheets API Credentials
        try:
            creds_dict = json.loads(st.secrets["google_credentials"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
            client = gspread.authorize(creds)
            st.success(" Google Credentials Loaded Successfully!")

            #  Fetch Data from Google Sheets
            SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"  #  Replace with your actual Google Sheet ID
            sheet = client.open_by_key(SHEET_ID).sheet1
            data = sheet.get_all_values()  # Get all rows

            if data:
                st.write(" **Google Sheets Data:**")
                st.table(data)  # Show data in table
            else:
                st.warning(" No data found in the sheet.")

        except Exception as e:
            st.error(f" Error Fetching Google Sheets: {e}")

    else:
        st.error(" Incorrect username or password!")
