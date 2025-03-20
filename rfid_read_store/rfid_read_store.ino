#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

// WiFi Credentials
const char* ssid     = "Karthi";//"SSN";
const char* password = "karthi11";//"Ssn1!Som2@Sase3";

// Google Apps Script Deployment ID
const char* GScriptId = "AKfycbzfl-1keIg0JjjdvP-k10NXMkXolkwGAss-PXBkV1XQk9EjerktHkjGJTU4NvpSXjTK";
String serverURL = "https://script.google.com/macros/s/" + String(GScriptId) + "/exec";

// RFID Module Pins
#define SS_PIN  D4
#define RST_PIN D3

MFRC522 mfrc522(SS_PIN, RST_PIN);

// WiFi & HTTP Clients
WiFiClientSecure client;  
HTTPClient http;

// NTP Client for Time Sync
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800, 60000); // GMT +5:30 (India Time)

void setup() {
    Serial.begin(115200);
    Serial.println("\nInitializing...");

    // Start WiFi Connection
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
        attempts++;
        if (attempts > 20) { // Fail after 20 seconds
            Serial.println("\nFailed to connect to WiFi!");
            return;
        }
    }
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Test Connection to Google
    Serial.print("Pinging Google... ");
    if (client.connect("script.google.com", 443)) {
        Serial.println("Success!");
    } else {
        Serial.println("Failed!");
    }

    // Start SPI & RFID Module
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("RFID Scanner Ready...");

    // Start NTP Client
    timeClient.begin();
}

void loop() {
    // Ensure WiFi is connected before sending data
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi lost. Reconnecting...");
        WiFi.disconnect();
        delay(1000);
        WiFi.begin(ssid, password);
        while (WiFi.status() != WL_CONNECTED) {
            delay(1000);
            Serial.print(".");
        }
        Serial.println("\nWiFi Reconnected!");
    }

    // Update the NTP Time
    timeClient.update();
    String currentTime = timeClient.getFormattedTime();

    // Check for new RFID Card
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        Serial.println("No RFID card detected...");
        delay(1000);
        return;
    }

    // Read RFID UID
    String tagID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        tagID += String(mfrc522.uid.uidByte[i], HEX);
    }
    tagID.toUpperCase();
    Serial.print("Card UID: ");
    Serial.println(tagID);

    // Print Full HTTP URL
    String fullRequest = serverURL + "?tag=" + tagID + "&time=" + currentTime;
    Serial.print("Requesting URL: ");
    Serial.println(fullRequest);

    // Send Data to Google Sheets
    if (WiFi.status() == WL_CONNECTED) {
        http.begin(client, fullRequest);
        int httpResponseCode = http.GET();

        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);

        if (httpResponseCode > 0) {
            Serial.println("Data Sent Successfully!");
        } else {
            Serial.println("HTTP Request Failed! Error: " + String(httpResponseCode));
        }
        http.end();
    } else {
        Serial.println("WiFi Disconnected. Reconnecting...");
        WiFi.begin(ssid, password);
    }

    delay(2000);
}
