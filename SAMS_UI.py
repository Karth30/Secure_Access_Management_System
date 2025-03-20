import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

#  Ensure Google credentials exist
if "google_credentials" not in st.secrets:
    st.error(" Google Credentials Not Found! Add them in Streamlit Secrets.")
    st.stop()

#  Load credentials
try:
    creds_dict = dict(st.secrets["google_credentials"])
    
    #  Use correct scope for Google Sheets API
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    st.success(" Google Credentials Loaded Successfully!")
except Exception as e:
    st.error(f" Failed to load credentials: {e}")
    st.stop()
