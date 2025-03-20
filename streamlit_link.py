import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# 🔹 Define Admin Credentials
ADMIN_USERNAME = "Karthi"
ADMIN_PASSWORD = "SAMS"  # Change this to your actual password

# 🔹 Login Page
st.title(" Admin Login")

username = st.text_input("Username", "")
password = st.text_input("Password", type="password")
login_btn = st.button("Login")

# 🔹 Authenticate Admin
if login_btn:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.success(" Logged in successfully!")

        # 🔹 Google Sheets API Setup
        sheet_id = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClID"  # REPLACE with your actual Sheet ID
        
        # Load credentials from secrets
        creds_dict = json.loads(st.secrets["google_credentials"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        
        # Connect to Google Sheets
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1  # Access first sheet

        # Fetch Data
        data = sheet.get_all_records()

        # Display Data
        st.subheader(" Google Sheets Data")
        st.write(data)

    else:
        st.error(" Incorrect username or password!")

