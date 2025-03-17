#include "Balanced.h"
#include "Wire.h"
#include "Motor.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "KalmanFilter.h"
MPU6050 MPU6050;
Mpu6050 Mpu6050;
KalmanFilter kalmanfilter;
Motor Motor;
void Timer2::init(int time)
{
  MsTimer2::set(time,interrupt);
  MsTimer2::start();
}

static void Timer2::interrupt()
{ 
  sei();//enable the global interrupt
  Mpu6050.DataProcessing();
  Motor.Log_RotationalSpeed();
}

void Motor::Log_RotationalSpeed()
{
    static unsigned long lastTime = 0;
    unsigned long currentTime = millis();
    float deltaTime = (currentTime - lastTime) / 1000.0;  // Convert to seconds
    lastTime = currentTime;

    float rpm_left = (Motor::encoder_count_left_a * 60.0) / (PPR * deltaTime);

    Serial.print(rotational_speed);
    Serial.print(", ");
    Serial.println(rpm_left);

    Motor::encoder_count_left_a = 0;

}


void Mpu6050::init()
{
   Wire.begin();         
   MPU6050.initialize();    
 }

Mpu6050::Mpu6050()
{
    dt = 0.005, Q_angle = 0.001, Q_gyro = 0.005, R_angle = 0.5, C_0 = 1, K1 = 0.05;
}

void Mpu6050::DataProcessing()
{  
  MPU6050.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);// Data acquisition of MPU6050 gyroscope and accelerometer
  kalmanfilter.Angletest(ax, ay, az, gx, gy, gz, dt, Q_angle, Q_gyro, R_angle, C_0, K1);// Obtaining Angle by Kalman Filter
}
