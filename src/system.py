class System:
    """
    Represents a physical system with particles, including their properties and interactions.

    This class handles particle initialization, positions, velocities, and forces, and interacts
    with a provided potential to calculate forces acting on the particles.

    Attributes:
        mass (float): Mass of the particles in the system.
        potential: An object representing the potential energy of the system, which must have a
                   `force` method to compute forces given positions.
        positions (np.ndarray or None): Array of particle positions.
        velocities (np.ndarray or None): Array of particle velocities.
        forces (np.ndarray or None): Array of forces acting on the particles, initialized based on
                                     the current positions and potential.
    """

    def __init__(self, mass: float, potential):
        """
        Initialize the system with particle mass and the potential.

        Parameters:
            mass (float): The mass of the particles in the system.
            potential: An object representing the potential energy of the system. 
                       It must implement a `force` method to compute forces as a function of positions.
        """
        self.mass = mass
        self.potential = potential
        self.positions = None  # Positions of particles (to be initialized)
        self.velocities = None  # Velocities of particles (to be initialized)
        self.forces = None  # Forces acting on particles (computed based on positions)

    def initialize(self, positions, velocities):
        """
        Initialize the system with positions and velocities of particles.

        This method also calculates the initial forces based on the provided positions
        and the given potential.

        Parameters:
            positions (np.ndarray): Initial positions of particles.
            velocities (np.ndarray): Initial velocities of particles.
        """
        self.positions = positions
        self.velocities = velocities
        # Compute the initial forces based on the potential and positions
        self.forces = self.potential.force(self.positions)

