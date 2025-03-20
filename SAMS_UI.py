import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os

# ------------------------------
# Admin Login Setup
# ------------------------------
ADMIN_USERNAME = "Karthi"  # Change to your preferred username
ADMIN_PASSWORD = "SAMS"  # Change to a secure password

# Streamlit login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login UI
if not st.session_state.logged_in:
    st.title(" Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success(" Login successful! Redirecting...")
            st.rerun()
        else:
            st.error(" Invalid credentials. Try again.")

    st.stop()  # Stop execution if not logged in

# ------------------------------
# Load Google Service Account Credentials
# ------------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
json_path = r"C:\Users\Karthayani\OneDrive\Documents\Arduino\SAMS\sams-credentials.json"

if not os.path.exists(json_path):
    st.error(f" Credentials file not found at: {json_path}")
    st.stop()

try:
    creds = Credentials.from_service_account_file(json_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    st.success(" Credentials loaded successfully!")
except Exception as e:
    st.error(f" Failed to load credentials: {e}")
    st.stop()

# ------------------------------
# Connect to Google Sheet
# ------------------------------
SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    st.success(f" Connected to Google Sheet: {sheet.title}")
except Exception as e:
    st.error(f" Permission error: {e}")
    st.write(" Make sure the service account email is added as an **Editor** in the Google Sheet.")
    st.stop()

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("SAMS Access Log")

# Load and display data
try:
    data = sheet.get_all_values()
    if data:
        st.table(data)
    else:
        st.warning(" No data found in the Google Sheet.")
except Exception as e:
    st.error(f"Failed to fetch data from the sheet: {e}")

# ------------------------------
# Streamlit App Link
# ------------------------------
st.markdown("### Open Streamlit App")
st.markdown("[Click here to open the SAMS App](http://localhost:8501)", unsafe_allow_html=True)
