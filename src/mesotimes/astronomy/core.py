"""
**`astronomy/core.py`** - Core astronomical corrections, constants, and geodetic data.

This module provides low-level tools, algorithms (Horner's method), historical
time corrections (Delta T), and geodetic properties for ancient Mesopotamian sites.
"""

import math
from typing import Final
from pymeeus.Epoch import Epoch
from pymeeus.Angle import Angle
from pymeeus import Coordinates
from pymeeus.Moon import Moon
from pymeeus.Sun import Sun


# Strict type hinting for the geographic metadata structure
mesopotamian_cities: Final[dict[str, dict[str, str | float | int]]] = {
    "Babylon": {
        "description": "Main center of the astronomical diaries (Esagila).",
        "latitude": 32.5430,
        "longitude": 44.4244,
        "altitude": 26,
        "modern_name": "Al Hillah, Iraq",
    },
    "Uruk": {
        "description": "Important center of observation and late mathematical/astronomical texts.",
        "latitude": 31.3222,
        "longitude": 45.6361,
        "altitude": 21,
        "modern_name": "Warka, Iraq",
    },
    "Nineveh": {
        "description": "Seat of the library of Ashurbanipal, rich in texts of celestial omens (Enuma Anu Enlil).",
        "latitude": 36.3583,
        "longitude": 43.1517,
        "altitude": 223,
        "modern_name": "Mosul, Iraq",
    },
    "Ur": {
        "description": "Key Sumerian city with an astronomically aligned ziggurat.",
        "latitude": 30.9625,
        "longitude": 46.1031,
        "altitude": 5,
        "modern_name": "Tell el-Muqayyar, Iraq",
    },
    "Nippur": {
        "description": "Religious center and lunar calendar calibration center.",
        "latitude": 32.1264,
        "longitude": 45.2319,
        "altitude": 25,
        "modern_name": "Afak, Iraq",
    },
    "Sippar": {
        "description": "City of the sun god (Utu/Shamash), relevant for solstice calculations.",
        "latitude": 33.0594,
        "longitude": 44.2525,
        "altitude": 32,
        "modern_name": "Tell Abu Habbah, Iraq",
    },
    "Assur": {
        "description": "Assyrian religious capital with early observations.",
        "latitude": 35.4567,
        "longitude": 43.2625,
        "altitude": 165,
        "modern_name": "Qal'at Sherqat, Iraq",
    },
    "Kish": {
        "description": "A site of great antiquity, mentioned in royal lists and eclipse records.",
        "latitude": 32.5453,
        "longitude": 44.6033,
        "altitude": 29,
        "modern_name": "Tell al-Uhaymir, Iraq",
    },
    "Borsippa": {
        "description": "Sister city of Babylon with an important ziggurat (associated with Nabu).",
        "latitude": 32.3917,
        "longitude": 44.3417,
        "altitude": 30,
        "modern_name": "Birs Nimrud, Iraq",
    },
    "Susa": {
        "description": "Capital of Elam; seat of administrative and astronomical archives shared with Mesopotamia.",
        "latitude": 32.1892,
        "longitude": 48.2436,
        "altitude": 78,
        "modern_name": "Shush, Iran",
    },
    "Harran": {
        "description": "Main center of worship of the god Sin (the Moon). Fundamental for lunar observations in the north.",
        "latitude": 36.8625,
        "longitude": 39.0250,
        "altitude": 377,
        "modern_name": "Harran, Turkey",
    },
    "Eridu": {
        "description": "Considered the oldest city; relevant to the cosmogony associated with the sea horizon.",
        "latitude": 30.8158,
        "longitude": 45.9961,
        "altitude": 6,
        "modern_name": "Tell Abu Shahrein, Iraq",
    },
    "Larsa": {
        "description": "Ancient solar center relevant for astronomical observations.",
        "latitude": 31.2858,
        "longitude": 45.8533,
        "altitude": 20,
        "modern_name": "Tell as-Senkereh, Iraq",
    },
    "Sevilla": {
        "description": "Non-Mesopotamian test node (internal verification).",
        "latitude": 37.40855,
        "longitude": -5.92328,
        "altitude": 20,
        "modern_name": "Seville, Spain",
    },
}

