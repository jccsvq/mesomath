"""
mesotimes.astronomy.visibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Atmospheric visibility and twilight models for ancient astronomical phenomena.
Includes extinction, refraction, horizon dip, and sky brightness scattering.
"""

import math
from typing import Callable, Tuple, Iterable

import pymeeus.Coordinates as Coordinates
from pymeeus.Angle import Angle
from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun

from mesotimes.astronomy.core import (
    get_horizon_dip,
    resolve_city_coordinates,
)
from mesotimes.astronomy.stars import BabStar

# --- 1. Atmospheric Physics ---


def get_sun_eq(epoch: Epoch) -> tuple[Angle, Angle]:
    """Calculates Sun's right ascension and declination for the epoch.

    Args:
        epoch (Epoch): Epoch object.

    Returns:
        tuple[Angle, Angle]: Tuple containing Sun's right ascension and declination (EoD).
    """
    # 1. Sun ecliptical coordinates (VSOP87)

    sun_lon, sun_lat, _ = Sun.geometric_geocentric_position(epoch, tofk5=False)

    # 2. True obliquity
    true_obliquity = Coordinates.true_obliquity(epoch)

    # 3. Transformation from Ecliptic to Equatorial
    sun_alpha, sun_delta = Coordinates.ecliptical2equatorial(
        sun_lon, sun_lat, true_obliquity
    )

    return sun_alpha, sun_delta


def get_sun_star_data(epoch: Epoch, star: BabStar) -> dict:
    """Gathers relevant data for star visibility calculation in a dictionary.

    The returned dictionary contains the following keys:
        - "Epoch": The input PyMeeus Epoch object.
        - "GAST": Greenwich Apparent Sidereal Time scaled to standard hours [0, 24).
        - "Star": Star name as a string.
        - "Sun_ra": Sun's right ascension (EoD).
        - "Sun_dec": Sun's declination (EoD).
        - "Star_ra": Star's right ascension (EoD).
        - "Star_dec": Star's declination (EoD).
        - "Sun_Star_angle": Angular separation between the Sun and the Star.

    Args:
        epoch (Epoch): Epoch object.
        star (BabStar): Star object.

    Returns:
        dict: Data dictionary containing astronomical coordinates and times.
    """
    data_dict = {}
    # Star equatorial coordinates
    star_alpha, star_delta, _ = star.get_geocentric_position(epoch)
    # Sun equatorial coordinates
    sun_alpha, sun_delta = get_sun_eq(epoch)
    # Sun-Star angle
    sun_star_angle = Coordinates.angular_separation(
        sun_alpha, sun_delta, star_alpha, star_delta
    )
    # Sidereal Time
    true_obliquity = Coordinates.true_obliquity(epoch)
    nutation_longitude = Coordinates.nutation_longitude(epoch)
    # CRITICAL: PyMeeus returns sidereal time in decimal fractions of a day [0, 1).
    # We multiply by 24.0 to scale it into standard astronomical hours.
    gast_hours = epoch.apparent_sidereal_time(true_obliquity, nutation_longitude) * 24.0

    data_dict["Epoch"] = epoch
    data_dict["GAST"] = gast_hours
    data_dict["Star"] = star.name
    data_dict["Sun_ra"] = sun_alpha
    data_dict["Sun_dec"] = sun_delta
    data_dict["Star_ra"] = star_alpha
    data_dict["Star_dec"] = star_delta
    data_dict["Sun_Star_angle"] = sun_star_angle

    return data_dict


def get_azimut_elevation(
    h: Angle, dec: Angle, lat: Angle, horizon_correction: Angle
) -> Tuple[Angle, Angle]:
    """Transform hour angle coordinates to alt-azimuth coordinates.

    Args:
        h (Angle): Hour angle.
        dec (Angle): Declination.
        lat (Angle): Latitude of the observer.
        horizon_correction (Angle): Horizon sinking due to the height of the observer.

    Returns:
        Tuple[Angle, Angle]: Azimuth and elevation.
    """
    azi, ele = Coordinates.equatorial2horizontal(h, dec, lat)
    ele = refraction_true_to_apparent(ele)
    ele += horizon_correction
    azi = Angle((azi() + 180.0) % 360.0)
    return azi, ele


