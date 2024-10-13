#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor = AFMS.getMotor(4);

void setup() {
  AFMS.begin();
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
}

void loop() {
  myMotor->setSpeed(150);
  myMotor->run(FORWARD);
}
