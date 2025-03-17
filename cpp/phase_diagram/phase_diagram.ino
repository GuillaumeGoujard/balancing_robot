#include "Motor.h"
#include "Balanced.h"


Timer2 Timer2;
extern Mpu6050 Mpu6050;
extern Motor Motor;
extern Balanced Balanced;



void setup() 
{
  Motor.Pin_init();
  Motor.Encoder_init();
  Timer2.init(TIMER);
  Mpu6050.init();
  Serial.begin(19200);
  delay(100);
}

void loop() 
{
  Motor.Forward(0);
  delay(10000);
}
