#include <Adafruit_MotorShield.h>

//sensor analog input pins
int far_left_sensor = A1;
int middle_left_sensor = A1;
int middle_right_sensor = A1;
int far_right_sensor = A1;

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
int wheel_speed[2] = {50, 50};

//Wheel speed parameters (all variables in cm and sec)
int normal_speed=50;
float wheel_diameter = 3;
float wheel_speed_to_cm = 25.0/(6.0*255.0)*3.14*wheel_diameter;
int base_distance = 10/wheel_speed_to_cm;

//PID
float current_error;
float previous_error;
float integral_error;
float timestep = 0.5;
float P = 0.3;
float I = 0;
float D = 0;

//Initiate Motor Shield OBject
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

//Initiate and connect motor objects
Adafruit_DCMotor *left_motor = AFMS.getMotor(1);
Adafruit_DCMotor *right_motor = AFMS.getMotor(4);

void setup() {
  current_error = 0;
  previous_error = 0;
  integral_error = 0;
  // put your setup code here, to run once:
  AFMS.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  int error = getSensorReading();

  //PID

  //getWheelSpeedHeading(0);

  left_motor->setSpeed(wheel_speed[0]);
  left_motor->run(FORWARD);
  right_motor->setSpeed(wheel_speed[1]);
  right_motor->run(FORWARD);

  Serial.println(sensor_reading[0]);
  
  delay(timestep * 1000);
}

int getSensorReading(){
  sensor_reading[0] = analogRead(far_left_sensor);
  sensor_reading[1] = analogRead(middle_left_sensor);
  sensor_reading[2] = analogRead(middle_right_sensor);
  sensor_reading[3] = analogRead(far_right_sensor);
  return 0;
}

int PID(float new_error){
  current_error = new_error;
  integral_error = integral_error + new_error * timestep;
  float derivative_error = (new_error - previous_error)/timestep;
  previous_error = current_error;
  return (P * current_error) + (I * integral_error) + (D * derivative_error);
}

int getWheelSpeedHeading(float heading){
  float omega = heading/180.0;
  int Vr = ((2.0 * normal_speed) + (omega * base_distance))/2.0;
  int Vl = (2.0 * normal_speed) - Vr;
  wheel_speed[0] = Vl;
  wheel_speed[1] = Vr;
  return 0;
}