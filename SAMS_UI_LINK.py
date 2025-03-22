import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ** Define Admin Credentials**
ADMIN_USERNAME = "SAMS"
ADMIN_PASSWORD = "SAMS"  # Change this to a secure password

# ** Authentication Function**
def authenticate(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# ** Session State for Login**
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ** Login Form**
if not st.session_state.authenticated:
    st.title(" Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error(" Invalid Credentials!")

# ** If Logged In, Show Dashboard**
if st.session_state.authenticated:
    st.title(" Access Management System")

    # ** Load Google Credentials**
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["google_credentials"], scopes=SCOPES)
    client = gspread.authorize(creds)

    # ** Open Users Sheet**
    SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"
    users_sheet = client.open_by_key(SHEET_ID).worksheet("Sheet1")

    # ** Load Users Data**
    users_data = users_sheet.get_all_values()
    users_dict = {row[0]: row[1:] for row in users_data[1:]}  # Convert to Dictionary

    # ** Display User Table**
    st.write("### Current Users")
    st.table(users_data)

    # ** Modify Access**
    st.write("### Modify Access")
    selected_user = st.selectbox("Select User", list(users_dict.keys()))
    new_status = st.radio("Change Access State", ["Accepted", "Denied"])

    if st.button("Update Access"):
        for i, row in enumerate(users_data):
            if row[0] == selected_user:
                users_sheet.update_cell(i+1, 3, new_status)  # Update Access State
                st.success(f" Updated {selected_user} to {new_status}")
                st.experimental_rerun()  # Refresh UI

    # ** Logout Button**
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
