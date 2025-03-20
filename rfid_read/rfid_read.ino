#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN  D4
#define RST_PIN D3

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
    Serial.begin(115200);
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("RFID Scanner Ready...");
}

void loop() {
    if (!mfrc522.PICC_IsNewCardPresent()) {
        Serial.println("No card detected...");
        delay(1000);
        return;
    }
    if (!mfrc522.PICC_ReadCardSerial()) {
        Serial.println("Failed to read card...");
        delay(1000);
        return;
    }
    Serial.print("Card UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println();
    delay(2000);
}
