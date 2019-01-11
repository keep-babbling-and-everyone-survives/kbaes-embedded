#include <stdio.h>
#include <stddef.h>

void setup() {
  pinMode(13,OUTPUT);
  Serial.begin(9600);
}
void loop() {
  //if(Serial.available() > 0) {
    String data = Serial.readString();
    if(data == "on") {
      //Serial.print("blyet");
      digitalWrite(13,HIGH);
    }
    if(data == "off") {
      //Serial.print("doom");
      digitalWrite(13,LOW);
    }
    Serial.print(data);
    //delay(1000);
  //}
}
