import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.spatial import ConvexHull
from model import InvertedPendulum
from simulator import Simulator
from plotter import plot_results
from controller import PIDController

# Define the range of initial conditions
theta_range = np.linspace(0, np.pi / 3, 30)  # Sweep over theta from 0 to 60°
theta_dot_range = np.linspace(0, 2, 30)  # Sweep over theta_dot from 0 to 2 rad/s

# Initialize model and controller
pendulum = InvertedPendulum()
controller = PIDController(Kp=55*2, Kd=0.75, Ki=0, max_voltage=7)

# Create simulator instance
simulator = Simulator(pendulum, controller, dt_dynamics=0.001, dt_control=0.005, t_max=10)

run_empirical_validation = False
if run_empirical_validation:
    # Step 1: Sweep over theta with theta_dot = 0
    theta_range = np.linspace(0, np.pi / 3, 100)  # From 0 to 60°
    max_theta = 0

    for theta_0 in theta_range:
        print(theta_0)
        initial_conditions = [0, 0, theta_0, 0]  # theta_dot = 0
        output_file = "results/temp_simulation.csv"

        # Run simulation
        csv_file = simulator.run(initial_conditions, output_file)

        # Load results and check convergence
        data = pd.read_csv(csv_file)
        final_theta = data["theta"].iloc[-1]
        final_theta_dot = data["theta_dot"].iloc[-1]

        # Convergence criteria
        if np.abs(final_theta) < 1e-2 and np.abs(final_theta_dot) < 1e-2:
            max_theta = theta_0
        else:
            break  # Stop searching when failure occurs

    # Step 2: Sweep over theta_dot with theta = 0
    theta_dot_range = np.linspace(0, 2, 100)  # From 0 to 2 rad/s
    max_theta_dot = 0

    for theta_dot_0 in theta_dot_range:
        print('theta_dot', theta_dot_0)

        initial_conditions = [0, 0, 0, theta_dot_0]  # theta = 0
        output_file = "results/temp_simulation.csv"

        # Run simulation
        csv_file = simulator.run(initial_conditions, output_file)

        # Load results and check convergence
        data = pd.read_csv(csv_file)
        final_theta = data["theta"].iloc[-1]
        final_theta_dot = data["theta_dot"].iloc[-1]

        # Convergence criteria
        if np.abs(final_theta) < 1e-2 and np.abs(final_theta_dot) < 1e-2:
            max_theta_dot = theta_dot_0
        else:
            break  # Stop searching when failure occurs

    # Generate ellipse points
    theta_vals = np.linspace(0, 2 * np.pi, 100)
    ellipse_x = max_theta * np.cos(theta_vals)
    ellipse_y = max_theta_dot * np.sin(theta_vals)

    # Plot the estimated region of attraction
    plt.figure(figsize=(6, 6))
    plt.plot(ellipse_x, ellipse_y, 'r-', label="Estimated Region of Attraction")
    plt.xlabel("Theta (rad)")
    plt.ylabel("Theta dot (rad/s)")
    plt.title("Empirical Estimation of the Region of Attraction")
    plt.legend()
    plt.grid()
    plt.show()

run_sims = True
if run_sims:
    max_theta = 0.075
    max_theta_dot = 0.5

    # Generate ellipse points for estimated attraction region
    theta_vals = np.linspace(0, 2 * np.pi, 100)
    ellipse_x = max_theta * np.cos(theta_vals)
    ellipse_y = max_theta_dot * np.sin(theta_vals)

    # Define epsilon and create two test cases
    epsilon = 0.01
    inside_initial_conditions = [0, 0, max_theta - epsilon, 0]
    outside_initial_conditions = [0, 0, max_theta + epsilon, 0]

    # Simulate both test cases
    inside_csv = simulator.run(inside_initial_conditions, "results/inside_simulation.csv")

    simulator = Simulator(pendulum, controller, dt_dynamics=0.001, dt_control=0.005, t_max=0.7)
    outside_csv = simulator.run(outside_initial_conditions, "results/outside_simulation.csv")

    # Load phase trajectories
    inside_data = pd.read_csv(inside_csv)
    outside_data = pd.read_csv(outside_csv)

    import scienceplots  # This ensures the package is available

    plt.style.use(['science'])  # Use IEEE style for plots

    # Create figure
    plt.figure(figsize=(6, 6))

    # Plot the estimated region of attraction
    plt.fill(ellipse_x, ellipse_y, color="lightgreen", alpha=0.3, label="Estimated Attraction Region")
    plt.plot(ellipse_x, ellipse_y, 'g-', lw=2)

    # Plot phase trajectories
    plt.plot(inside_data["theta"], inside_data["theta_dot"], 'b-', label="Trajectory (Inside)")
    plt.plot(outside_data["theta"], outside_data["theta_dot"], 'r-', label="Trajectory (Outside)")

    # Labels and legend
    plt.xlabel("$\\theta$ (rad)")
    plt.ylabel("$\\dot{\\theta}$ (rad/s)")
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)

    # Show plot
    plt.show()