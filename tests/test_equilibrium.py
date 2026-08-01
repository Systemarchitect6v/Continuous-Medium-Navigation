"""
Unit Test Suite: 6-Vector Dynamic Equilibrium Verification
Tests instantaneous tracking angle (theta_i) resolution and zero-lag convergence 
under simulated fluid shear and hydrostatic pressure tensors.
"""

import math
import numpy as np
import pytest
from src.engine import SixVectorEngine


@pytest.fixture
def default_engine():
    """Provides a default SixVectorEngine instance with zero hull trim factor."""
    return SixVectorEngine(trim_factor=0.0)


def test_hydrostatic_equilibrium(default_engine):
    """
    Verifies that under uniform hydrostatic pressure (zero shear components),
    the tracking angle remains perfectly at zero (Dynamic Equilibrium).
    """
    # Isotropic pressure field: s_xx = s_yy = s_zz = 100 kPa, zero shear
    hydrostatic_tensor = np.array([100.0, 100.0, 100.0, 0.0, 0.0, 0.0])
    
    result = default_engine.compute_tracking_angle(hydrostatic_tensor)
    
    assert math.isclose(result["theta_i_rad"], 0.0, abs_tol=1e-7)
    assert result["residual_shear"] == 0.0
    assert result["in_equilibrium"] is True


def test_transverse_shear_alignment(default_engine):
    """
    Verifies that a transverse shear component (tau_xy) correctly induces an 
    alignment tracking angle theta_i to neutralize shear resistance.
    """
    # Tensor with normal differential (20 kPa) and shear stress (10 kPa)
    shear_tensor = np.array([120.0, 100.0, 90.0, 10.0, 0.0, 0.0])
    
    result = default_engine.compute_tracking_angle(shear_tensor)
    
    # Expected raw angle: 0.5 * arctan2(2 * 10, 120 - 100) = 0.5 * arctan2(20, 20) = 22.5 deg (pi/8 rad)
    expected_rad = math.pi / 8.0
    
    assert math.isclose(result["theta_i_rad"], expected_rad, abs_tol=1e-5)
    assert math.isclose(result["theta_i_deg"], 22.5, abs_tol=1e-3)


def test_trim_factor_offset():
    """
    Verifies that hull geometry trim factor (phi_trim) applies a constant structural shift.
    """
    trim_angle_rad = math.radians(2.5)  # 2.5 degree hull offset
    trimmed_engine = SixVectorEngine(trim_factor=trim_angle_rad)
    
    tensor = np.array([100.0, 100.0, 100.0, 0.0, 0.0, 0.0])
    result = trimmed_engine.compute_tracking_angle(tensor)
    
    assert math.isclose(result["theta_i_rad"], trim_angle_rad, abs_tol=1e-7)
    assert math.isclose(result["theta_i_deg"], 2.5, abs_tol=1e-5)


def test_invalid_tensor_dimension(default_engine):
    """
    Ensures the engine enforces 6-vector state space integrity.
    """
    invalid_tensor = np.array([100.0, 50.0, 0.0])  # Only 3 elements
    
    with pytest.raises(ValueError, match="must contain exactly 6 elements"):
        default_engine.compute_tracking_angle(invalid_tensor)
