#include <SPI.h>
#include <LoRa.h>

const int csPin = 5; //15, 7, 13
const int resetPin = 14; //14, 6, 9
const int irqPin = 2;

//#define ss 5
//#define rst 14
//#define dio0 2

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("LoRa Receiver");
  LoRa.setPins(csPin, resetPin, irqPin);
  LoRa.setSPIFrequency (20000000);
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    //delay(1);
    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // received a packet
    //Serial.print("Received packet '");

    // read packet
    String s = "";
    while (LoRa.available()) {
      s += (char)LoRa.read();
    }
    Serial.println(s+" "+LoRa.packetRssi());
    //s += " "+LoRa.packetRssi();
    
    // // Отправляем ответ
    // LoRa.beginPacket();
    // LoRa.print(s);
    // LoRa.endPacket();

    // print RSSI of packet
    //Serial.print("' with RSSI ");
    //Serial.println(LoRa.packetRssi());
  }
}
