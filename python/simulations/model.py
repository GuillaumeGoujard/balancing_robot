import numpy as np

class InvertedPendulum:
    def __init__(self, share_of_weight=0.6):
        # System Parameters
        total_mass = 0.81
        self.M = total_mass*share_of_weight  # Cart mass (kg)
        self.Mp = total_mass*(1-share_of_weight)  # Pendulum mass (kg)
        self.l = 0.1  # Pendulum length (m)
        self.I = 3e-3  # Pendulum moment of inertia (kg·m²)
        self.r = 0.033  # Wheel radius (m)
        self.N = 30  # Gear ratio
        self.Kv = 0.1 #3.2  # Voltage gain (N/V)
        self.b = 5.7e-2 #1.9e-3  # Damping (Ns/m)
        self.g = 9.81  # Gravity (m/s²)

    def equations_of_motion(self, t, state, V):
        x_c, x_c_dot, theta, theta_dot = state
        
        # Compute control input from controller
        # V = controller.compute(theta, theta_dot, t)
        F_c = self.Kv * V - self.b * x_c_dot

        # Compute accelerations
        denominator = (self.M + self.Mp) * (self.I + self.Mp * self.l**2) - (self.Mp * self.l * np.cos(theta))**2
        x_c_ddot = ((self.I + self.Mp * self.l**2) * F_c + self.Mp * self.l * (self.Mp * self.g * self.l * np.sin(theta) - self.Mp * self.l * x_c_dot * theta_dot * np.sin(theta))) / denominator
        theta_ddot = (self.Mp * self.l * np.cos(theta) * F_c + (self.M + self.Mp) * (self.Mp * self.g * self.l * np.sin(theta) - self.Mp * self.l * x_c_dot * theta_dot * np.sin(theta))) / denominator

        return [x_c_dot, x_c_ddot, theta_dot, theta_ddot]