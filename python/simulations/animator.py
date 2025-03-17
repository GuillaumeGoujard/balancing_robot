import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_pendulum(csv_file, max_time=None, frame_skip=20):
    data = pd.read_csv(csv_file)

    if max_time is not None:
        data = data[data["time"]<=max_time]

    data = data.iloc[::frame_skip, :]

    t_values = data["time"].values
    x_c_values = data["x_c"].values
    theta_values = data["theta"].values

    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.1, 0.2)
    ax.set_aspect("equal")
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.grid()

    cart_width, cart_height = 0.2, 0.1
    pendulum_length = 0.1
    
    cart, = ax.plot([], [], "ks", markersize=10)  # Cart
    pendulum, = ax.plot([], [], "-o", lw=2, markersize=6)
    
    # Time progress bar setup
    bar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.02])  # Position at bottom
    bar_ax.set_xlim(0, t_values[-1])
    bar_ax.set_ylim(0, 1)
    bar_ax.set_xlabel("Time (s)")
    bar_ax.axis("off")
    time_bar, = bar_ax.barh(0.5, 0, height=0.8, color='blue')
    
    # Time label
    time_text = bar_ax.text(t_values[-1] / 2, 0.5, "Time: 0.00 s", ha="center", va="bottom", color="black", fontsize=10)
    
    def init():
        cart.set_data([], [])
        pendulum.set_data([], [])
        time_bar.set_width(0)
        time_text.set_text("Time: 0.00 s")
        return cart, pendulum, time_bar, time_text

    def update(frame):
        x_c = x_c_values[frame]
        theta = theta_values[frame]
        
        # Cart position
        cart.set_data([x_c], [0])
        
        # Pendulum position
        pendulum_x = [x_c, x_c + pendulum_length * np.sin(theta)]
        pendulum_y = [0, pendulum_length * np.cos(theta)]
        pendulum.set_data(pendulum_x, pendulum_y)

        # Update time progress bar
        time_bar.set_width(t_values[frame])
        time_text.set_text(f"Time: {t_values[frame]:.2f} s")
        
        return cart, pendulum, time_bar, time_text

    ani = animation.FuncAnimation(fig, update, frames=len(t_values), init_func=init, blit=True, interval=30)
    plt.show()
