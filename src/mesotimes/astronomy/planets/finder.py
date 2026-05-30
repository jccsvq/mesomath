"""
`astronomy/planets/finder.py` - Root finder for Mesopotamian planetary phases.
"""

from typing import Literal

from mesotimes.astronomy.planets.base import Planet
from mesotimes.astronomy.sun import sun_rise_transit_set
from pymeeus.Epoch import Epoch

def find_heliacal_event(
    planet: Planet,
    start_epoch: Epoch,
    horizon: Literal["sunrise", "sunset"],
    search_type: Literal["appearance", "disappearance"],
    city: str = "Babylon",
    ziggurat: float = 0.0,
    max_days: int = 60,
) -> Epoch:
    """Scans forward day-by-day from an astronomical baseline to locate the exact 
    calendar day of a planet's heliacal event (appearance or disappearance).

    :param planet: The Mesopotamian planet instance.
    :param start_epoch: The starting point for the scan (e.g., date of conjunction).
    :param horizon: Target twilight horizon to evaluate ("sunrise" or "sunset").
    :param search_type: Whether we look for the first day of visibility ("appearance")
                        or the first day of total invisibility ("disappearance").
    :param city: Target city string registry.
    :param ziggurat: Height of the observer structure in meters.
    :param max_days: Safety limit for the iterative loop.
    :return: The Epoch corresponding to the twilight of the resolved event day.
    """
    current_jdn = start_epoch()
    
    # We recorded the initial state of the planet on the day of departure
    ep_init = Epoch(current_jdn, utc=True)
    y_i, m_i, d_i = ep_init.get_date()
    rise_i, _, set_i, _, _, _ = sun_rise_transit_set(int(y_i), int(m_i), int(d_i), city=city, ziggurat=ziggurat)
    h_i = rise_i if horizon == "sunrise" else set_i
    was_visible = planet.is_visible_at_twilight(
        Epoch(int(y_i), int(m_i), int(d_i) + (h_i / 24.0), utc=True), 
        city=city, 
        ziggurat=ziggurat
    )

    # We move on to the first day of actual scanning
    current_jdn += 1.0

    for _ in range(max_days - 1):
        ep_step = Epoch(current_jdn, utc=True)
        year, month, day = ep_step.get_date()

        rise_ut, _, set_ut, _, _, _ = sun_rise_transit_set(
            int(year), int(month), int(day), city=city, ziggurat=ziggurat
        )

        target_hour = rise_ut if horizon == "sunrise" else set_ut
        twilight_epoch = Epoch(int(year), int(month), int(day) + (target_hour / 24.0), utc=True)

        # We evaluate the current visibility
        is_visible = planet.is_visible_at_twilight(twilight_epoch, city=city, ziggurat=ziggurat)

        # --- CRITICAL TRANSITION LOGIC ---
        if search_type == "appearance":
            # Heliacal Rising/Setting: Yesterday INVISIBLE, today VISIBLE
            if is_visible and not was_visible:
                return twilight_epoch
                
        elif search_type == "disappearance":
            # Babylonian adjustment: We look for the LAST day of visibility (Yesterday VISIBLE, today INVISIBLE)
            # We return yesterday's twilight, which was the last time the scribe saw it shine.
            if not is_visible and was_visible:
                # We calculate the twilight of the previous day to return the exact date of the last sighting
                prev_year, prev_month, prev_day = Epoch(current_jdn - 1.0, utc=True).get_date()
                prev_rise, _, prev_set, _, _, _ = sun_rise_transit_set(int(prev_year), int(prev_month), int(prev_day), city=city, ziggurat=ziggurat)
                prev_hour = prev_rise if horizon == "sunrise" else prev_set
                return Epoch(int(prev_year), int(prev_month), int(prev_day) + (prev_hour / 24.0), utc=True)

        # Today's state will be the 'yesterday' of the next iteration
        was_visible = is_visible
        current_jdn += 1.0

    raise RuntimeError(
        f"Heliacal {search_type} on {horizon} not found within {max_days} days for {planet.name}."
    )

