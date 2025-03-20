import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from Streamlit secrets
try:
    creds_dict = st.secrets["google_credentials"]
    creds = Credentials.from_service_account_info(creds_dict)
    client = gspread.authorize(creds)
    st.success(" Credentials loaded successfully!")
except Exception as e:
    st.error(f" Failed to load credentials: {e}")
    st.stop()