# User can add cities, for instance:
#
#   mesopotamian_cities["Ebla"] = {
#      "description": "Important ancient city in Syria.",
#       "latitude": 35.7986,
#       "longitude": 36.7889,
#       "altitude": 390,
#       "modern_name": "Tell Mardikh, Syria",
#   }

def _horner(x: float, a: list[float]) -> float:
    """
    Evaluates a polynomial using Horner's method.

    :param x: Independent variable
    :type x: float
    :param a: List of coefficients ordered from lowest to highest degree
    :type a: list[float]
    :return: Polynomial evaluation value
    :rtype: float
    """
    result = 0.0
    for i in range(len(a) - 1, -1, -1):
        result = a[i] + (x * result)
    return result


def jde2date(jd: float) -> tuple[int, int, int]:
    """
    Converts a Julian Date (JD/JDE) to a calendar date tuple (Year, Month, Day).

    :param jd: Julian Day Number
    :type jd: float
    :return: Year, month, day calendar units
    :rtype: tuple[int, int, int]
    """
    y, m, d = Epoch(jd, utc=True).get_date()
    return y, m, d


def _historical_gmst_degrees(epoch: Epoch) -> float:
    """
    Calculates Greenwich Mean Sidereal Time (GMST) in degrees from an Epoch.
    Bypasses library limitations for ancient negative years.
    Reference: Meeus, Astronomical Algorithms, Chapter 12.

    :param epoch: pymeeus.Epoch object
    :type epoch: Epoch
    :return: GMST in decimal degrees [0.0, 360.0)
    :rtype: float
    """
    jde = epoch.jde()
    t = (jde - 2451545.0) / 36525.0
    gmst = (
        280.46061837
        + 360.98564736629 * (jde - 2451545.0)
        + 0.000387933 * (t * t)
        - (t * t * t / 38710000.0)
    )
    return gmst % 360.0


def get_horizon_dip(altitude_m: float) -> float:
    """
    Calculates the geometric dip of the horizon based on observer elevation.

    :param altitude_m: Height above local terrain in meters
    :type altitude_m: float
    :return: Horizon dip in decimal degrees
    :rtype: float
    """
    if altitude_m <= 0.0:
        return 0.0
    return 0.0347 * math.sqrt(altitude_m)


