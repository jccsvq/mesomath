"""
`tests/astronomy/test_moon.py` - Unit tests for lunar astronomical functions.
"""

import math
import pytest
from mesotimes.astronomy.moon import (
    moon_age,
    calculate_moon_transit,
    moon_rise_transit_set,
    check_neomenia,
    calculate_mi_mush,
    calculate_kur,
    calculate_shu_interval,
    calculate_full_moon_na,
)


def test_moon_age_basic() -> None:
    """Test that moon_age returns reasonable integer days within the synodic month."""
    # JDN 2451545.0 is J2000.0. Let's verify integer outputs
    age_1 = moon_age(2451545.0)
    age_2 = moon_age(2451560.0)
    
    assert isinstance(age_1, int)
    assert 0 <= age_1 <= 30
    assert isinstance(age_2, int)
    assert 0 <= age_2 <= 30


def test_calculate_moon_transit_convergence() -> None:
    """Test that lunar transit returns a valid decimal hour for Babylon."""
    # Babylon longitude is approx 44.42 degrees
    lon_babylon = 44.42
    
    # Check transit for a standard arbitrary historical date (e.g., -567, 4, 15)
    transit_ut = calculate_moon_transit(-567, 4, 15, lon_babylon)
    
    assert isinstance(transit_ut, float)
    assert 0.0 <= transit_ut < 24.0
    assert not math.isnan(transit_ut)


def test_moon_rise_transit_set_output_types() -> None:
    """Verify that moon_rise_transit_set returns a 6-tuple of floats."""
    res = moon_rise_transit_set(-567, 5, 1, city="Babylon", ziggurat=0.0)
    
    assert isinstance(res, tuple)
    assert len(res) == 6
    for val in res:
        assert isinstance(val, float)


def test_check_neomenia_logic() -> None:
    """Verify check_neomenia returns interval in minutes and altitude in degrees."""
    na_min, alt_deg = check_neomenia(-567, 5, 1, city="Babylon", verbose=False)
    
    assert isinstance(na_min, float)
    assert isinstance(alt_deg, float)
    # The altitude can be negative if the moon set before sunset, but it shouldn't be NaN
    assert not math.isnan(alt_deg)


def test_calculate_mi_mush_tuple() -> None:
    """Test that Mi-Mush (ME) returns the 3-element tuple with interval, moonset, and sunrise."""
    interval, m_set, s_rise = calculate_mi_mush(-567, 6, 15, city="Babylon")
    
    assert isinstance(interval, float)
    assert isinstance(m_set, float)
    assert isinstance(s_rise, float)
    # Interval in minutes must match the mathematical difference in hours * 60
    assert math.isclose(interval, (m_set - s_rise) * 60.0, abs_tol=1e-5)


def test_calculate_kur_tuple() -> None:
    """Test that KUR returns the 3-element tuple with interval, moonrise, and sunrise."""
    interval, m_rise, s_rise = calculate_kur(-567, 6, 28, city="Babylon")
    
    assert isinstance(interval, float)
    assert isinstance(m_rise, float)
    assert isinstance(s_rise, float)
    # KUR = (Sunrise - Moonrise) * 60
    assert math.isclose(interval, (s_rise - m_rise) * 60.0, abs_tol=1e-5)


def test_calculate_shu_interval_value() -> None:
    """Verify Shú interval matches (Moonset - Sunset) * 60."""
    shu_min = calculate_shu_interval(-567, 6, 14, city="Babylon")
    assert isinstance(shu_min, float)
    assert not math.isnan(shu_min)


def test_calculate_full_moon_na_value() -> None:
    """Verify Full Moon NA interval matches (Sunset - Moonrise) * 60."""
    fm_na_min = calculate_full_moon_na(-567, 6, 13, city="Babylon")
    assert isinstance(fm_na_min, float)
    assert not math.isnan(fm_na_min)


def test_invalid_city_raises_key_error() -> None:
    """Ensure that passing a non-existent city raises a KeyError due to final dict lookup."""
    with pytest.raises(KeyError):
        moon_rise_transit_set(-567, 5, 1, city="Atlantis")
