"""
This module contains classes for different kinds of potentials (and corresponding forces) 
that can be used in molecular dynamics simulations.

Classes:
    Harmonic: Implements the harmonic (spring-like) potential.
    DoubleWell: Implements a double-well potential with optional asymmetry.

Usage:
    Import this module and use the `Harmonic` or `DoubleWell` classes to calculate 
    potential energies and forces for molecular dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt

class Harmonic:
    """
    Represents a harmonic potential of the form V(x) = 0.5 * k * (x - x0)^2.

    Attributes:
        k (float): Spring constant.
        x0 (float): Equilibrium position of the potential.
    """

    def __init__(self, k: float, x0: float = 0.0):
        """
        Initializes the harmonic potential.

        Args:
            k (float): Spring constant.
            x0 (float, optional): Equilibrium position. Defaults to 0.0.
        """
        self.k = k
        self.x0 = x0

    def potential(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the potential energy for a given position x.

        Args:
            x (ndarray): Position(s) where the potential is evaluated.

        Returns:
            ndarray: Potential energy at the given position(s).
        """
        return 0.5 * self.k * (x - self.x0)**2

    def force(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the force for a given position x.

        Args:
            x (ndarray): Position(s) where the force is evaluated.

        Returns:
            ndarray: Force at the given position(s).
        """
        return -self.k * (x - self.x0)

class DoubleWell:
    """
    Represents a double-well potential of the form 
    V(x) = a * x^4 - b * x^2 + c * x + d.

    Customizing the Potential:
    Well Depth: Change b (larger b makes the wells deeper and further apart).
    Asymmetry: Adjust c to make one well shallower or deeper than the other.
    Steepness: Modify a to control the "width" and steepness of the wells.

    Attributes:
        a (float): Coefficient for the quartic term (x^4).
        b (float): Coefficient for the quadratic term (x^2).
        c (float): Coefficient for the linear term (asymmetry).
        d (float): Constant offset.
    """

    def __init__(self, a: float = 1.0, b: float = 1.0, c: float = 0.5, d: float = 0.0):
        """
        Initializes the double-well potential.

        Args:
            a (float, optional): Coefficient for the quartic term. Defaults to 1.0.
            b (float, optional): Coefficient for the quadratic term. Defaults to 1.0.
            c (float, optional): Coefficient for the linear term (asymmetry). Defaults to 0.5.
            d (float, optional): Constant offset. Defaults to 0.0.
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def potential(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the potential energy for a given position x.

        Args:
            x (ndarray): Position(s) where the potential is evaluated.

        Returns:
            ndarray: Potential energy at the given position(s).
        """
        return self.a * x**4 - self.b * x**2 + self.c * x + self.d

    def force(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the force for a given position x.

        Args:
            x (ndarray): Position(s) where the force is evaluated.

        Returns:
            ndarray: Force at the given position(s).
        """
        return -4.0 * self.a * x**3 + 2.0 * self.b * x - self.c

if __name__ == "__main__":
    # Demonstrate the harmonic potential
    k = 1.0
    x0 = 0.25
    harmonic = Harmonic(k, x0)

    x = np.linspace(-2, 2, 100)
    y_harmonic = harmonic.potential(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y_harmonic, label="Harmonic Potential", color="green")
    plt.xlabel("Position (x)")
    plt.ylabel("Potential Energy (V)")
    plt.title("Harmonic Potential")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Demonstrate the double-well potential
    a = 1.0
    b = 3.0
    c = 0.3
    d = 0.0
    doublewell = DoubleWell(a=a, b=b, c=c, d=d)

    x = np.linspace(-2, 2, 500)
    y_doublewell = doublewell.potential(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y_doublewell, label=f"Double-Well Potential ($a={a}, b={b}, c={c}, d={d}$)", color="blue")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.8)
    plt.axvline(0, color="black", linestyle="--", linewidth=0.8)
    plt.xlabel("Position (x)")
    plt.ylabel("Potential Energy (V)")
    plt.title("Asymmetric Double-Well Potential")
    plt.legend()
    plt.grid(True)
    plt.show()