def air_mass_pickering(
    altitude: Angle, k: float = 0.10, m0: float = -1.46
) -> tuple[float, float, float]:
    """Air mass and extinction calculated using Pickering (2002) approximation.
    Safeguarded against negative altitudes below the horizon.

    Args:
        altitude (Angle): Object altitude over horizon.
        k (float, optional): Extinction coefficient. Defaults to 0.10.
        m0 (float, optional): Magnitude out of atmosphere. Defaults to -1.46 (Sirius).

    Returns:
        tuple[float, float, float]: Air mass, extinction, and magnitude at ground level.
    """
    # If the object is below the horizon, we limit it to 0 to avoid complex errors
    h = max(0.0, altitude())

    x = 1 / (math.sin((math.pi / 180.0) * (h + 224.0 / (165.0 + 47.0 * h**1.1))))
    return x, x * k, m0 + x * k


def air_mass_KY(
    altitude: Angle, k: float = 0.10, m0: float = -1.46
) -> tuple[float, float, float]:
    """Air mass and extinction calculated using Kasten & Young (1989) approximation.
    Safeguarded against deep zenith angles.

    Args:
        altitude (Angle): Object altitude over horizon.
        k (float, optional): Extinction coefficient. Defaults to 0.10.
        m0 (float, optional): Magnitude out of atmosphere. Defaults to -1.46 (Sirius).

    Returns:
        tuple[float, float, float]: Air mass, extinction, and magnitude at ground level.
    """
    h = max(0.0, altitude())
    # Zenith distance.
    z = 90.0 - h
    zr = math.pi * z / 180

    x = math.cos(zr) + 0.50572 * (96.07995 - z) ** -1.6364
    x = 1 / x
    return x, x * k, m0 + x * k


def refraction_true_to_apparent(true_altitude: Angle) -> Angle:
    """Calculates the apparent altitude of an object over the horizon by
    adding atmospheric refraction using Sæmundsson's (1986) formula for TRUE altitude.

    Valid for standard atmospheric conditions (1010 mb, 10°C).

    Args:
        true_altitude (Angle): The geometric/true altitude of the object.

    Returns:
        Angle: The apparent (visually observed) altitude.
    """
    h = true_altitude()

    if h < -2.0:
        return Angle(h)

    # Specific constants for true altitude (7.31 and 4.4)
    argument_degrees = h + (7.31 / (h + 4.4))
    denominator = math.tan(math.radians(argument_degrees))
    r_arcminutes = 1.0 / denominator

    r_degrees = r_arcminutes / 60.0

    return Angle(h + r_degrees)


# --- 2. Phase Functions for Scattering ---


def _sky_scattering_phase(phi_deg: float) -> float:
    """Calculates the Rayleigh + Mie phase function value for a given separation angle.

    Args:
        phi_deg (float): Separation angle in degrees.

    Returns:
        float: Value of the Rayleigh + Mie phase function.
    """
    phi_rad = math.radians(phi_deg)
    return (1.0 + math.cos(phi_rad) ** 2) + 3.0 * math.exp(-phi_deg / 10.0)


# --- 3. Visibility Core Engines ---


def is_star_visible_crepuscular(
    v_mag: float,
    star_altitude: Angle,
    sun_altitude: Angle,
    sun_star_angle: Angle | None = None,
    air_mass_func: Callable[
        [Angle, float], Tuple[float, float, float]
    ] = air_mass_pickering,
    k: float = 0.20,
) -> tuple[bool, float, float]:
    """Evaluates if a star is visible to the naked eye under twilight conditions.

    Supports both a standard zenith-based ramp model and a 3D scattering model
    if `sun_star_angle` is provided.

    Args:
        v_mag (float): Visual apparent magnitude of the star (outside atmosphere).
        star_altitude (Angle): Star apparent altitude over horizon.
        sun_altitude (Angle): Sun apparent altitude over horizon.
        sun_star_angle (Angle | None, optional): Sun-Star angle. Defaults to None.
        air_mass_func (Callable[[Angle, float], tuple[float, float, float]], optional):
            Air-mass function to use. Defaults to air_mass_pickering.
        k (float, optional): Extinction coefficient. Defaults to 0.20.

    Returns:
        tuple[bool, float, float]: A tuple containing:
            - bool: True if the star is visible to the naked eye, False otherwise.
            - float: Real apparent magnitude of the star under the atmosphere (m_real).
            - float: Maximum magnitude perceivable under current twilight conditions (m_lim).
    """
    h_sun = sun_altitude()

    # True extinction of the star (independent of the sky model)
    _, _, m_real = air_mass_func(star_altitude, k)

    if h_sun >= 0:
        return False, m_real, -99.0  # Daylight

    # Base sky brightness ramp at zenith (mag/arcsec2)
    if h_sun <= -18.0:
        m_sky = 22.0
    else:
        m_sky = 3.0 + (h_sun / -18.0) * (22.0 - 3.0)

    # Apply 3D scattering correction if geometry is provided
    if sun_star_angle is not None:
        phase_val = _sky_scattering_phase(sun_star_angle())
        m_sky -= 2.5 * math.log10(phase_val)

    # Eye limit magnitude (Schaefer / Blackwell with calibrated pivot at 14.5)
    m_lim = 6.0 - 2.5 * math.log10(1.0 + 10 ** (0.4 * (14.5 - m_sky)))

    return m_real <= m_lim, m_real, m_lim


