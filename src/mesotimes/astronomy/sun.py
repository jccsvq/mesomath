"""
`astronomy/sun.py` - Solar coordinates, cardinal events, and daytime metrics.

This module provides tools to compute solar ephemerides, equinoxes, solstices,
local rotational times for sunrise/sunset, and the historical duration of the
Babylonian day (sunset to sunset).
"""

import math
from typing import Literal
from juliandate import from_gregorian, from_julian  # type: ignore

from mesotimes.astronomy.core import (
    _horner,
    delta_t,
    get_horizon_dip,
    mesopotamian_cities,
)
from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun


def vernal_equinox(year: int) -> float:
    """
    Calculates the approximate Julian Date (JD) of the vernal equinox.
    Based on J. Meeus's Astronomical Algorithms, incorporating Delta T (ΔT)
    corrections for historical accuracy.

    Range: -1000 to 3000

    :param year: Astronomical year
    :type year: int
    :return: Julian Date of the vernal equinox
    :rtype: float
    """
    a1 = [1721139.29189, 365242.13740, 0.06134, 0.00111, -0.00071]
    a2 = [2451623.80984, 365242.37404, 0.05169, -0.00411, -0.00057]
    
    if -1000 <= year < 1000:
        a = a1
        y = year / 1000.0
    elif 1000 <= year < 3000:
        a = a2
        y = (year - 2000) / 1000.0
    else:
        raise ValueError("Year must be between -1000 and 3000")
        
    jd = _horner(y, a)
    return jd - delta_t(year, 6) / 86400.0


def summer_solstice(year: int) -> float:
    """
    Calculates the approximate Julian Date (JD) of the summer solstice.
    Based on J. Meeus's Astronomical Algorithms, incorporating Delta T (ΔT)
    corrections for historical accuracy.

    Range: -1000 to 3000

    :param year: Astronomical year
    :type year: int
    :return: Julian Date of the summer solstice
    :rtype: float
    """
    a1 = [1721233.25401, 365241.72562, -0.05323, 0.00907, 0.00025]
    a2 = [2451716.56767, 365241.62603, 0.00325, 0.00888, -0.00030]
    
    if -1000 <= year < 1000:
        a = a1
        y = year / 1000.0
    elif 1000 <= year < 3000:
        a = a2
        y = (year - 2000) / 1000.0
    else:
        raise ValueError("Year must be between -1000 and 3000")
        
    jd = _horner(y, a)
    return jd - delta_t(year, 6) / 86400.0


def autumnal_equinox(year: int) -> float:
    """
    Calculates the approximate Julian Date (JD) of the autumnal equinox.
    Based on J. Meeus's Astronomical Algorithms, incorporating Delta T (ΔT)
    corrections for historical accuracy.

    Range: -1000 to 3000

    :param year: Astronomical year
    :type year: int
    :return: Julian Date of the autumnal equinox
    :rtype: float
    """
    a1 = [1721325.70455, 365242.49558, -0.11677, -0.00297, 0.00074]
    a2 = [2451810.21715, 365242.01767, -0.11575, 0.00337, 0.00078]
    
    if -1000 <= year < 1000:
        a = a1
        y = year / 1000.0
    elif 1000 <= year < 3000:
        a = a2
        y = (year - 2000) / 1000.0
    else:
        raise ValueError("Year must be between -1000 and 3000")
        
    jd = _horner(y, a)
    return jd - delta_t(year, 6) / 86400.0


def winter_solstice(year: int) -> float:
    """
    Calculates the approximate Julian Date (JD) of the winter solstice.
    Based on J. Meeus's Astronomical Algorithms, incorporating Delta T (ΔT)
    corrections for historical accuracy.

    Range: -1000 to 3000

    :param year: Astronomical year
    :type year: int
    :return: Julian Date of the winter solstice
    :rtype: float
    """
    a1 = [1721414.39987, 365242.88257, -0.00769, -0.00933, -0.00006]
    a2 = [2451900.05952, 365242.74049, -0.06223, -0.00823, 0.00032]
    
    if -1000 <= year < 1000:
        a = a1
        y = year / 1000.0
    elif 1000 <= year < 3000:
        a = a2
        y = (year - 2000) / 1000.0
    else:
        raise ValueError("Year must be between -1000 and 3000")
        
    jd = _horner(y, a)
    return jd - delta_t(year, 6) / 86400.0


