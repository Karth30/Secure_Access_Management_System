import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Define Admin Credentials
ADMIN_USERNAME = "Karthi"
ADMIN_PASSWORD = "karthi11"  # Change this!

# 🔹 Login Page
st.title(" Admin Login")

# Input fields
username = st.text_input("Username", "")
password = st.text_input("Password", type="password")
login_btn = st.button("Login")

#  Authentication
if login_btn:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.success(" Logged in successfully!")

        # Debug: Check login is working
        st.write(" Login Successful! Now Fetching Google Sheets Data...")

        #  Load Google Sheets API Credentials
        try:
            st.write(" Loading Google Credentials...")  # Debug
            creds_dict = dict(st.secrets["google_credentials"])  #  FIXED THIS LINE
            creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
            client = gspread.authorize(creds)
            st.success(" Google Credentials Loaded Successfully!")

            # 🔹 Fetch Data from Google Sheets
            SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"  #  REPLACE WITH YOUR SHEET ID
            st.write("🔹 Connecting to Google Sheets...")  # Debug
            sheet = client.open_by_key(SHEET_ID).sheet1
            st.write(" Google Sheets Connection Established!")  # Debug

            # Get all rows
            data = sheet.get_all_values()  
            if data:
                st.write(" **Google Sheets Data:**")
                st.table(data)  # Show data in table
            else:
                st.warning(" No data found in the sheet.")

        except Exception as e:
            st.error(f" Error Fetching Google Sheets: {e}")

    else:
        st.error(" Incorrect username or password!")