def scan_twilight_visibility(
    year: int,
    star: BabStar,
    phenomena: str = "heliacal",
    city: str = "Babylon",
    ziggurat: float = 0.0,
    minutes: int = 6,
    ramp_model: bool = False,
    air_mass_func: Callable[
        [Angle, float], Tuple[float, float, float]
    ] = air_mass_pickering,
    k: float = 0.20,
    day_offset: int = 0,
    verbose: bool = True,
) -> None:
    """Scans and profiles a star's twilight visibility contrast during an event.

    Calculates the exact epoch of a given astronomical phenomenon, applies a
    day offset if requested, and runs a time-series simulation backwards
    to evaluate the atmospheric extinction and visual contrast of the star
    against the twilight sky brightness.

    Args:
        year (int): Historical BCE/CE year to evaluate (e.g., -378).
        star (BabStar): The star object containing catalog positions and magnitudes.
        phenomena (str, optional): Type of phenomenon to seek. Defaults to "heliacal".
        city (str, optional): Target archaeological site or city. Defaults to "Babylon".
        ziggurat (float, optional): Elevation override in meters to simulate observations
            from high platforms. Defaults to 0.0.
        minutes (int, optional): Step interval in sidereal minutes for the time loop. Defaults to 6.
        ramp_model (bool, optional): Use standard zenith-based ramp model instead of a 3D 
            scattering model if True. Defaults to False.
        air_mass_func (Callable[[Angle, float], tuple[float, float, float]], optional):
            Air-mass function to use. Defaults to air_mass_pickering.
        k (float, optional): Atmospheric extinction coefficient. Defaults to 0.20.
        day_offset (int, optional): Shifts the evaluation date backward by N days relative
            to the base event date. Defaults to 0.
        verbose (bool, optional): Makes star.search_phenomena verbose if True. Defaults to True.

    Raises:
        ValueError: If the star object lacks valid V photometric magnitude data.
    """
    # Star magnitude
    vmag = star.V
    # If star object is created from the catalog it has self.V and self.B_V
    # but, did the user include them in his/her custom star?
    if vmag is None:
        raise ValueError("Star has no valid magnitude.")

    # Search the epoch of phenomenon
    base_epoch = star.search_phenomena(
        year, phenomena, city, ziggurat, with_return=True, verbose=verbose
    )
    epoch = base_epoch - float(day_offset)

    # Get basic data
    d = get_sun_star_data(epoch, star)

    # 1. Geographic parameters and horizon dip correction
    lat = Angle(resolve_city_coordinates(city)["latitude"])
    lon = Angle(resolve_city_coordinates(city)["longitude"])
    alt = float(resolve_city_coordinates(city)["altitude"]) + ziggurat
    horizon_correction = get_horizon_dip(alt)

    # Sidereal Time
    last = 15.0 * d["GAST"] + lon
    lst = Angle(last() % 360.0)

    year, month, day = d["Epoch"].get_date()
    s = f" {year:04d}-{month:02d}-{round(day, 0)}"
    print(f"Scanning {star.name} visibility in {city} ({s})")
    direction = "forward" if phenomena == "acronychal" else "backward"
    print(f"at {minutes} sidereal minutes interval ({direction})")
    print(f"Day Offset: {day_offset}")
    print(f"Current Extinction Coefficient value: {k = }")
    print("|sun_ele |star_ele |     phi |Vis. |m_real | m_lim | Contrast")
    print("|--------|---------|---------|-----|-------|-------|---------------------")

    for delta_lst in range(0, 60, minutes):
        if phenomena == "heliacal":
            sun_h = lst - d["Sun_ra"] - Angle(delta_lst) / 4.0
            star_h = lst - d["Star_ra"] - Angle(delta_lst) / 4.0
        elif phenomena == "acronychal":
            sun_h = lst - d["Sun_ra"] + Angle(delta_lst) / 4.0
            star_h = lst - d["Star_ra"] + Angle(delta_lst) / 4.0
        sun_dec = d["Sun_dec"]
        star_dec = d["Star_dec"]

        sun_azi, sun_ele = get_azimut_elevation(sun_h, sun_dec, lat, horizon_correction)
        star_azi, star_ele = get_azimut_elevation(
            star_h, star_dec, lat, horizon_correction
        )
        sun_star_angle = Coordinates.angular_separation(
            sun_azi, sun_ele, star_azi, star_ele
        )

        # Star must be over horizon
        if star_ele < 0.0:
            break

        if sun_ele < 0.0:
            visible, m_real, m_lim = is_star_visible_crepuscular(
                vmag,
                star_ele,
                sun_ele,
                sun_star_angle if not ramp_model else None,
                air_mass_func=air_mass_func,
                k=k,
            )

            # We calculate the visual indicator based on the contrast margin
            vis = "No"
            bar = ""
            if visible:
                vis = "Yes"
                contrast_delta = m_lim - m_real
                num_chars = min(int(contrast_delta * 8), 20)
                bar = "#" * max(1, num_chars)

            # Formatted print (Fixed total base width: ~55 characters)
            print(
                f"|{sun_ele():7.3f} | {star_ele():7.3f} | {sun_star_angle():7.3f} | "
                f"{vis:3s} | {m_real:5.2f} | {m_lim:5.2f} | {bar}"
            )
    print("-" * 73)



