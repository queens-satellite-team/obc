#include <Wire.h>
#define SLAVE_ADDRESS 0x8

const int ledPin = 13; //onboard LED
static_assert(LOW == 0, "Expecting LOW to be 0");

int data_send_to_PI = 1;

char data[12] = {}; // receive data array

void setup()
{
  Wire.begin(SLAVE_ADDRESS);                // join i2c bus with address #8, defined in Pi pytho code as slave_address
  Wire.onReceive(receiveEvent); // register event? receive
  Wire.onRequest(sendEvent); // send
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); //turn LED off
  Serial.begin(9600);           // start serial for output
}


void loop()
{
  delay(10);
  delay(10);
  delay(10);
  delay(10);
  delay(10);
  data_send_to_PI = 1;
}


// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  int i = 0;
  while(Wire.available()) // loop through all but the last
  {
    data[i] = Wire.read();
    i++; 
  }
  data[i] = '\0';
    //for (int i = 0; i < 25; i++){
      //data[i] = Wire.read(); // receive byte as a character and stored in data[]
    //}
    if (data[0] == 1){
      data_send_to_PI = 0;
      }
    Serial.print(data); // print the string
  
}


void sendEvent()
{
  Wire.write(data_send_to_PI);
  //while(Wire.available())
  //{
    //Wire.write(data_send_to_PI);
  //}
}