#ifndef _BALANCED_h
#define _BALANCED_h

#include "MsTimer2.h"
#include "KalmanFilter.h"

enum Direction
{
  FORWARD,
  BACK,
  LEFT,
  RIGHT,
  STOP,
};

class Timer2
{
  public:
          void init(int time);
          static void interrupt();
  private:       
          #define TIMER 500
};


class Mpu6050
{
  public:
          void init();
          void DataProcessing();
          Mpu6050();

  public:
         int ax, ay, az, gx, gy, gz;
         float dt, Q_angle, Q_gyro, R_angle, C_0, K1;
};












#endif
