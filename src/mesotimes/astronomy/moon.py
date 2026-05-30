"""
`astronomy/moon.py` - Lunar ephemerides, topocentric event solvers, and 
Babylonian astronomical diary intervals.

This module provides tools to track lunar age, compute precise topocentric 
moonrise, transit, and moonset times, and analyze the six classical Babylonian 
lunar intervals (na, šú, me, kúr, etc.) for historical diary reconstructions.
"""

import math

from mesotimes.astronomy.core import (
    _historical_gmst_degrees,
    get_horizon_dip,
    mesopotamian_cities,
)
from mesotimes.astronomy.sun import (
    sun_rise_transit_set,
)
from pymeeus.Epoch import Epoch
from pymeeus.Moon import Moon


def moon_age(jd: float, offset: float = 0.0) -> int:
    """
    Calculates the days elapsed since the last New Moon using a coarse
    linear model.

    This function uses the Mean Synodic Month constant from the
    'Five Millennium Canon of Solar Eclipses'.

    :param jd: Julian Day (UT)
    :type jd: float
    :param offset: Adjustment for local events (e.g., sunset), defaults to 0.0
    :type offset: float, optional
    :return: Moon age in days
    :rtype: int
    """
    # Lunar Month (according to Five Millenium Cannon of Solar Eclipses)
    synodic_month = 29.5305989171002
    m_inv = 0.0338631804488803
    moon0 = -83017.2906422287
    
    mean_phase = moon0 + (jd + offset) * m_inv
    fractional_phase = mean_phase - math.floor(mean_phase)
    age = synodic_month * fractional_phase
    return round(age)


def calculate_moon_event(
    year: int,
    month: int,
    day: int,
    lat: float,
    lon: float,
    dip: float,
    is_setting: bool = True,
    seed_ut: float = 12.0,
) -> float:
    """
    Iterative solver for lunar rise/set events using topocentric corrections.

    Accounts for Horizontal Parallax (pi) and atmospheric refraction.
    Iterates to find the exact UT where the Moon's limb touches the
    local horizon. Bypasses library limits for ancient Sidereal Time.

    :param year: Astronomical year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param lat: Latitude (degrees)
    :type lat: float
    :param lon: Longitude (degrees)
    :type lon: float
    :param dip: Horizon depth (refraction + geometric dip)
    :type dip: float
    :param is_setting: True for Moonset, False for Moonrise, defaults to True
    :type is_setting: bool, optional
    :param seed_ut: Initial UT guess, defaults to 12.0
    :type seed_ut: float, optional
    :return: Event UT in decimal hours (NaN if no event occurs)
    :rtype: float
    """
    phi_rad = math.radians(lat)
    h_sign = 1.0 if is_setting else -1.0
    hour_ut_est = seed_ut % 24.0

    for _ in range(4):
        safe_hour = hour_ut_est % 24.0

        h = int(safe_hour)
        m = int((safe_hour - h) * 60)
        s = ((safe_hour - h) * 60 - m) * 60
        e_est = Epoch(year, month, day, h, m, s, utc=True)

        ra_ang, dec_ang, _, ppi_ang = Moon.apparent_equatorial_pos(e_est)
        ra = ra_ang._deg
        dec = dec_ang._deg
        ppi = ppi_ang._deg

        h0 = (0.7275 * ppi) - 0.5667 - dip
        h0_rad = math.radians(h0)
        delta_rad = math.radians(dec)

        cos_H = (math.sin(h0_rad) - math.sin(phi_rad) * math.sin(delta_rad)) / (
            math.cos(phi_rad) * math.cos(delta_rad)
        )

        if cos_H > 1.0 or cos_H < -1.0:
            return float("nan")

        H_target = math.degrees(math.acos(cos_H))
        st_greenwich = _historical_gmst_degrees(e_est)
        H_current = (st_greenwich + lon - ra) % 360.0
        if H_current > 180.0:
            H_current -= 360.0

        delta_H = H_current - (h_sign * H_target)
        if delta_H > 180.0:
            delta_H -= 360.0
        if delta_H < -180.0:
            delta_H += 360.0

        dt_hours = delta_H / 15.04107
        hour_ut_est = (hour_ut_est - dt_hours) % 24.0

    return hour_ut_est


def calculate_moon_transit(year: int, month: int, day: int, lon: float) -> float:
    """
    Iterative solver for Moon Transit (Meridian Culmination).
    Target: Local Hour Angle (LHA) == 0.0

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param lon: Geographical Longitude
    :type lon: float
    :return: Moon transit UT in decimal hours
    :rtype: float
    """
    hour_ut_est = 12.0

    for _ in range(3):
        h = int(hour_ut_est)
        m = int((hour_ut_est - h) * 60)
        s = ((hour_ut_est - h) * 60 - m) * 60
        e_est = Epoch(year, month, day, h, m, s, utc=True)

        ra_ang, _, _, _ = Moon.apparent_equatorial_pos(e_est)
        ra = ra_ang._deg

        st_greenwich = _historical_gmst_degrees(e_est)

        H_current = (st_greenwich + lon - ra) % 360.0
        if H_current > 180.0:
            H_current -= 360.0

        dt_hours = H_current / 15.04107
        hour_ut_est = (hour_ut_est - dt_hours) % 24.0

    return hour_ut_est


