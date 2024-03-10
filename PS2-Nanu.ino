#include <dht.h>
#define dht_pin 6
#define led_pin 7

dht DHT;
byte incomingByte;

void setup() {
  pinMode(led_pin, OUTPUT);
}

void loop() {
  Serial.begin(9600);
  Serial.println("1. Temperature And Humidity Sensor");
  Serial.println("2. LED Functions");
  Serial.println("Which function would you like to access? ");

  while (Serial.available() == 0) {}

  int menuChoice = Serial.parseInt();

  switch (menuChoice) {
    case 1:
    int chk = DHT.read11(dht_pin);
    Serial.print("Humidity = ");
    Serial.print(DHT.humidity);
    Serial.print("%  ");
    Serial.print("Temperature = ");
    Serial.print(DHT.temperature);
    Serial.println("C  ");
    Serial.print("\n");
    break;
    case 2:
    Serial.println("Press A for turning LED ON");
    Serial.println("Press S for turning LED OFF");
    Serial.end();
    Serial.begin(9600);
    while (Serial.available() == 0) {}
    incomingByte = Serial.read();
    if (incomingByte == 'A') {
     Serial.println("A Pressed");
     digitalWrite(led_pin, HIGH);
    }else if (incomingByte == 'S') {
     Serial.println("S Pressed");
     digitalWrite(led_pin, LOW);
    }else
      Serial.println("Invalid Choice");
    Serial.print("\n");
    break;
  default:
      Serial.println("Please choose a valid selection");
      Serial.print("\n");
      break;
  }
  Serial.end();
}