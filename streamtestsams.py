import os
import gspread
from google.oauth2.service_account import Credentials

# Load credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
json_path = r"C:\Users\Karthayani\OneDrive\Documents\Arduino\SAMS\sams-credentials.json"

try:
    print("Checking if JSON file exists:", os.path.exists(json_path))  

    creds = Credentials.from_service_account_file(json_path, scopes=SCOPES)
    client = gspread.authorize(creds)

    SHEET_ID = "1c-8nJVLV49nDyXtuPLbOQs9c4SdWSR9HTYzGyJsFClI"

    print("Accessing Google Sheet...")
    sheet = client.open_by_key(SHEET_ID).sheet1  # Change to .worksheet("Sheet1") if needed
    print("Successfully accessed the sheet!")

    data = sheet.get_all_values()
    print("First 5 rows of data:", data[:5])

except FileNotFoundError:
    print("ERROR: The credentials file was not found. Check the file path.")
except gspread.exceptions.APIError as api_err:
    print("ERROR: Google Sheets API error:", api_err)
except Exception as e:
    import traceback
    print("ERROR: Unexpected error:")
    print(traceback.format_exc())  # 🔹 PRINT FULL ERROR DETAILS
