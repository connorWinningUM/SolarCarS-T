/*
* This file is the main program for the electronic control unit for the Missouri S&T Solar Car.
* This program is meant to be run on an Arduino Due board and bootloaded using the Arduino IDE.
*
*////////////////////////////////////////

#include <cstdint>
#include <cstring>
#include <Arduino.h>
#include "due_can.h"

using namespace std;

void pinInit();
void updateDrive();

void setup() {
  //setup the CAN bus interface
  Can0.begin(CAN_BPS_500k, 255);
  Can1.begin(CAN_BPS_500k, 255);
}

void loop() {


}

void pinInit() {

}