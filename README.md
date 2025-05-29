# Secure_Access_Management_System

INTRODUCTION:

This project introduces a refined approach to automating access control by integrating Radio Frequency Identification (RFID) technology with Internet of Things (IoT) capabilities. In institutions and organizations, ensuring secure and efficient entry management is crucial for maintaining safety and operational integrity. Traditional access systems—such as manual logs or physical ID checks—are often inefficient, time-consuming, and prone to errors or manipulation. In response to these limitations, this work presents an IoT-enabled RFID-based access control system that ensures accurate, real-time, and tamper-proof monitoring of entry attempts. Despite the availability of modern technologies, many facilities still rely on outdated manual verification methods. Security personnel often verify identities visually or record entries on paper, which may lead to delays, inconsistencies, and limited traceability. This system aims to address such challenges by leveraging RFID technology combined with cloud-based storage and web interfaces. The proposed solution utilizes RFID for identity verification, the ESP8266 NodeMCU for connectivity, and Google Sheets for real-time data logging via Google Apps Script (GAS) and Google API integration.To enhance administrative control and usability, a web-based dashboard is developed using the Streamlit framework. This dashboard provides visual access logs and user-specific activity records through an intuitive, interactive interface.

Note:

RFID(Radio-Frequency Identification) is an automatic identification system that uses electromagnetic fields to transfer data between a RFID reader and an RFID tag. It is a contactless communication that enables storage and retrieval of information from a source.


SYSTEM ARCHITECTURE:

![image](https://github.com/user-attachments/assets/3af1689e-6d41-42f3-a16b-5bc3fb111957)

The Secure Access Management System functions through a coordinated interaction of hardware and cloud components. At the core is the RFID Reader (MFRC522), which detects RFID tags presented by users and reads their unique identifier (UID) via SPI communication. This UID is then transmitted to the ESP8266 NodeMCU, which serves as the primary microcontroller. The ESP8266 processes the UID by cross-referencing it with a predefined list of authorized credentials stored in a local dictionary or optionally in a Firebase database for scalable management. Based on this verification, the system activates LED indicators to provide immediate user feedback—green LED lights up for authorized access and red for unauthorized access. Simultaneously, the scan event, along with metadata such as UID, timestamp (retrieved using NTP), and access status, is logged to a Google Sheet via an HTTPS request. This logged data is visualized in real-time using a Streamlit web dashboard, which serves as the administrative panel. The dashboard allows authenticated admins to view and filter access records efficiently. Additionally, the system includes an alert mechanism that monitors access attempts; when more than five unauthorized entries are detected in succession, a notification is triggered (via E-mail alerts using Google app script), instantly alerting the administrator to possible intrusion attempts.


HARDWARE SETUP:

![image](https://github.com/user-attachments/assets/f62cd21e-cfc8-4f18-bec0-92661df596a3)

![image](https://github.com/user-attachments/assets/f47ab677-5d96-4367-9f1d-6a2d995948a2)

● The MFRC522 RFID reader reads the UID of RFID tags upon proximity detection.
● The ESP8266 fetches this UID via SPI and compares it to a hardcoded array of authorized tags.
● Depending on validation, the system blinks either a green or red LED.
● The access attempt (UID, timestamp, result) is sent to the cloud using HTTP

REAL- TIME LOGGING VIA GOOGLE SCRIPTS:

● The ESP8266 sends a GET request to a published Web App URL.
● Google Apps Script captures the parameters and appends a new row in the Sheet. (javascript)
function doGet(e) {
 var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
 sheet.appendRow([e.parameter.tag, e.parameter.time, e.parameter.access]);
 return ContentService.createTextO}

 ![image](https://github.com/user-attachments/assets/2567f8b0-2abe-4d74-9bfc-9ca720b4de80)

 STREAMLIT-BASED ADMIN DASHBOARD:
 
Developed using Python’s Streamlit and GSpread, the dashboard allows for:
● Secure admin login
● Visual tabular display of logs
● Filtering by Tag UID, Time, or Access Status
Filtering Example:
python
selected_column = st.selectbox("Select Column", df.columns)
filter_value = st.selectbox("Select Value", df[selected_column].unique())
st.table(df[df[selected_column] == filter_value])

RESULTS:

![image](https://github.com/user-attachments/assets/a2abf155-ef3e-4d75-903a-f0563c21a400)

 Image of ACCESS GRANTED condition

![image](https://github.com/user-attachments/assets/aefea983-6610-4278-af8c-3cb4346964b0)

 Image of ACCESS denied condition

 The Google Sheet remained synchronized in real-time, with timestamps accurate to the
second.

![image](https://github.com/user-attachments/assets/79d6be10-e9e2-40a4-b67f-13ae25f2189c)

Google Sheet with Sample Entries

The Streamlit dashboard performed reliably across devices, providing fast and
filterable access insights.

![image](https://github.com/user-attachments/assets/7b0551a5-aec7-4a83-bd4a-ef0241adde8b)

 Dashboard UI and Filtered Table

 CONCLUSION:
 
The project was aimed to get effective and efficient time-saving automated computerized access in real-time with a excel sheet to maintain access records. The implemented system proved to be easy to use and implement, cost efficient, time-saving, less tedious, and portable