def find_heliacal_event2(
    planet: Planet,
    start_epoch: Epoch,
    horizon: Literal["sunrise", "sunset"],
    search_type: Literal["appearance", "disappearance"],
    city: str = "Babylon",
    ziggurat: float = 0.0,
    max_days: int = 60,
) -> Epoch:
    """
    Scans forward day-by-day from an astronomical baseline to locate the exact 
    calendar day of a planet's heliacal event (appearance or disappearance).

    :param planet: The Mesopotamian planet instance.
    :param start_epoch: The starting point for the scan (e.g., date of conjunction).
    :param horizon: Target twilight horizon to evaluate ("sunrise" or "sunset").
    :param search_type: Whether we look for the first day of visibility ("appearance")
                        or the first day of total invisibility ("disappearance").
    :param city: Target city string registry.
    :param ziggurat: Height of the observer structure in meters.
    :param max_days: Safety limit for the iterative loop.
    :return: The Epoch corresponding to the twilight of the resolved event day.
    """
    current_jdn = start_epoch()

    for _ in range(max_days):
        ep_step = Epoch(current_jdn, utc=True)
        year, month, day = ep_step.get_date()

        # 1. Compute solar horizons for the local site (returns UT decimal hours)
        rise_ut, _, set_ut, _, _, _ = sun_rise_transit_set(
            int(year), int(month), int(day), city=city, ziggurat=ziggurat
        )

        # 2. Select the precise twilight target based on the required horizon
        target_hour = rise_ut if horizon == "sunrise" else set_ut
        day_fraction = target_hour / 24.0
        twilight_epoch = Epoch(int(year), int(month), int(day) + day_fraction, utc=True)

        # 3. Evaluate visibility through our base OOM rules
        is_visible = planet.is_visible_at_twilight(twilight_epoch, city=city, ziggurat=ziggurat)

        # 4. Phase-change logic branching
        if search_type == "appearance" and is_visible:
            # First day the planet breaks through the solar glare (Gamma / Xi)
            return twilight_epoch
        
        if search_type == "disappearance" and not is_visible:
            # First day the planet fails to clear the Arc of Vision and vanishes (Omega / Sigma)
            return twilight_epoch

        # Step forward by exactly one calendar/Julian day
        current_jdn += 1.0

    raise RuntimeError(
        f"Heliacal {search_type} on {horizon} not found within {max_days} days for {planet.name}."
    )


def find_first_appearance_morning(planet: Planet, start_epoch: Epoch, city: str = "Babylon", ziggurat: float = 0.0) -> Epoch:
    """Finds the First Heliacal Appearance in the East before sunrise (Phenomenon Gamma / Xi)."""
    return find_heliacal_event(planet, start_epoch, horizon="sunrise", search_type="appearance", city=city, ziggurat=ziggurat)


def find_last_appearance_evening(planet: Planet, start_epoch: Epoch, city: str = "Babylon", ziggurat: float = 0.0) -> Epoch:
    """Finds the Last Heliacal Appearance in the West after sunset (Phenomenon Omega / Sigma)."""
    return find_heliacal_event(planet, start_epoch, horizon="sunset", search_type="appearance", city=city, ziggurat=ziggurat)


def find_setting_heliacal_morning(planet: Planet, start_epoch: Epoch, city: str = "Babylon", ziggurat: float = 0.0) -> Epoch:
    """Finds the Morning Heliacal Setting/Disappearance in the East (Phenomenon Delta)."""
    return find_heliacal_event(planet, start_epoch, horizon="sunrise", search_type="disappearance", city=city, ziggurat=ziggurat)


def find_setting_heliacal_evening(planet: Planet, start_epoch: Epoch, city: str = "Babylon", ziggurat: float = 0.0) -> Epoch:
    """Finds the Evening Heliacal Setting/Disappearance in the West (Phenomenon Epsilon)."""
    return find_heliacal_event(planet, start_epoch, horizon="sunset", search_type="disappearance", city=city, ziggurat=ziggurat)