def delta_t(year: int, month: int = 7) -> float:
    """
    Calculates Delta T (ΔT), the difference between Terrestrial Time (TT)
    and Universal Time (UT) in seconds.

    Uses the polynomial fits by Espenak and Meeus (NASA) to account for
    the deceleration of Earth's rotation.

    :param year: Astronomical year (-1999 to 3000)
    :type year: int
    :param month: Month, defaults to 7 (mid-year pivot)
    :type month: int, optional
    :raises ValueError: If year is outside the [-1999, 3000] range
    :return: Delta T in seconds
    :rtype: float
    """
    y = year + (month - 0.5) / 12

    if y < -1999 or y >= 3000:
        raise ValueError("The year must be between -1999 and 3000")

    if y < -500:
        u = (y - 1820) / 100.0
        dt0 = 20 + 32 * (u * u)

    elif y < 500:
        u = y / 100.0
        coeffs = [
            10583.6,
            -1014.41,
            33.78311,
            -5.952053,
            -0.1798452,
            0.022174192,
            0.0090316521,
        ]
        dt0 = _horner(u, coeffs)

    elif y < 1600:
        u = (y - 1000) / 100.0
        coeffs = [
            1574.2,
            -556.01,
            71.23472,
            0.319781,
            -0.8503463,
            -0.005050998,
            0.0083572073,
        ]
        dt0 = _horner(u, coeffs)

    elif y < 1700:
        t = y - 1600
        coeffs = [120, -0.9808, -0.01532, 1.0 / 7129.0]
        dt0 = _horner(t, coeffs)

    elif y < 1800:
        t = y - 1700
        coeffs = [8.83, 0.1603, -0.0059285, 0.00013336, -1.0 / 1174000.0]
        dt0 = _horner(t, coeffs)

    elif y < 1860:
        t = y - 1800
        coeffs = [
            13.72,
            -0.332447,
            0.0068612,
            0.0041116,
            -0.00037436,
            0.0000121272,
            -0.0000001699,
            0.000000000875,
        ]
        dt0 = _horner(t, coeffs)

    elif y < 1900:
        t = y - 1860
        coeffs = [7.62, 0.5737, -0.251754, 0.01680668, -0.0004473624, 1.0 / 233174.0]
        dt0 = _horner(t, coeffs)

    elif y < 1920:
        t = y - 1900
        coeffs = [-2.79, 1.494119, -0.0598939, 0.0061966, -0.000197]
        dt0 = _horner(t, coeffs)

    elif y < 1941:
        t = y - 1920
        coeffs = [21.20, 0.84493, -0.076100, 0.0020936]
        dt0 = _horner(t, coeffs)

    elif y < 1961:
        t = y - 1950
        coeffs = [29.07, 0.407, -1.0 / 233.0, 1.0 / 2547.0]
        dt0 = _horner(t, coeffs)

    elif y < 1986:
        t = y - 1975
        coeffs = [45.45, 1.067, -1.0 / 260.0, -1.0 / 718.0]
        dt0 = _horner(t, coeffs)

    elif y < 2005:
        t = y - 2000
        coeffs = [63.86, 0.3345, -0.060374, 0.0017275, 0.000651814, 0.00002373599]
        dt0 = _horner(t, coeffs)

    elif y < 2050:
        t = y - 2000
        coeffs = [62.92, 0.32217, 0.005589]
        dt0 = _horner(t, coeffs)

    elif y < 2150:
        u = (y - 1820) / 100.0
        dt0 = -20 + 32 * (u * u) - 0.5628 * (2150 - y)

    else:
        u = (y - 1820) / 100.0
        dt0 = -20 + 32 * (u * u)

    drift = 0.000012932 * (y - 1955) * (y - 1955)
    return float(round(dt0 - drift))


def delta_t_sigma(year: int, month: int = 7) -> float:
    """
    Calculates Delta T (ΔT) Uncertainty in seconds based on Espenak & Meeus (NASA).
    Covers the full historical range from ancient eras to future projections.

    :param year: Astronomical year (-1999 to 3000)
    :type year: int
    :param month: Month, defaults to 7
    :type month: int, optional
    :return: Delta T (ΔT) Uncertainty estimates in seconds
    :rtype: float
    """
    y = year + (month - 0.5) / 12

    def dts_huber(y_val: float, y_ref: float) -> float:
        """Huber's derived long-term uncertainty estimation."""
        q = 0.058
        n = abs(y_val - y_ref)
        m = 2500
        return 365.25 * n * math.sqrt((n * q / 3.0) * (1 + n / m)) / 1000.0

    if y < -1000:
        return float(round(dts_huber(y, -500)))

    elif -1000 <= y <= 1200:
        t = (y - 1820) / 100.0
        return float(round(0.8 * t * t))

    elif 1200 < y <= 1600:
        t = (y - 1600) / 100.0
        return float(round(0.36 * t * t))

    elif 1600 < y <= 1900:
        t = (y - 1820) / 100.0
        return float(round(0.005 * t * t))

    elif 1900 < y <= 2005:
        if y > 1955:
            return 0.0
        return float(round(0.0001 * (y - 1955) ** 2))

    else:
        return float(round(dts_huber(y, 2005)))

