#include "BluetoothSerial.h"

const char turnOFF = '0';

BluetoothSerial esp_BT;

const int irSensorPin = 33;
const int motorPin = 26;
const int buzzerPin = 14;
const int ledPin = 2;


unsigned long totalBuzzerHighTime = 0;    ///// for wheel deactivation (time)

bool motorStopped = false;

void setup() {
  pinMode(irSensorPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
 pinMode(ledPin, OUTPUT);
  pinMode(motorPin, OUTPUT);
  Serial.begin(115200);

  esp_BT.begin("ESP32test");  ///////////////////name for bluetooth connectivity
  Serial.println("The device started, now you can pair it with Bluetooth!");

}

void loop() {


 
  if (esp_BT.available()) {
    
    char incoming = esp_BT.read();

    if (incoming == turnOFF) {
       Serial.println("                         ORDER FROM COMPANY TO STOP CAR");
      esp_BT.print("0");
      // Stop the motor
      totalBuzzerHighTime=0;
     digitalWrite(motorPin, LOW);
     digitalWrite(ledPin, LOW);
      digitalWrite(buzzerPin, LOW);

      motorStopped = true;
    } else {
      // If any other character is received, allow the motor to start
      motorStopped = false;
    }
  }

 //If the motor is not stopped, continuously check the IR sensor
 if (!motorStopped) {
  // Serial.println("                         ORDER ENDS, Receiving IR VALUES");
   int eyeStatus = digitalRead(irSensorPin);

    if (eyeStatus == HIGH) {      ///................
      update_text_run();
      Serial.println("                                    Eyes open");        
      LOW_the_buzzer();
      deactivateAlarm();
      totalBuzzerHighTime=0;




    } else {

       Serial.println("                                    Eyes closed");

       Serial.println("                             totalBuzzerHighTime  "+totalBuzzerHighTime);
        Serial.println("                             .......................................................");
      
      

      digitalWrite(buzzerPin, HIGH);

      totalBuzzerHighTime+=1000;

      delay(1000);




      if(totalBuzzerHighTime >2000){
      activateAlarm();
      update_text_stop();
      }
      
    }
 }
}

void update_text_run() {
  esp_BT.print("1");
}

void update_text_stop() {
  esp_BT.print("0");
}

void activateAlarm() {
 // Serial.println("Alarm activated!");
  digitalWrite(motorPin, LOW);
 
  digitalWrite(ledPin, LOW);
}

void deactivateAlarm() {
//  Serial.println("Alarm deactivated");

  digitalWrite(motorPin, HIGH);

  digitalWrite(ledPin, HIGH);
}


void LOW_the_buzzer() {
  digitalWrite(buzzerPin, LOW);
}