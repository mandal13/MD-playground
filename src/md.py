from system import System
from potentials_and_forces import Harmonic, DoubleWell
from integrators import VVIntegrator, LangevinIntegrator
from utils import compute_energies

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def run_md(args):
    """
    Run a molecular dynamics (MD) simulation based on the specified arguments.

    Parameters:
        args (Namespace): Parsed command-line arguments containing the following:
            - potential (str): The type of potential to use ("harmonic" or "double_well").
            - k (float): Force constant for the harmonic potential (if applicable).
            - x0 (float): Equilibrium position for the harmonic potential (if applicable).
            - mass (float): Mass of the particle.
            - positions (list of float): Initial positions of the particle(s).
            - velocities (list of float): Initial velocities of the particle(s).
            - sim_type (str): Type of simulation ("nve" for energy-conserving or "nvt" for thermostatted).
            - dt (float): Time step for the integrator.
            - steps (int): Total number of MD steps to run.
            - print_freq (int): Frequency of logging and output.
            - output (str): Path to the output file for logging simulation results.

    Returns:
        None: Writes simulation data to the specified output file.
    """
    # Assign potential based on user input
    if args.potential == "harmonic":
        potential = Harmonic(args.k, args.x0)  # Harmonic potential
    elif args.potential == "double_well":
        potential = DoubleWell()  # Double-well potential
    else:
        raise ValueError(f"Unknown potential type: {args.potential}")

    # Initialize the system with the specified mass and potential
    system = System(args.mass, potential)
    system.initialize(
        np.array(args.positions, dtype=np.float64), 
        np.array(args.velocities, dtype=np.float64)
    )

    # Initialize the appropriate integrator based on simulation type
    if args.sim_type == "nve":
        integrator = VVIntegrator(system, args.dt)  # Velocity Verlet integrator
    elif args.sim_type == "nvt":
        integrator = LangevinIntegrator()  # Langevin integrator (requires implementation)
    else:
        raise ValueError(f"Unknown simulation type: {args.sim_type}")

    # Open the output file for logging
    with open(args.output, "w") as file:
        # Run the molecular dynamics simulation
        for i in range(args.steps):
            integrator.step()  # Perform one integration step

            # Log energies and system state at specified intervals
            if i % args.print_freq == 0:
                compute_energies(system, i, log_file=file)


    # read the output file and plot the positions and velocities
    
    df = pd.read_csv("output.log", sep=", ", header=None)
    #data = np.loadtxt("output.txt", delimiter=",")
    data = np.array(df, dtype=np.float64)
    print(data.ndim, len(data), data.shape)
    
    #plt.plot(data[:, 0], data[:, 1], label = "Position")
    #plt.plot(data[:, 0], data[:, 2], label = "Velocity")
    plt.plot(data[:, 0], data[:, 1], label = "Potential Energy")
    plt.plot(data[:, 0], data[:, 2], label = "Kinetic Energy")
    plt.plot(data[:, 0], data[:, 3], label = "Total Energy")
    plt.legend()
    plt.show()
