#include <Wire.h>
#define SLAVE_ADDRESS 0x8

// Created by Jeremy Dube
// I2C slave code 
// SDA pin A4
// SCL pin A5
// To be edited further

char dataSent[25];
int dataSent_index = 0;
char dataReceived[5];
int dataReceived_index = 0;

void setup() {
  // put your setup code here, to run once:
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
}


void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

void receiveData(int byteCount) {
  
int i = 0;
  while (1 < Wire.available()) {
    dataReceived[i] = Wire.read(); // Read data and store into array
    i++;
  }
  Serial.print(dataReceived);
}

// callback for sending data
void sendData() {
  Wire.write(dataSent[dataSent_index]); // Write data from array
  dataSent_index++;
  if(dataSent_index >= 5){
    dataSent_index = 0;
  }
}
