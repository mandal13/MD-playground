from system import System
from potentials_and_forces import Harmonic, DoubleWell
from integrators import VVIntegrator, LangevinIntegrator
from utils import compute_energies, animate

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
        np.array([args.positions], dtype=np.float64), 
        np.array([args.velocities], dtype=np.float64)
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

    if args.animation:
        # read the output file and animate the results
        df = pd.read_csv(args.output, sep=",", header=None)
        data = np.array(df, dtype=np.float64)
        n_steps = len(data)
        potential_energies, kinetic_energies, total_energies = data[:, 1], data[:, 2], data[:, 3]
        positions = data[:, 4]

        animate(n_steps, potential_energies, kinetic_energies, total_energies, potential.potential, positions, args.dt*args.print_freq, save_file=args.save_file)