def moon_rise_transit_set(
    year: int, month: int, day: int, city: str = "Babylon", ziggurat: float = 0.0
) -> tuple[float, float, float, float, float, float]:
    """
    Calculates the precise Moonrise, transit, and Moonset for a Mesopotamian site.

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: ut_rise, ut_transit, ut_set, local_rise, local_transit, local_set
    :rtype: tuple[float, float, float, float, float, float]
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    lon_hours = lon / 15.0
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    dip = get_horizon_dip(alt)

    ut_rise = calculate_moon_event(year, month, day, lat, lon, dip, is_setting=False)
    ut_transit = calculate_moon_transit(year, month, day, lon)
    ut_set = calculate_moon_event(year, month, day, lat, lon, dip, is_setting=True)

    local_rise = (ut_rise + lon_hours) % 24 if not math.isnan(ut_rise) else float("nan")
    local_transit = (ut_transit + lon_hours) % 24
    local_set = (ut_set + lon_hours) % 24 if not math.isnan(ut_set) else float("nan")

    return ut_rise, ut_transit, ut_set, local_rise, local_transit, local_set


def get_lunar_info(epoch_obj: Epoch) -> tuple[float, float]:
    """
    Returns precise lunar age and illumination percentage.

    :param epoch_obj: pymeeus Epoch object.
    :type epoch_obj: Epoch
    :return: Tuple with lunar age (days) and illumination fraction (0-100)
    :rtype: tuple[float, float]
    """
    target_jde = epoch_obj.jde()
    search_date = epoch_obj - 2.0

    last_new_moon = Moon.moon_phase(search_date, target="new")

    while last_new_moon.jde() > target_jde:
        search_date -= 15.0
        last_new_moon = Moon.moon_phase(search_date, target="new")

    age = target_jde - last_new_moon.jde()
    if age > 30.0:
        search_retry = last_new_moon + 15.0
        last_new_moon = Moon.moon_phase(search_retry, target="new")
        age = target_jde - last_new_moon.jde()

    illum = float(Moon.illuminated_fraction_disk(epoch_obj) * 100.0)
    return float(age), illum


def lunar_info(jd: float) -> tuple[float, float]:
    """
    Wrapper around get_lunar_info accepting an absolute Julian Date.

    :param jd: Julian Date
    :type jd: float
    :return: tuple with lunar age and illumination.
    :rtype: tuple[float, float]
    """
    epoch_obj = Epoch(jd, utc=True)
    return get_lunar_info(epoch_obj)


def check_neomenia(
    year: int,
    month: int,
    day: int,
    city: str = "Babylon",
    ziggurat: float = 0.0,
    AoV: float = 12.0,
    uncertainty: float = 0.833,
    verbose: bool = True,
) -> tuple[float, float]:
    """
    Evaluate visibility criteria for the first lunar crescent after New Moon (na interval).

    Calculates the 'na' interval (Sunset to Moonset) and the lunar altitude
    at the moment of sunset. The standard Babylonian criterion for
    visibility is an 'na' interval > 12 US (48 minutes).

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Elevation in meters, defaults to 0.0
    :type ziggurat: float, optional
    :param AoV: Angle of Viewing in degrees, defaults to 12.0
    :type AoV: float, optional
    :param uncertainty: Uncertainty or marginal visibility factor, defaults to 0.833
    :type uncertainty: float, optional
    :param verbose: If True, prints analysis to console, defaults to True
    :type verbose: bool, optional
    :return: Tuple (na_interval_min, lunar_altitude_at_sunset)
    :rtype: tuple[float, float]
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat

    # Clear fix: avoid passing absolute adjusted altitude to a relative ziggurat parameter
    _, _, sun_set_ut, _, _, _ = sun_rise_transit_set(year, month, day, city=city, ziggurat=ziggurat)

    h = int(sun_set_ut)
    m = int((sun_set_ut - h) * 60)
    s = ((sun_set_ut - h) * 60 - m) * 60
    e_sunset = Epoch(year, month, day, h, m, s, utc=True)

    ra_l, dec_l, _, _ = Moon.apparent_equatorial_pos(e_sunset)

    st_local = (_historical_gmst_degrees(e_sunset) + lon) % 360.0
    ha_l = (st_local - ra_l._deg) % 360.0

    phi_rad = math.radians(lat)
    dec_rad = math.radians(dec_l._deg)
    ha_rad = math.radians(ha_l)

    sin_alt = math.sin(phi_rad) * math.sin(dec_rad) + math.cos(phi_rad) * math.cos(
        dec_rad
    ) * math.cos(ha_rad)
    alt_lunar = math.degrees(math.asin(sin_alt))

    moon_set_ut = calculate_moon_event(
        year, month, day, lat, lon, get_horizon_dip(alt), is_setting=True
    )
    na_interval_min = (moon_set_ut - sun_set_ut) * 60.0
    limit_visible = 4.0 * AoV
    limit_doubtful = limit_visible * uncertainty

    if verbose:
        print(f"\n--- Neomenia Check: {city} {year}/{month}/{day} ---")
        print(f"  Sun Set (UT):   {sun_set_ut:.4f}")
        print(f"  Moon Alt at SS: {alt_lunar:.2f}°")
        print(
            f"  NA Interval:     {na_interval_min:.2f} min ({(na_interval_min / 4.0):.2f} ush)"
        )

        if na_interval_min > limit_visible:
            print("  Result: VISIBLE (New month starts tonight)")
        elif na_interval_min > limit_doubtful:
            print("  Result: DOUBTFUL (Possible visibility)")
        else:
            print("  Result: NOT VISIBLE (Month has 30 days)")

    return na_interval_min, alt_lunar


