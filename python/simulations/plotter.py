import pandas as pd
import matplotlib.pyplot as plt

def plot_results(csv_file):
    data = pd.read_csv(csv_file)
    t_values = data["time"]
    x_c_values = data["x_c"]
    x_c_dot_values = data["x_c_dot"]
    theta_values = data["theta"]
    theta_dot_values = data["theta_dot"]
    F_c_values = data["V"]

    plt.figure(figsize=(10, 8))

    # Cart position and velocity
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(t_values, x_c_values, label="Cart Position $x_c$")
    ax2 = ax1.twinx()
    ax2.plot(t_values, x_c_dot_values, 'r', label="Cart Velocity $\\dot{x}_c$")
    ax1.set_ylabel("Position (m)")
    ax2.set_ylabel("Velocity (m/s)")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Pendulum angle and angular velocity
    ax3 = plt.subplot(3, 1, 2)
    ax3.plot(t_values, theta_values, label="Pendulum Angle $\\theta$")
    ax4 = ax3.twinx()
    ax4.plot(t_values, theta_dot_values, 'r', label="Angular Velocity $\\dot{\\theta}$")
    ax3.set_ylabel("Angle (rad)")
    ax4.set_ylabel("Angular Velocity (rad/s)")
    ax3.legend(loc="upper left")
    ax4.legend(loc="upper right")

    # Control force
    ax5 = plt.subplot(3, 1, 3)
    ax5.plot(t_values, F_c_values, label="Control voltage $V$")
    ax5.set_xlabel("Time (s)")
    ax5.set_ylabel("Voltage (V)")
    ax5.legend()

    plt.tight_layout()
    plt.show()

    # Phase diagram
    plt.figure(figsize=(6, 6))
    plt.plot(theta_values, theta_dot_values, label="Phase Trajectory")
    plt.xlabel("Pendulum Angle $\\theta$ (rad)")
    plt.ylabel("Angular Velocity $\\dot{\\theta}$ (rad/s)")
    plt.title("Phase Diagram")
    plt.legend()
    plt.grid()
    plt.show()
