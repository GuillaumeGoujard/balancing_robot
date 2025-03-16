from model import InvertedPendulum
from simulator import Simulator
from plotter import plot_results
from animator import animate_pendulum
import os

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
        error = -theta  # Stabilize around theta = 0
        self.integral_error += error * self.dt
        derivative_error = (error - self.previous_error) / self.dt
        self.previous_error = error

        V = self.Kp * error + self.Ki * self.integral_error + self.Kd * derivative_error
        V = max(min(V, self.max_voltage), -self.max_voltage)
        return V

# Initialize model and simulator
pendulum = InvertedPendulum()
controller = PIDController(Kp=55, Kd=0.75)
simulator = Simulator(pendulum, controller, dt = 0.005)

# Define initial conditions: x_c, x_c_dot, theta, theta_dot
initial_conditions = [0, 0, 0.2, 0]

# Ensure results directory exists
os.makedirs("results", exist_ok=True)
output_file = "results/simulation_output.csv"

# Run simulation
csv_file = simulator.run(initial_conditions, output_file)

animate_pendulum(csv_file, max_time=2)
# Plot results
plot_results(csv_file)
