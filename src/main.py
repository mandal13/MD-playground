"""
Main script for running molecular dynamics (MD) simulations.

This script serves as the entry point for setting up and running MD simulations 
with customizable potentials, system properties, and integration schemes. It allows 
users to specify simulation parameters via command-line arguments and outputs 
the simulation results to a log file.

Usage:
    python main.py --potential harmonic --positions 1.0 --velocities 0.5 --steps 1000
"""

from md import run_md
import argparse

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run a molecular dynamics simulation.")

    # Potential-related arguments
    parser.add_argument(
        "--potential", type=str, default="harmonic", 
        help="Type of potential to use: 'harmonic' or 'double_well'."
    )
    parser.add_argument(
        "--x0", type=float, default=0.0, 
        help="Equilibrium position of the harmonic potential (only for harmonic)."
    )
    parser.add_argument(
        "--k", type=float, default=1.0, 
        help="Spring constant of the harmonic potential (only for harmonic)."
    )

    # System properties
    parser.add_argument(
        "--mass", type=float, default=1.0, 
        help="Mass of the particle."
    )
    parser.add_argument(
        "--positions", type=float, default=[2.0], 
        help="Initial position(s) of the particle(s)."
    )
    parser.add_argument(
        "--velocities", type=float, default=[4.0], 
        help="Initial velocity(ies) of the particle(s)."
    )

    # Simulation control
    parser.add_argument(
        "--sim_type", type=str, default="nve", 
        help="Simulation type: 'nve' for energy-conserving or 'nvt' for thermostatted dynamics."
    )
    parser.add_argument(
        "--output", type=str, default="output.log", 
        help="Path to the output file for logging results."
    )
    parser.add_argument(
        "--steps", type=int, default=10000, 
        help="Number of simulation steps to run."
    )
    parser.add_argument(
        "--dt", type=float, default=0.002, 
        help="Time step for the integration (in arbitrary units)."
    )
    parser.add_argument(
        "--print_freq", type=int, default=100, 
        help="Frequency at which results are logged."
    )

    # Thermostat-related arguments
    parser.add_argument(
        "--thermostat", type=str, default="none", 
        help="Thermostat type to apply: 'none' or 'langevin'."
    )
    parser.add_argument(
        "--temperature", type=float, default=1.0, 
        help="Target temperature for Langevin thermostat."
    )
    parser.add_argument(
        "--gamma", type=float, default=1.0, 
        help="Friction coefficient for the Langevin thermostat."
    )
    parser.add_argument(
        "--seed", type=int, default=42, 
        help="Random seed for reproducibility (used in Langevin dynamics)."
    )

    # Parse arguments
    args = parser.parse_args()

    # Run the molecular dynamics simulation
    run_md(args)





# Main file for running molecular dynamics simulations

from md import run_md


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--potential", type=str, default="harmonic", help="Potential type: harmonic or double_well")
    parser.add_argument("--x0", type=float, default=0.0, help="Equilibrium position of the harmonic potential")
    parser.add_argument("--k", type=float, default=1.0, help="Spring constant of the harmonic potential")

    parser.add_argument("--mass", type=float, default=1.0, help="Mass of the particle")
    parser.add_argument("--positions", type=float, default=[2.0], help="Initial positions")
    parser.add_argument("--velocities", type=float, default=[4.0], help="Initial velocities")

    parser.add_argument("--sim_type", type=str, default="nve", help="Simulation type: nve or nvt")
    parser.add_argument("--output", type=str, default="output.log", help="Output file")
    parser.add_argument("--steps", type=int, default=10000, help="Number of MD steps")
    parser.add_argument("--dt", type=float, default=0.002, help="Time step")
    parser.add_argument("--print_freq", type=int, default=100, help="Print frequency")
    
    
    parser.add_argument("--thermostat", type=str, default="none", help="Thermostat type: none or langevin")
    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature for Langevin thermostat")
    parser.add_argument("--gamma", type=float, default=1.0, help="Friction coefficient for Langevin thermostat")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    
    
    args = parser.parse_args()

    run_md(args)