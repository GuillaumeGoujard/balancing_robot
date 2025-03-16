import pandas as pd
import matplotlib.pyplot as plt
import scienceplots  # This ensures the package is available

PWM_to_V = 3.43/255

# Load the data
path_to_csv = "/Users/guillaumegoujard/Desktop/balancing_robot/serial_logger/motor_step_test.csv"
ramp_test = pd.read_csv(path_to_csv)

# Set IEEE-style plot
plt.style.use(['science', 'grid'])  # Using an IEEE-like style

# Create figure and axis
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot Motor Speed (RPM) on primary y-axis
ax1.plot(ramp_test["Time (ms)"], ramp_test["Motor Speed (RPM)"], label="Motor Speed (RPM)", linestyle="--", linewidth=2, color='b')
ax1.set_xlabel("Time (ms)", fontsize=12)
ax1.set_ylabel("Motor Speed (RPM)", fontsize=12, color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle="--", linewidth=0.5)

# Create secondary y-axis for PWM
ax2 = ax1.twinx()
ax2.plot(ramp_test["Time (ms)"], ramp_test["PWM"]*PWM_to_V, label="Voltage (converted from PWM)", linestyle="-", linewidth=2, color='r')
ax2.set_ylabel("Voltage (V)", fontsize=12, color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.grid(False)

# Legend
fig.legend(loc="upper right", fontsize=10)

# Title
ax1.set_title("Motor Step Response", fontsize=14)
plt.savefig("motor_step_response.png")
# Show plot
plt.show()



# Load the data
path_to_csv = "/Users/guillaumegoujard/Desktop/balancing_robot/serial_logger/motor_ramp_test.csv"
ramp_test = pd.read_csv(path_to_csv)

# Set IEEE-style plot
plt.style.use(['science', 'grid'])  # Using an IEEE-like style

# Create figure and axis
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot Motor Speed (RPM) on primary y-axis
ax1.plot(ramp_test["Time (ms)"], ramp_test["Motor Speed (RPM)"], label="Motor Speed (RPM)", linestyle="--", linewidth=2, color='b')
ax1.set_xlabel("Time (ms)", fontsize=12)
ax1.set_ylabel("Motor Speed (RPM)", fontsize=12, color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle="--", linewidth=0.5)

# Create secondary y-axis for PWM
ax2 = ax1.twinx()
ax2.plot(ramp_test["Time (ms)"], ramp_test["PWM"]*PWM_to_V, label="Voltage (converted from PWM)", linestyle="-", linewidth=2, color='r')
ax2.set_ylabel("Voltage (V)", fontsize=12, color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.grid(False)

# Legend
fig.legend(loc="upper right", fontsize=10)

# Title
ax1.set_title("Motor Ramp Response", fontsize=14)
plt.savefig("motor_ramp_response.png")

# Show plot
plt.show()