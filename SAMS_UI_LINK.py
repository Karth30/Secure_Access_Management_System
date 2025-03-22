import streamlit as st
import requests
import pandas as pd

# ---- GOOGLE APPS SCRIPT URL ----
GAS_URL = "https://script.google.com/macros/s/AKfycbxagzKZR3ypBOIrRzNojwPpgrhN4x1SbyyMISkkli6VaN2yR_eH3bmjBMNpFPCp-YnP/exec"

# ---- ADMIN LOGIN ----
ADMIN_USERNAME = "SAMS"
ADMIN_PASSWORD = "SAMS"  # Change this to a secure password!

st.set_page_config(page_title="RFID Access Control", layout="wide")

# ---- SESSION STATE ----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---- LOGIN PAGE ----
def login():
    st.title("Admin Login")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", key="password", type="password")  # ✅ FIXED HERE

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Incorrect credentials!")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---- MAIN DASHBOARD ----
st.title("RFID Access Control System")

# ---- Fetch Data from Google Sheet ----
@st.cache_data(ttl=30)
def fetch_data():
    response = requests.get(GAS_URL)

    if response.status_code != 200:
        st.error("Failed to fetch data from Google Sheets!")
        return pd.DataFrame()  # Return empty DataFrame on error

    try:
        json_data = response.json()

        if not json_data or not isinstance(json_data, list):
            st.warning("No data found in Google Sheets!")
            return pd.DataFrame()

        return pd.DataFrame(json_data)

    except ValueError:
        st.error("Error parsing JSON response!")
        return pd.DataFrame()

df = fetch_data()

# ---- FILTERING OPTIONS ----
st.sidebar.header("Filter Logs")

if not df.empty:
    # Convert Timestamp column to datetime for filtering
    df.columns = ["Timestamp", "RFID Tag ID", "Time Scanned", "Access State"]

    # Dropdown Filters
    unique_tags = df["RFID Tag ID"].unique()
    unique_states = df["Access State"].unique()

    selected_filter = st.sidebar.radio("Filter By:", ["All", "RFID Tag", "Timestamp", "Access State"])

    if selected_filter == "RFID Tag":
        selected_tag = st.sidebar.selectbox("Select RFID Tag", unique_tags)
        df = df[df["RFID Tag ID"] == selected_tag]

    elif selected_filter == "Timestamp":
        start_date = st.sidebar.date_input("Start Date", df["Timestamp"].min())
        end_date = st.sidebar.date_input("End Date", df["Timestamp"].max())
        df = df[(df["Timestamp"] >= pd.to_datetime(start_date)) & (df["Timestamp"] <= pd.to_datetime(end_date))]

    elif selected_filter == "Access State":
        selected_state = st.sidebar.selectbox("Select Access State", unique_states)
        df = df[df["Access State"] == selected_state]

    st.dataframe(df, use_container_width=True)

else:
    st.warning("No data available.")

# ---- Update Access State ----
st.subheader("Update Access State")

tag_id = st.text_input("Enter RFID Tag ID to Update")
new_state = st.selectbox("Select New Access State", ["Accepted", "Denied"])

if st.button("Update Access State"):
    if tag_id:
        update_data = {"tag": tag_id, "access_state": new_state}
        response = requests.post(GAS_URL, json=update_data)

        if response.status_code == 200:
            st.success(f"Access state for {tag_id} updated to {new_state} successfully!")
            st.rerun()  # Auto-refresh app
        else:
            st.error("Failed to update access state!")
    else:
        st.warning("Please enter an RFID Tag ID.")

# ---- Logout ----
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
