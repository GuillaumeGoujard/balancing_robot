#include "Motor.h"
#include "Balanced.h"


Timer2 Timer2;
extern Mpu6050 Mpu6050;
extern Motor Motor;
#define DELAY 3000
char mode = '0';

void setup() 
{
  Motor.Pin_init();
  Motor.Encoder_init();
  Mpu6050.init();
  Serial.begin(115200);
  delay(100);

  // Serial.println("Waiting for Python signal...");
  // while (Serial.available() == 0) {
  //   // Wait until a signal is received from Python
  // }
  
  // mode = Serial.read();
  // Serial.print("Received signal: ");
  // Serial.println(mode);

  // if (mode == '1') {
  //   Serial.println("Starting PWM ramp test...");
  //   Timer2.init(100);
  // } 
  // else if (mode == '2') {
  //   Serial.println("Starting step response test...");
  //   Timer2.init(20);
  // }
}


void loop() 
{
  Motor.Forward(255);
  if (mode == '1') {
    startRampTest();
    mode = '0';  // Reset mode after execution (Arduino can wait for new command)
  } 
  else if (mode == '2') {
    startStepTest();
    mode = '0';  
  }
}

void startRampTest() 
{
    delay(1500);
    for (int pwm_value = 0; pwm_value <= 255; pwm_value += 10) {
      Serial.println(mode);
      Motor.Forward(pwm_value);
      delay(3000);
    }
    Motor.Forward(254);
    delay(3000);
    Motor.Forward(255);
    delay(3000);
    Motor.Forward(0);
}


void startStepTest() 
{
    // Motor.Forward(100);
    delay(1500);
    for (int i = 0; i < 3; i++) {
      Motor.Forward(255);
      delay(1000);
      Motor.Forward(0);
      delay(500);
    }
}

// void setup() 
// {
//   Motor.Pin_init();
//   Motor.Encoder_init();
//   Timer2.init(100);
//   Mpu6050.init();
//   Serial.begin(9600);
//   delay(100);

//   Serial.println("Waiting for Python signal...");
//   while (Serial.available() == 0) {
//     // Wait until a signal is received from Python
//   }
  
//   char received = Serial.read();
//   if (received == '1') {
//     Serial.println("Starting PWM ramp test...");
//   }
// }

// void loop() 
// {
//   for (int pwm_value = 0; pwm_value <= 255; pwm_value += 10) {
//     Motor.Forward(pwm_value);  // Set motor PWM
//     delay(DELAY);  // 1s delay per step
//   }

//   Motor.Forward(254);
//   delay(DELAY);
//   Motor.Forward(255);
//   delay(DELAY);
//   Motor.Forward(0);
//   while (1);  // Stop execution after full sweep
// }