def profile_visibility_sequence(
    year: int,
    star: BabStar,
    phenomena: str = "heliacal",
    city: str = "Babylon",
    ziggurat: float = 0.0,
    minutes: int = 6,
    ramp_model: bool = False,
    air_mass_func: Callable[
        [Angle, float], Tuple[float, float, float]
    ] = air_mass_pickering,
    k: float = 0.20,
    day_offset: Iterable[int] = (0, 1, 2, 3, 4),
    verbose: bool = True,
) -> None:
    """Executes a multi-day twilight visibility scan sequence for a star.

    Acts as a wrapper over `scan_twilight_visibility`. It iterates over a collection
    of day offsets relative to a base astronomical event epoch, printing consecutive
    time-series reports. To avoid terminal noise, it automatically silences the
    underlying geometric finder data (`verbose=False`) for all iterations except 
    the first day of the sequence.

    Args:
        year (int): Historical BCE/CE year to evaluate (e.g., -378).
        star (BabStar): The star object containing catalog positions and magnitudes.
        phenomena (str, optional): Type of phenomenon to seek. Defaults to "heliacal".
        city (str, optional): Target archaeological site or city. Defaults to "Babylon".
        ziggurat (float, optional): Elevation override in meters to simulate observations
            from high platforms. Defaults to 0.0.
        minutes (int, optional): Step interval in sidereal minutes for the time loop. Defaults to 6.
        ramp_model (bool, optional): Use standard zenith-based ramp model instead of a 3D 
            scattering model if True. Defaults to False.
        air_mass_func (Callable[[Angle, float], tuple[float, float, float]], optional):
            Air-mass function to use. Defaults to air_mass_pickering.
        k (float, optional): Atmospheric extinction coefficient. Defaults to 0.20.
        day_offset (Iterable[int], optional): Sequence of integer day offsets to simulate. 
            Defaults to (0, 1, 2, 3, 4).
        verbose (bool, optional): If True, allows the initial geometric search report to 
            print. Defaults to True.

    Raises:
        ValueError: If the star object lacks valid V photometric magnitude data.
    """
    for offset in day_offset:
        # The first iteration honors the global verbose flag; subsequent ones are silenced
        is_first = (offset == list(day_offset)[0]) if isinstance(day_offset, (list, tuple)) else True
        
        scan_twilight_visibility(
            year,
            star,
            phenomena=phenomena,
            city=city,
            ziggurat=ziggurat,
            minutes=minutes,
            ramp_model=ramp_model,
            air_mass_func=air_mass_func,
            k=k,
            day_offset=offset,
            verbose=verbose if is_first else False,
        )


if __name__ == "__main__":
    star = BabStar.from_catalog("Sirius")
    year = -378

    # scan_twilight_visibility(
    #     year,
    #     star,
    #     phenomena="acronychal",
    #     city="Babylon",
    #     ziggurat=0.0,
    #     minutes=6,
    #     k=0.15,
    #     day_offset=-3,
    # )


    star = BabStar.from_catalog("Sirius")
    year = -378

    profile_visibility_sequence(
        -378,
        star,
    )