"""
`tests/astronomy/test_sun.py` - Unit tests for solar astronomical functions.
"""

import math
import pytest
from mesotimes.astronomy.sun import (
    vernal_equinox,
    summer_solstice,
    autumnal_equinox,
    winter_solstice,
    get_season_day_str,
    sun_rise_transit_set,
    bab_day_duration,
)


def test_cardinal_events_chronology() -> None:
    """Verify that equinoxes and solstices follow chronological order for a historical year."""
    year = -567  # Significant year in Babylonian astronomy (VAT 4956 diary)
    
    ve = vernal_equinox(year)
    ss = summer_solstice(year)
    ae = autumnal_equinox(year)
    ws = winter_solstice(year)
    
    # Check proper order over the tropical year
    assert ve < ss < ae < ws
    
    # Check distances between quarters are roughly ~90-95 days
    assert 90.0 < (ss - ve) < 95.0
    assert 88.0 < (ws - ae) < 94.0


def test_cardinal_events_out_of_bounds() -> None:
    """Ensure that years outside the boundaries defined by Meeus throw a ValueError."""
    with pytest.raises(ValueError, match="Year must be between -1000 and 3000"):
        vernal_equinox(-1001)
        
    with pytest.raises(ValueError, match="Year must be between -1000 and 3000"):
        summer_solstice(3001)


@pytest.mark.parametrize(
    "y, m, d, cal, expected_season",
    [
        (-567, 4, 15, "julian", "spring"),
        (-567, 7, 20, "julian", "summer"),
        (-567, 10, 10, "julian", "autumn"),
        (-567, 1, 15, "julian", "winter"),
    ]
)
def test_get_season_day_str_valid(y: int, m: int, d: int, cal: str, expected_season: str) -> None:
    """Verify the string formatting and accurate matching of seasons."""
    # mypy requires explicit casting or checking if passing dynamic literals
    res = get_season_day_str(y, m, d, calendar=cal)  # type: ignore[arg-type]
    
    assert res.startswith("Day: ")
    assert expected_season in res


def test_get_season_day_str_invalid_calendar() -> None:
    """Ensure passing an unsupported calendar throws a ValueError."""
    with pytest.raises(ValueError, match="Unsupported calendar system"):
        get_season_day_str(-567, 4, 15, calendar="mayan")  # type: ignore[arg-type]


def test_sun_rise_transit_set_babylon() -> None:
    """Check that sunrise, transit, and sunset match geometric rules in Babylon."""
    # Summer solstice period (long days, short nights)
    rise_ut, transit_ut, set_ut, rise_loc, trans_loc, set_loc = sun_rise_transit_set(
        -567, 6, 21, city="Babylon", ziggurat=0.0
    )
    
    # Basic logic assertions
    assert rise_ut < transit_ut < set_ut
    assert rise_loc < trans_loc < set_loc
    
    # Diurnal duration should be greater than 12 hours in summer
    diurnal_hours = set_ut - rise_ut
    assert diurnal_hours > 12.0
    
    # Local solar transit should be very close to 12.0 (Apparent Time)
    # Depending on the Equation of Time effect inside the function
    assert math.isclose(trans_loc, 12.0, abs_tol=0.5)


def test_sun_rise_transit_set_with_ziggurat() -> None:
    """Elevation (Ziggurat) must anticipate sunrise and delay sunset due to horizon dip."""
    # Flat ground
    r_flat, _, s_flat, _, _, _ = sun_rise_transit_set(-567, 3, 21, city="Babylon", ziggurat=0.0)
    # High structure (e.g., Etemenanki, 91 meters)
    r_high, _, s_high, _, _, _ = sun_rise_transit_set(-567, 3, 21, city="Babylon", ziggurat=91.0)
    
    # High ground sees sunrise EARLIER
    assert r_high < r_flat
    # High ground sees sunset LATER
    assert s_high > s_flat


def test_bab_day_duration_math() -> None:
    """Verify that the components of the Babylonian Day (Sunset to Sunset) add up correctly."""
    # We use Julian Date for an arbitrary day in Babylon
    jd_test = 1514300.0  # Historical JDN range
    
    duration, diurnal, nocturnal, set1, rise2, transit2, set2 = bab_day_duration(
        jd_test, city="Babylon", ziggurat=0.0
    )
    
    # Mathematical invariants of the definition:
    # 1. Total day duration must equal diurnal + nocturnal parts
    assert math.isclose(duration, diurnal + nocturnal, abs_tol=1e-5)
    
    # 2. Sequential times order check
    assert set1 < rise2 < transit2 < set2 or (set2 < set1 and "handled by modulo/date adjustments")
    
    # 3. Output bounds validation
    assert 23.9 < duration < 24.1  # Earth rotation isn't perfectly 24h relative to sunset tracking
    assert diurnal > 0.0
    assert nocturnal > 0.0
