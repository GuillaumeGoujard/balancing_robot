from model import InvertedPendulum
from simulator import Simulator
from plotter import plot_results
from animator import animate_pendulum
import os
import numpy as np
from controller import PIDController

# Initialize model and simulator
pendulum = InvertedPendulum(share_of_weight=0.7)
controller = PIDController(Kp=55*2, Kd=0.75, Ki=0, max_voltage=7)
simulator = Simulator(pendulum, controller, dt_dynamics = 0.001, dt_control = 0.005, t_max=10)

# Define initial conditions: x_c, x_c_dot, theta, theta_dot
theta_d = 20*2*np.pi/360
theta_d = 0.5*2*np.pi/360

initial_conditions = [0, 0, theta_d, 0]

# Ensure results directory exists
os.makedirs("results", exist_ok=True)
output_file = "results/simulation_output.csv"

# Run simulation
csv_file = simulator.run(initial_conditions, output_file)

animate_pendulum(csv_file, max_time=10)
# Plot results
plot_results(csv_file)
