#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

// WiFi Credentials
const char* ssid     = "Karthi";  
const char* password = "karthi11";  

// Google Apps Script Deployment ID
const char* GScriptId = "AKfycbxOrciNsS-dNmRdVegdXvzrEZrCi8LsgUj3ilNJJrsj9XtXsD_xjrxK-suybSy2-3lI";
String serverURL = "https://script.google.com/macros/s/" + String(GScriptId) + "/exec";

// RFID Module Pins
#define SS_PIN  D4
#define RST_PIN D3

MFRC522 mfrc522(SS_PIN, RST_PIN);
WiFiClientSecure client;
HTTPClient http;

// NTP Client for Time Sync
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 19800, 60000);

void setup() {
    Serial.begin(115200);
    Serial.println("\nInitializing...");

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");

    // Check Internet Access
    Serial.print("Pinging Google... ");
    if (client.connect("www.google.com", 80)) {
        Serial.println("Success!");
    } else {
        Serial.println("Failed! No Internet Access.");
    }

    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("RFID Scanner Ready...");

    timeClient.begin();
    client.setInsecure();  // Ignore SSL certificate validation
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        delay(1000);
        return;
    }

    // Read RFID Tag
    String tagID = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        tagID += String(mfrc522.uid.uidByte[i], HEX);
    }
    tagID.toUpperCase();
    Serial.print("Card UID: ");
    Serial.println(tagID);

    // Check if Tag is in the Allowed List
    String accessState = "Denied";
    String allowedTags[] = {"F33F38DA", "8D053202", "B3850332", "B33E1532", "03440732"};
    for (String allowed : allowedTags) {
        if (tagID == allowed) {
            accessState = "Accepted";
            break;
        }
    }

    // Get Current Time
    timeClient.update();
    String currentTime = timeClient.getFormattedTime();

    // Create Full Request URL
    String fullRequest = serverURL + "?tag=" + tagID + "&time=" + currentTime + "&access=" + accessState;
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

    delay(3000);
}
