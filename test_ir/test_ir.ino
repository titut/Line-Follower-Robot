#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

//sensor analog input pins
int far_left_sensor = A0;
int middle_left_sensor = A1;
int middle_right_sensor = A2;
int far_right_sensor = A3;

/*Bird-eye view with the front of the car on top, sensor reading from left to right
0: far left
1: middle left
2: middle right
3: far right
*/
int sensor_reading[4] = {1023, 1023, 1023, 1023};

/*current wheel speed from 0 to 255
0: left wheel
1: right wheel
*/
int wheel_speed[2] = {0, 0};

//Wheel speed parameters (all variables in cm and sec)
int normal_speed=0;
float wheel_diameter = 6;
float wheel_speed_to_cm = 25.0/(6.0*255.0)*3.14*wheel_diameter;
int base_distance = 13/wheel_speed_to_cm;

//PID
float current_error;
float previous_error;
float integral_error;
float timestep = 0.01;
float P = 0.3;
float I = 0;
float D = 0;

//Initiate Motor Shield OBject
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

//Initiate and connect motor objects
Adafruit_DCMotor *left_motor = AFMS.getMotor(1);
Adafruit_DCMotor *right_motor = AFMS.getMotor(4);

String delimiter = ",";

void setup() {
  current_error = 0;
  previous_error = 0;
  integral_error = 0;
  Serial.begin(9600);
  // put your setup code here, to run once:
  AFMS.begin();
}

void loop() {
  if(Serial.available()){
    normal_speed = Serial.readString().toInt();
  }

  // put your main code here, to run repeatedly:
  int error = getSensorReading();
  current_error = error;

  getWheelSpeedHeading(error);
  //printReading();

  left_motor->setSpeed(wheel_speed[0]);
  left_motor->run(BACKWARD);
  right_motor->setSpeed(wheel_speed[1]);
  right_motor->run(FORWARD);

  String print_to_serial = wheel_speed[0] + delimiter + wheel_speed[1] + delimiter + sensor_reading[0] + delimiter + sensor_reading[1] + delimiter + sensor_reading[2] + delimiter + sensor_reading[3];
  Serial.println(print_to_serial);
  
  delay(timestep * 1000);
}

int printReading(){
  Serial.print("Sensor 0: ");
  Serial.println(sensor_reading[0]);
  Serial.print("Sensor 1: ");
  Serial.println(sensor_reading[1]);
  Serial.print("Sensor 2: ");
  Serial.println(sensor_reading[2]);
  Serial.print("Sensor 3: ");
  Serial.println(sensor_reading[3]);
}

int getSensorReading(){
  sensor_reading[0] = analogRead(far_left_sensor);
  sensor_reading[1] = analogRead(middle_left_sensor);
  sensor_reading[2] = analogRead(middle_right_sensor);
  sensor_reading[3] = analogRead(far_right_sensor);
  int threshold = 400;
  bool far_left_reading = sensor_reading[0] > threshold;
  bool middle_left_reading = sensor_reading[1] > threshold;
  bool middle_right_reading = sensor_reading[2] > threshold;
  bool far_right_reading = sensor_reading[3] > threshold;
  if(middle_left_reading && middle_right_reading && !far_left_reading && !far_right_reading){
    return 0;
  } else if(middle_left_reading && !middle_right_reading && !far_left_reading && !far_right_reading){
    return 50;
  } else if(middle_left_reading && far_left_reading && !middle_right_reading && !far_right_reading){
    return 100;
  } else if(far_left_reading && !middle_left_reading && !middle_right_reading && !far_right_reading){
    return 200;
  } else if(middle_right_reading && !middle_left_reading && !far_left_reading && !far_right_reading){
    return -50;
  } else if(middle_right_reading && far_right_reading && !middle_left_reading && !far_left_reading){
    return -100;
  } else if(far_right_reading && !middle_right_reading && !middle_left_reading && !far_left_reading){
    return -200;
  }
  return current_error;
}

int PID(float new_error){
  current_error = new_error;
  integral_error = integral_error + new_error * timestep;
  float derivative_error = (new_error - previous_error)/timestep;
  previous_error = current_error;
  return (P * current_error) + (I * integral_error) + (D * derivative_error);
}

int getWheelSpeedHeading(float heading){
  if(normal_speed == 0){
    wheel_speed[0] = 0;
    wheel_speed[1] = 0;
    return 0;
  }
  float omega = heading/180.0;
  int Vr = ((2.0 * normal_speed) + (omega * base_distance))/2.0;
  int Vl = (2.0 * normal_speed) - Vr;
  if(Vl > normal_speed || Vr > normal_speed){
    if(Vl > Vr){
      Vl = Vl/Vl * normal_speed;
      Vr = Vr/Vl * normal_speed;
    } else {
      Vl = Vl/Vr * normal_speed;
      Vr = Vr/Vr * normal_speed;
    }
  }
  if(Vl < 0){
    Vl = 0;
  }
  if(Vr < 0){
    Vr = 0;
  }
  wheel_speed[0] = Vl;
  wheel_speed[1] = Vr;
  return 0;
}