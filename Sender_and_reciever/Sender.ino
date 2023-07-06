#include <SPI.h>
#include <LoRa.h>

int counter = 0;

// const int csPin = 10; //15, 7, 10
// const int resetPin = 9; //14, 6, 9
// const int irqPin = 1;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // LoRa.setPins(csPin, resetPin, irqPin);
  Serial.println("LoRa Sender");


  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  LoRa.setTxPower(20);
}

void loop() {
  //Serial.print("Sending packet: ");
  //Serial.println(counter);

  //(!LoRa.available()) Serial.println("HUITA");
  // send packet
  LoRa.beginPacket();
  LoRa.print("hello ");
  LoRa.print(counter);
  LoRa.endPacket();

  // // Читаем ответ
  // String s = "";
  // while (LoRa.available()) {
  //   s += (char)LoRa.read();
  // }
  // Serial.println(s+" "+LoRa.packetRssi());

  counter++;

  //delay(500);
}
