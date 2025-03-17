import numpy as np

RAD_to_DEG = 360/(2*np.pi)

# Define Controller (dummy PID for now)
class PIDController:
    def __init__(self, Kp=0.0, Ki=0.0, Kd=0.0, dt=0.005, max_voltage=3.5):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral_error = 0.0
        self.previous_error = 0.0
        self.max_voltage = max_voltage

    def compute(self, theta, theta_dot, dt):
        angle = theta*RAD_to_DEG
        speed = theta_dot*RAD_to_DEG

        error = -angle  # Stabilize around theta = 0
        self.integral_error += error * self.dt
        # derivative_error = theta_dot #(error - self.previous_error) / self.dt
        self.previous_error = error
        continuous_pwm = -self.Kp * angle + self.Ki * self.integral_error - self.Kd * speed
        pwm = max(min(255, continuous_pwm), -255)/255
        V = pwm*self.max_voltage
        V = max(min(V, self.max_voltage), -self.max_voltage)
        return V