def calculate_mi_mush(
    year: int, month: int, day: int, city: str = "Babylon", ziggurat: float = 0.0
) -> tuple[float, float, float]:
    """
    Calculates the 'Mi-Mush' (ME) interval: The time between Moonset and Sunrise
    around the day of the Full Moon.

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: Tuple containing (mi_mush_interval_min, moon_set_ut, sun_rise_ut)
    :rtype: tuple[float, float, float]
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    dip = get_horizon_dip(alt)

    sun_rise_ut, _, _, _, _, _ = sun_rise_transit_set(year, month, day, city, ziggurat)

    moon_set_ut = calculate_moon_event(
        year, month, day, lat, lon, dip, is_setting=True, seed_ut=sun_rise_ut - 4.0
    )

    mi_mush_min = (moon_set_ut - sun_rise_ut) * 60.0
    return mi_mush_min, moon_set_ut, sun_rise_ut


def calculate_kur(
    year: int, month: int, day: int, city: str = "Babylon", ziggurat: float = 0.0
) -> tuple[float, float, float]:
    """
    Calculates the 'KUR' interval: Time between Moonrise and Sunrise
    on the last days of the lunar month.

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: Tuple containing (kur_interval_min, moon_rise_ut, sun_rise_ut)
    :rtype: tuple[float, float, float]
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    dip = get_horizon_dip(alt)

    sun_rise_ut, _, _, _, _, _ = sun_rise_transit_set(year, month, day, city, ziggurat)
    moon_rise_ut = calculate_moon_event(
        year, month, day, lat, lon, dip, is_setting=False
    )

    kur_interval_min = (sun_rise_ut - moon_rise_ut) * 60.0
    return kur_interval_min, moon_rise_ut, sun_rise_ut


def calculate_shu_interval(
    year: int, month: int, day: int, city: str = "Babylon", ziggurat: float = 0.0
) -> float:
    """
    Calculate the SU (Shu) interval: Time from the Solar Sunset to the
    Lunar Sunset on the days near the full moon.

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: SU = Moonset - Sunset in minutes
    :rtype: float
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    dip = get_horizon_dip(alt)

    _, _, sun_set_ut, _, _, _ = sun_rise_transit_set(year, month, day, city, ziggurat)

    moon_set_ut = calculate_moon_event(
        year, month, day, lat, lon, dip, is_setting=True, seed_ut=sun_set_ut
    )

    return (moon_set_ut - sun_set_ut) * 60.0


def calculate_full_moon_na(
    year: int, month: int, day: int, city: str = "Babylon", ziggurat: float = 0.0
) -> float:
    """
    Calculate the NA interval of the full moon: Time from the Lunar Rising to the Solar Setting.

    :param year: Year
    :type year: int
    :param month: Month
    :type month: int
    :param day: Day
    :type day: int
    :param city: City name, defaults to "Babylon"
    :type city: str, optional
    :param ziggurat: Height above terrain in meters, defaults to 0.0
    :type ziggurat: float, optional
    :return: NA (Full Moon) = Sunset - Moonrise in minutes
    :rtype: float
    """
    lat = float(mesopotamian_cities[city]["latitude"])
    lon = float(mesopotamian_cities[city]["longitude"])
    alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
    dip = get_horizon_dip(alt)

    _, _, sun_set_ut, _, _, _ = sun_rise_transit_set(year, month, day, city, ziggurat)
    moon_rise_ut = calculate_moon_event(
        year, month, day, lat, lon, dip, is_setting=False
    )

    return (sun_set_ut - moon_rise_ut) * 60.0