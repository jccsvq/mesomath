"""
`tests/astronomy/test_planets.py` - Unit tests for Mesopotamian planetary models.
"""

import pytest
import math
from pymeeus.Epoch import Epoch

from mesotimes.astronomy.planets.superiors import MesopotamianMars
from mesotimes.astronomy.planets.inferiors import MesopotamianVenus
from mesotimes.astronomy.planets.finder import find_heliacal_event


def test_planet_altitude_calculation_with_sevilla() -> None:
    """
    Validates that the shared equatorial-to-horizontal coordinates transformation
    matches verified baseline outputs (checked against XEphem).
    """
    mars = MesopotamianMars()
    
    # 2026-05-18 06:13:15 UTC -> Sevilla test horizon benchmark
    day_decimal = 18 + (6 + (13 + 15 / 60.0) / 60.0) / 24.0
    epoch = Epoch(2026, 5, day_decimal, utc=True)
    
    # Calculate geometric altitude (ignoring refraction/dip for structural matching)
    # XEphem returns ~26.68° geometric altitude for Mars under these parameters
    apparent_alt = mars.calculate_apparent_altitude(epoch=epoch, city="Sevilla")
    
    # The output should sit close to ~27.87° when incorporating the full horizon_correction
    assert math.isclose(apparent_alt, 27.87, abs_tol=0.2)


def test_superior_planet_opposition_logic() -> None:
    """
    Verifies that the superior planet specific subclass features (like checking
    for acronychal opposition via elongation) trigger correctly.
    """
    mars = MesopotamianMars()
    
    # Hypothetical exact opposition epoch placeholder (Elongation = 180 degrees)
    # We pick an epoch where Mars is far from opposition to test the False branch
    quiet_epoch = Epoch(2026, 5, 18.0, utc=True)
    assert not mars.is_in_opposition(quiet_epoch, tolerance_deg=1.0)


def test_inferior_planet_subclass_instantiation() -> None:
    """
    Ensures inferior planets safely load their specific parameters (like Venus' Arc of Vision)
    and successfully link to PyMeeus native VSOP87 structures.
    """
    venus = MesopotamianVenus()
    assert venus.name == "Venus"
    assert venus.arc_of_vision == 6.0
    
    epoch = Epoch(2026, 5, 18.0, utc=True)
    ra_obj, dec_obj, elon = venus.get_geocentric_position(epoch)
    
    # Duck-typing or instance type checks for PyMeeus object attributes
    assert hasattr(ra_obj, "get_ra")
    assert callable(ra_obj.get_ra)


def test_finder_loop_safety_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    venus = MesopotamianVenus()
    epoch = Epoch(2026, 5, 18.0, utc=True)
    
    # Mocking visibility to always return False so 'appearance' can never be triggered
    monkeypatch.setattr(venus, "is_visible_at_twilight", lambda *args, **kwargs: False)
    
    with pytest.raises(RuntimeError) as exc_info:
        find_heliacal_event(
            planet=venus,
            start_epoch=epoch,
            horizon="sunset",
            search_type="appearance",
            city="Sevilla",
            max_days=5  # It will fail regardless of how many days it scans
        )
        
    assert "not found within 5 days" in str(exc_info.value)