def epsilon(year: int|float)-> float:
    """
    Calculates the historical obliquity in decimal degrees. From Laskar (1986),
    Bibcode:1986A&A...157...59L

    :param year: Year
    :type year: int|float
    :return: Obliquity in decimal degrees
    :rtype: float
    """    
    # Polynomial coefficients in arcseconds:
    coef = [84381.448, -4680.93, -1.55, 1999.25, -51.38, -249.67,  -39.05, 7.12, 27.87, 5.79, 2.45]

    t= (year-2000.0)/10000.
    return _horner(t, coef)/3600.0

def equatorial_to_horizontal_at_instant(
    jd_ut: float, ra_hours: float, dec_deg: Angle, city_lon: float, city_lat: float
) -> tuple[Angle, Angle]:
    """Calculates geometric horizontal coordinates.

    :param jd_ut: Julian Day (UT)
    :type jd_ut: float
    :param ra_hours: Right Ascension in decimal hours
    :type ra_hours: float
    :param dec_deg: Declination in degrees
    :type dec_deg: Angle
    :param city_lon: Geografic longitude of the city in degrees (East is positive)
    :type city_lon: float
    :param city_lat: Geografic latitude of the city in degrees (North is positive)
    :type city_lat: float
    :return: Tuple elevation, azimut
    :rtype: tuple[Angle, Angle]
    """
    lon_ast = -city_lon
    lat = Angle(city_lat)

    # The start of the UT civil day (00:00h) is always the Julian Day with decimal .5
    # We subtract 0.5, round down with floor, and add 0.5.
    # This works mathematically for any decimal without the need for IFs.
    jd_midnight = math.floor(jd_ut - 0.5) + 0.5
    epoch_midnight = Epoch(jd_midnight)

    true_obliquity = Coordinates.true_obliquity(epoch_midnight)
    nutation_longitude = Coordinates.nutation_longitude(epoch_midnight)

    gast_midnight = (
        epoch_midnight.apparent_sidereal_time(true_obliquity, nutation_longitude) * 24.0
    )

    # The actual hours elapsed since midnight (always between 0.0 and 24.0)
    hours_since_midnight = (jd_ut - jd_midnight) * 24.0
    gast_instant = (gast_midnight + (hours_since_midnight * 1.00273790935)) % 24.0

    # Local Sidereal Time
    lst_hours = (gast_instant - (lon_ast / 15.0)) % 24.0

    # Hour Angle (H = LST - RA)
    h_hours = lst_hours - ra_hours
    h = Angle(h_hours * 15.0)

    # Transformation to Horizontals
    azi, ele = Coordinates.equatorial2horizontal(h, dec_deg, lat)

    return azi, ele


def get_body_equatorial_at_midnight(jd_ut: float, body_id: str, city: str = "Babylon")->tuple[Angle, Angle]:
    """Computes fixed equatorial positions using the safe math.floor approach.

    :param jd_ut: Julian Day (UT)
    :type jd_ut: float
    :param body_id: Body name
    :type body_id: str
    :param city: Observatory city name, defaults to "Babylon"
    :type city: str, optional
    :return: Right Ascension and Declination 
    :rtype: tuple[Angle, Angle]
    """    
    jd_midnight = math.floor(jd_ut - 0.5) + 0.5

    epoch_base = Epoch(jd_midnight)
    y, m, d = epoch_base.get_date()

    dt_days = delta_t(y, m) / 86400.0
    epoch_tt = Epoch(y, m, d + dt_days)

    if body_id == "sun":
        ra, dec, _ = Sun.apparent_rightascension_declination_coarse(epoch_tt)
        return ra / 15.0, dec 
    elif body_id == "moon":
        ra, dec, _, _ = Moon.apparent_equatorial_pos(epoch_tt)
        return ra / 15.0, dec
    else:
        ra, dec, _ = body_id.get_geocentric_position(epoch_tt)
        return ra / 15.0, dec
