import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


try:
    creds_dict = dict(st.secrets["google_credentials"])  # Convert TOML to dictionary
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)
    st.success(" Credentials loaded successfully!")
except Exception as e:
    st.error(f" Failed to load credentials: {e}")
    st.stop()

SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"


try:
    sheet = client.open_by_key(SHEET_ID).sheet1
    st.success(f" Connected to Google Sheet: {sheet.title}")
except Exception as e:
    st.error(f"Permission error: {e}")
    st.write("**Ensure the service account email is added as an Editor in the Google Sheet.**")
    st.stop()


st.title(" SAMS Access Log")


try:
    data = sheet.get_all_values()
    if data:
        st.write(" **Latest Access Logs:**")
        st.table(data)
    else:
        st.warning("⚠ No data found in the Google Sheet.")
except Exception as e:
    st.error(f" Failed to fetch data from the sheet: {e}")
