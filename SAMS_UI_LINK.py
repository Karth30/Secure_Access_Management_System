import streamlit as st
import requests
import pandas as pd

# ---- GOOGLE APPS SCRIPT URL ----
GAS_URL = "https://script.google.com/macros/s/AKfycbwycsq2zReJKQ3GZPxMRGDqK3NIXIl6ePNpmos0Etlpf716vWZo4jq2czSQPwtu8fQ/exec"

# ---- ADMIN LOGIN ----
ADMIN_USERNAME = "SAMS"
ADMIN_PASSWORD = "SAMS"  # Change this to a secure password!

st.set_page_config(page_title="RFID Access System", page_icon="")

# ---- SESSION STATE ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---- LOGIN PAGE ----
def login():
    st.title("Admin Login")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("❌ Incorrect credentials!")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---- MAIN DASHBOARD ----
st.title(" RFID Access Control")

# ---- Fetch Data from Google Sheet ----
@st.cache_data(ttl=30)
def fetch_data():
    response = requests.get(GAS_URL)
    
    if response.status_code != 200:
        st.error(" Failed to fetch data from Google Sheets!")
        return pd.DataFrame()  # Return empty DataFrame on error

    try:
        json_data = response.json()

        if not json_data or not isinstance(json_data, list):  # Check if data is empty or incorrect format
            st.warning("No data found in Google Sheets!")
            return pd.DataFrame()

        return pd.DataFrame(json_data)
    
    except ValueError:  # Handles JSON decoding errors
        st.error(" Error parsing JSON response!")
        return pd.DataFrame()

df = fetch_data()

# ---- Display Data ----
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.warning(" No data available.")

# ---- Update Access State ----
st.subheader(" Update Access State")

tag_id = st.text_input(" Enter RFID Tag ID to Update")
new_state = st.selectbox(" Select New Access State", ["Accepted", "Denied"])

if st.button("Update Access State"):
    if tag_id:
        update_data = {"tag": tag_id, "access_state": new_state}
        response = requests.post(GAS_URL, json=update_data)

        if response.status_code == 200:
            st.success("Access state updated successfully!")
            st.rerun()  # Rerun the app after update
        else:
            st.error(" Failed to update access state!")
    else:
        st.warning(" Please enter an RFID Tag ID.")

# ---- Logout ----
if st.button(" Logout"):
    st.session_state.logged_in = False
    st.rerun()