def get_season_day_str(
    year: int, month: int, day: int, calendar: Literal["julian", "gregorian"] = "julian"
) -> str:
    """
    Returns a string indicating the current day count within its astronomical season.
    Example: 'Day: 34 of spring'

    :param year: Calendar year
    :type year: int
    :param month: Calendar month
    :type month: int
    :param day: Calendar day
    :type day: int
    :param calendar: Calendar system ("julian" or "gregorian"), defaults to "julian"
    :type calendar: str, optional
    :return: String indicating the current day within the season
    :rtype: str
    """

    def date_to_jd(y_val: int, m_val: int, d_val: int, cal: str) -> float:
        if cal == "julian":
            return float(from_julian(y_val, m_val, d_val))
        elif cal == "gregorian":
            return float(from_gregorian(y_val, m_val, d_val))
        else:
            raise ValueError("Unsupported calendar system")

    current_jd = date_to_jd(year, month, day, calendar)

    eq_vernal = vernal_equinox(year)
    sol_summer = summer_solstice(year)
    eq_autumn = autumnal_equinox(year)
    sol_winter = winter_solstice(year)

    if current_jd < eq_vernal:
        start_jd = winter_solstice(year - 1)
        season = "winter"
    elif current_jd < sol_summer:
        start_jd = eq_vernal
        season = "spring"
    elif current_jd < eq_autumn:
        start_jd = sol_summer
        season = "summer"
    elif current_jd < sol_winter:
        start_jd = eq_autumn
        season = "autumn"
    else:
        start_jd = sol_winter
        season = "winter"

    days_in_season = int(current_jd - start_jd) + 1
    return f"Day: {days_in_season} of {season}"


def sun_rise_transit_set(
    year: int,
    month: int,
    day: int,
    city: str = "Babylon",
    ziggurat: float = 0.0,
) -> tuple[float, float, float, float, float, float]:
    """
    Calculates solar rise, transit, and set times considering atmospheric
    refraction and observer elevation.

    The geometric horizon is adjusted by -0.833° to account for
    standard refraction and solar semi-diameter. Elevation (ziggurat)
    adds a dip correction to the horizon.

    :param year: Calendar year
    :type year: int
    :param month: Calendar month
    :type month: int
    :param day: Calendar day
    :type day: int
    :param city: Name of the site in mesopotamian_cities, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Observer height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: (rise_ut, transit_ut, set_ut, rise_local, transit_local, set_local)
             in decimal hours.
    :rtype: tuple[float, float, float, float, float, float]
    """
    # 1. Geographical and horizon parameters
    # Note: Explicit casting to satisfy strict float expectations from metadata dictionary
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    h0 = -0.833 - get_horizon_dip(alt)

    # 2. Solar Position at approximate midday (12h UT) using arguments
    e_mid = Epoch(year, month, day, 12, 0, 0, utc=True)
    res = Sun.apparent_rightascension_declination_coarse(e_mid)
    dec_deg = res[1]

    # 3. Equation of Time (converted to decimal hours)
    e_min, e_sec = Sun.equation_of_time(e_mid)
    eq_time = (e_min + e_sec / 60.0) / 60.0

    # 4. Rotational UT Transit Calculation
    lon_hours = lon / 15.0
    transit_ut = (12.0 - lon_hours - eq_time) % 24

    # 5. Spherical Trigonometry for Hour Angle (H)
    phi_rad = math.radians(lat)
    delta_rad = math.radians(dec_deg)
    h0_rad = math.radians(h0)

    cos_H = (math.sin(h0_rad) - math.sin(phi_rad) * math.sin(delta_rad)) / (
        math.cos(phi_rad) * math.cos(delta_rad)
    )

    if cos_H > 1 or cos_H < -1:
        raise ValueError("Circumpolar sun detected. Body does not rise or set.")

    H_deg = math.degrees(math.acos(cos_H))
    H_hours = H_deg / 15.0

    # 6. Sunrise and Sunset in Rotational UT
    rise_ut = (transit_ut - H_hours) % 24
    set_ut = (transit_ut + H_hours) % 24

    # 7. Strict Local Apparent Time Conversion (UT + Lon/15)
    rise_local = (rise_ut + lon_hours) % 24
    transit_local = (transit_ut + lon_hours) % 24
    set_local = (set_ut + lon_hours) % 24

    return rise_ut, transit_ut, set_ut, rise_local, transit_local, set_local


def bab_day_duration(
    jd: float, city: str = "Babylon", ziggurat: float = 0.0
) -> tuple[float, float, float, float, float, float, float]:
    """
    Returns the duration parameters in hours for a specific Babylonian day
    (between two consecutive sunsets).

    :param jd: Julian Date representing the target day
    :type jd: float
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: Tuple containing (duration, diurnal, nocturnal, start UT, sunrise UT, transit UT, end UT) in decimal hours
    :rtype: tuple[float, float, float, float, float, float, float]
    """
    e = Epoch(int(jd), utc=True)
    year, month, day = e.get_date()

    rise2, transit2, set2, _, _, _ = sun_rise_transit_set(
        year, month, day, city=city, ziggurat=ziggurat
    )
    
    # Babylonian day starts with previous sunset
    y, m, d = (e - 1).get_date()
    _, _, set1, _, _, _ = sun_rise_transit_set(y, m, d, city=city, ziggurat=ziggurat)
    
    duration = set2 - set1 + 24
    diurnal = set2 - rise2
    nocturnal = rise2 - set1 + 24

    return duration, diurnal, nocturnal, set1, rise2, transit2, set2