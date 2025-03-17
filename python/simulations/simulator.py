import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

class Simulator:
    def __init__(self, model, controller, dt_dynamics=0.001, dt_control=0.005, t_max=10, theta_limit=np.pi/4):
        self.model = model
        self.controller = controller
        self.dt_dynamics = dt_dynamics  # High-resolution dynamics step
        self.dt_control = dt_control  # Lower-frequency control step
        self.t_max = t_max
        self.theta_limit = theta_limit

    def run(self, initial_conditions, output_file):
        t_values = [0]
        states = [initial_conditions]
        voltages = [0]  # Store voltage values

        t = 0
        V = 0  # Initialize control voltage

        while t < self.t_max:
            # Update control every dt_control
            if len(t_values) % int(self.dt_control / self.dt_dynamics) == 0:
                V = self.controller.compute(states[-1][2], states[-1][3], self.dt_control)  # Compute control

            # Solve dynamics at higher resolution
            sol = solve_ivp(self.model.equations_of_motion, [t, t + self.dt_dynamics], states[-1], 
                            args=(V,), method='RK45', t_eval=[t + self.dt_dynamics])
            new_state = sol.y[:, -1]

            if abs(new_state[2]) > self.theta_limit:
                break

            t += self.dt_dynamics
            t_values.append(t)
            states.append(new_state)
            voltages.append(V)

        # Save results to CSV
        results = pd.DataFrame(states, columns=["x_c", "x_c_dot", "theta", "theta_dot"])
        results.insert(0, "time", t_values)
        results["F_c"] = self.model.Kv * np.zeros_like(t_values) - self.model.b * results["x_c_dot"]
        results["V"] = voltages  # Log voltage
        results.to_csv(output_file, index=False)
        return output_file
