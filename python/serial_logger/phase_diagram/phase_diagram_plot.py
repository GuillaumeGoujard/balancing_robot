import pandas as pd
import matplotlib.pyplot as plt
import scienceplots  # This ensures the package is available

def plot_phase_diagram(csv_path, theta_col="theta", thetadot_col="thetadot", save_path=None):
    """
    Reads a CSV file and plots the phase diagram (thetadot vs theta) in IEEE style.
    
    Parameters:
    - csv_path: str, path to the CSV file.
    - theta_col: str, column name for theta (default: "theta").
    - thetadot_col: str, column name for thetadot (default: "thetadot").
    - save_path: str or None, if provided, saves the plot to this path.
    """
    # Load data
    data = pd.read_csv(csv_path)
    
    # Extract theta and thetadot
    theta = data[theta_col]
    thetadot = data[thetadot_col]

    # Set IEEE-style plot
    plt.style.use(['science', 'grid'])

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(theta, thetadot, linestyle='-', linewidth=1.5, color='b')

    # Labels and formatting
    ax.set_xlabel(r"$\theta$ (rad)", fontsize=12)
    ax.set_ylabel(r"$\dot{\theta}$ (rad/s)", fontsize=12)
    ax.set_title("Phase Diagram: $\dot{\Theta}$ vs $\Theta$", fontsize=14)
    ax.grid(True, linestyle="--", linewidth=0.5)

    # Save plot if path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show plot
    plt.show()

# Example usage
plot_phase_diagram("phase_test.csv", theta_col="Angle (deg.)", thetadot_col="Speed (deg./s)")