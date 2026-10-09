#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <ArduinoJson.h>

#define VIBRATOR_PIN 18
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHAR_UUID    "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class HapticCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        std::string value = pCharacteristic->getValue();
        if (value.length() > 0) {
            StaticJsonDocument<200> doc;
            deserializeJson(doc, value);
            
            int pulses = doc["vibration_pulses"];
            int duration = doc["pulse_duration_ms"];
            int intensity = doc["intensity"];
            
            for(int i=0; i<pulses; i++) {
                analogWrite(VIBRATOR_PIN, intensity);
                delay(duration);
                analogWrite(VIBRATOR_PIN, 0);
                delay(duration);
            }
        }
    }
};

void setup() {
    pinMode(VIBRATOR_PIN, OUTPUT);
    BLEDevice::init("OmniHear-DogCollar");
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);
    BLECharacteristic *pChar = pService->createCharacteristic(
        CHAR_UUID, BLECharacteristic::PROPERTY_WRITE
    );
    pChar->setCallbacks(new HapticCallbacks());
    pService->start();
    BLEDevice::getAdvertising()->addServiceUUID(SERVICE_UUID);
    BLEDevice::startAdvertising();
}
void loop() { delay(1000); }
