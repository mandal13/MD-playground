from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

def animate(n_steps, potential_energies, kinetic_energies, total_energies, potential_energy, positions, dt, save_file=None):
    """
    Animate the dynamics of a particle in a potential energy landscape.
    
    Parameters:
        n_steps (int): Number of simulation steps.
        potential_energies (list): Potential energy values at each step.
        kinetic_energies (list): Kinetic energy values at each step.
        total_energies (list): Total energy values at each step.
        potential_energy (callable): Function defining the potential energy surface.
        positions (list): Positions of the particle at each step.
        dt (float): Time step size.
        save_file (str, optional): File path to save the animation. If None, display the animation.
    """
    # Prepare for animation
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: Particle on the potential energy surface
    ax1 = axes[0]
    x_grid = np.linspace(min(positions) - 1, max(positions) + 1, 500)
    ax1.plot(x_grid, potential_energy(x_grid), label="Potential Energy Surface", color="blue")
    particle, = ax1.plot([], [], 'ro', label="Particle Position")
    
    ax1.set_xlim(min(positions) - 1, max(positions) + 1)
    ax1.set_ylim(min(potential_energies) - 0.5, max(potential_energies) + 0.5)

    ax1.set_xlabel("Position")
    ax1.set_ylabel("Potential Energy")
    ax1.legend()
    ax1.grid(True)
    
    # Right: Energies vs. time
    ax2 = axes[1]
    time = np.arange(n_steps) * dt
    pe_line, = ax2.plot([], [], label="Potential Energy", color="blue")
    ke_line, = ax2.plot([], [], label="Kinetic Energy", color="green")
    te_line, = ax2.plot([], [], label="Total Energy", color="red")
    ax2.set_xlim(0, n_steps * dt)
    ax2.set_ylim(min(min(potential_energies), min(kinetic_energies), min(total_energies)) - 0.5,
                 max(max(potential_energies), max(kinetic_energies), max(total_energies)) + 0.5)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Energy")
    ax2.legend()
    ax2.grid(True)


    # Update function for animation
    def update(frame):
        # Update particle position on the potential energy surface
        particle.set_data(positions[frame], potential_energies[frame])
        
        # Update energy plots
        pe_line.set_data(time[:frame+1], potential_energies[:frame+1])
        ke_line.set_data(time[:frame+1], kinetic_energies[:frame+1])
        te_line.set_data(time[:frame+1], total_energies[:frame+1])
        return particle, pe_line, ke_line, te_line
    
    # Initialize animation
    def init():
        particle.set_data([], [])
        pe_line.set_data([], [])
        ke_line.set_data([], [])
        te_line.set_data([], [])
        return particle, pe_line, ke_line, te_line

    ani = FuncAnimation(fig, update, frames=n_steps, init_func=init, blit=True, interval=30)
    

    # Save animation or show
    if save_file:
        ani.save(save_file, writer="ffmpeg", fps=30)
    else:
        plt.tight_layout()
        plt.show()
    


def compute_energies(system, istep, log_file=None):
    """
    Compute the kinetic, potential, and total energy of the system and optionally log the results.

    Parameters:
        system (System): The system object containing mass, positions, velocities, and potential.
        istep (int): The current simulation step.
        log_file (file object or None): A file object for logging energy and system data.
                                        If None, no logging is performed.

    Returns:
        tuple: A tuple containing:
            - kinetic_energy (float): The kinetic energy of the system at the current step.
            - potential_energy (float): The potential energy of the system at the current step.
            - total_energy (float): The total energy of the system at the current step.
    """
    # Calculate the kinetic energy: KE = 0.5 * m * v^2
    kinetic_energy = 0.5 * system.mass * system.velocities[0]**2

    # Calculate the potential energy using the system's potential
    potential_energy = system.potential.potential(system.positions[0])

    # Total energy is the sum of kinetic and potential energy
    total_energy = kinetic_energy + potential_energy

    # Optionally log the energies and system state to the provided log file
    if log_file is not None:
        log_file.write(f"{istep}, {potential_energy}, {kinetic_energy}, {total_energy}, {system.positions[0]}, {system.velocities[0]}\n")

    return kinetic_energy, potential_energy, total_energy
