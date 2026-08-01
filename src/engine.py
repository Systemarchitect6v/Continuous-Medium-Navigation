"""
6-Vector Continuous Medium Engine
Resolves instantaneous tracking angle (theta_i) and dynamic equilibrium state
from a localized 6-element stress-strain tensor field.
"""

import math
import numpy as np


class SixVectorEngine:
    """
    Calculates dynamic equilibrium and instantaneous tracking angle (theta_i)
    for an autonomous vessel immersed in a continuous fluid medium.
    """

    def __init__(self, trim_factor: float = 0.0):
        """
        Initialize the 6-Vector Engine.
        :param trim_factor: Structural trimming factor (phi_trim) based on hull geometry.
        """
        self.phi_trim = trim_factor

    def compute_tracking_angle(self, stress_tensor: np.ndarray) -> dict:
        """
        Resolves the instantaneous tracking angle (theta_i) from local stress-strain vectors.

        :param stress_tensor: 6-element numpy array [sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_zx]
        :return: Dictionary containing theta_i (rad/deg), residual shear strain, and equilibrium state.
        """
        if len(stress_tensor) != 6:
            raise ValueError("Stress tensor field must contain exactly 6 elements: [s_xx, s_yy, s_zz, t_xy, t_yz, t_zx]")

        sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_zx = stress_tensor

        # Normal stress difference along primary cardinal axes
        delta_sigma = sigma_xx - sigma_yy

        # Resolve theta_i using arctan2 to handle directional signs & zero-division safely
        if math.isclose(delta_sigma, 0.0, abs_tol=1e-9) and math.isclose(tau_xy, 0.0, abs_tol=1e-9):
            raw_angle = 0.0
        else:
            raw_angle = 0.5 * math.atan2(2.0 * tau_xy, delta_sigma)

        theta_i = raw_angle + self.phi_trim

        # Calculate residual shear strain magnitude
        residual_shear = math.sqrt(tau_xy**2 + tau_yz**2 + tau_zx**2)

        # Dynamic equilibrium criteria: shear strain minimized relative to primary stress
        in_equilibrium = math.isclose(residual_shear, 0.0, abs_tol=1e-6) or (abs(theta_i) < 1e-4)

        return {
            "theta_i_rad": theta_i,
            "theta_i_deg": math.degrees(theta_i),
            "residual_shear": residual_shear,
            "in_equilibrium": in_equilibrium
        }


if __name__ == "__main__":
    # Quick sanity check: Uniform medium with transverse shear component
    engine = SixVectorEngine(trim_factor=0.0)
    
    # Example tensor: [sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_zx]
    test_tensor = np.array([100.0, 80.0, 90.0, 15.0, 0.0, 0.0])
    
    result = engine.compute_tracking_angle(test_tensor)
    print("--- 6-Vector Engine Sanity Check ---")
    print(f"Tracking Angle (theta_i): {result['theta_i_deg']:.4f}°")
    print(f"Residual Shear Strain:   {result['residual_shear']:.4f}")
    print(f"Dynamic Equilibrium:    {result['in_equilibrium']}")
