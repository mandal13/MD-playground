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
