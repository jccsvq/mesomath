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
    city: str | dict = "Babylon",
    ziggurat: float = 0.0,
    max_days: int = 60,
    strict_bounds: bool = True,  # <--- Nuestro nuevo flag de control
) -> Epoch:
    """Scans forward day-by-day from an astronomical baseline to locate the exact
    calendar day of a celestial object's heliacal event (appearance or disappearance).

    Args:
        planet (Planet): The Mesopotamian planet or star instance.
        start_epoch (Epoch): The starting point for the scan (e.g., date of conjunction).
        horizon (Literal["sunrise", "sunset"]): Target twilight horizon to evaluate.
        search_type (Literal["appearance", "disappearance"]): Whether we look for the first
            day of visibility ("appearance") or the first day of total invisibility ("disappearance").
        city (str | dict, optional): Target city string registry. Defaults to "Babylon".
        ziggurat (float, optional): Height of the observer above terrain in meters. Defaults to 0.0.
        max_days (int, optional): Maximum number of days to scan. Defaults to 60.
        strict_bounds (bool, optional): If True, validates initial visibility state to guard
            against false positives (useful for stars). Defaults to True.

    Raises:
        ValueError: If `strict_bounds` is True and searching for an "appearance" but the
            object is already visible on the departure date.
        ValueError: If `strict_bounds` is True and searching for a "disappearance" but the
            object is already invisible on the departure date.
        RuntimeError: If the iterative day-by-day scanning loop reaches `max_days` without
            detecting the critical visibility transition.

    Returns:
        Epoch: The Epoch corresponding to the twilight of the resolved event day.
    """
    current_jdn = start_epoch()

    # Record the initial state of the planet on the day of departure
    ep_init = Epoch(current_jdn, utc=True)
    y_i, m_i, d_i = ep_init.get_date()
    rise_i, _, set_i, _, _, _ = sun_rise_transit_set(
        int(y_i), int(m_i), int(d_i), city=city, ziggurat=ziggurat
    )
    h_i = rise_i if horizon == "sunrise" else set_i
    twilight_init = Epoch(int(y_i), int(m_i), int(d_i) + (h_i / 24.0), utc=True)
    was_visible = planet.is_visible_at_twilight(
        twilight_init, city=city, ziggurat=ziggurat
    )

    # --- SHIELD AGAINST FALSE POSITIVES (Bifurcated) ---
    if strict_bounds:
        if search_type == "appearance" and was_visible:
            raise ValueError(
                f"[{planet.name}] Initialization Error: Object is ALREADY VISIBLE on the start date ({twilight_init.get_date()}). "
                f"To find an 'appearance', the search must begin during the object's period of invisibility."
            )

        if search_type == "disappearance" and not was_visible:
            raise ValueError(
                f"[{planet.name}] Initialization Error: Object is ALREADY INVISIBLE on the start date ({twilight_init.get_date()}). "
                f"To find a 'disappearance', the search must begin during the object's period of visibility."
            )
    # ---------------------------------------------------

    # We move on to the first day of actual scanning
    current_jdn += 1.0

    for _ in range(max_days - 1):
        ep_step = Epoch(current_jdn, utc=True)
        year, month, day = ep_step.get_date()

        rise_ut, _, set_ut, _, _, _ = sun_rise_transit_set(
            int(year), int(month), int(day), city=city, ziggurat=ziggurat
        )

        target_hour = rise_ut if horizon == "sunrise" else set_ut
        twilight_epoch = Epoch(
            int(year), int(month), int(day) + (target_hour / 24.0), utc=True
        )

        # We evaluate the current visibility
        is_visible = planet.is_visible_at_twilight(
            twilight_epoch, city=city, ziggurat=ziggurat
        )

        # --- CRITICAL TRANSITION LOGIC ---
        if search_type == "appearance":
            # Heliacal Rising/Setting: Yesterday INVISIBLE, today VISIBLE
            if is_visible and not was_visible:
                return twilight_epoch

        elif search_type == "disappearance":
            # Babylonian adjustment: We look for the LAST day of visibility (Yesterday VISIBLE, today INVISIBLE)
            if not is_visible and was_visible:
                prev_year, prev_month, prev_day = Epoch(
                    current_jdn - 1.0, utc=True
                ).get_date()
                prev_rise, _, prev_set, _, _, _ = sun_rise_transit_set(
                    int(prev_year),
                    int(prev_month),
                    int(prev_day),
                    city=city,
                    ziggurat=ziggurat,
                )
                prev_hour = prev_rise if horizon == "sunrise" else prev_set
                return Epoch(
                    int(prev_year),
                    int(prev_month),
                    int(prev_day) + (prev_hour / 24.0),
                    utc=True,
                )

        # Today's state will be the 'yesterday' of the next iteration
        was_visible = is_visible
        current_jdn += 1.0

    raise RuntimeError(
        f"Heliacal {search_type} on {horizon} not found within {max_days} days for {planet.name}."
    )


def find_first_appearance_morning(
    planet: Planet, start_epoch: Epoch, city: str | dict = "Babylon", ziggurat: float = 0.0
) -> Epoch:
    """Finds the First Heliacal Appearance in the East before sunrise (Phenomenon Gamma / Xi)."""
    return find_heliacal_event(
        planet,
        start_epoch,
        horizon="sunrise",
        search_type="appearance",
        city=city,
        ziggurat=ziggurat,
        strict_bounds=False,
    )


def find_last_appearance_evening(
    planet: Planet, start_epoch: Epoch, city: str | dict = "Babylon", ziggurat: float = 0.0
) -> Epoch:
    """Finds the Last Heliacal Appearance in the West after sunset (Phenomenon Omega / Sigma)."""
    return find_heliacal_event(
        planet,
        start_epoch,
        horizon="sunset",
        search_type="appearance",
        city=city,
        ziggurat=ziggurat,
        strict_bounds=False,
    )


def find_setting_heliacal_morning(
    planet: Planet, start_epoch: Epoch, city: str | dict = "Babylon", ziggurat: float = 0.0
) -> Epoch:
    """Finds the Morning Heliacal Setting/Disappearance in the East (Phenomenon Delta)."""
    return find_heliacal_event(
        planet,
        start_epoch,
        horizon="sunrise",
        search_type="disappearance",
        city=city,
        ziggurat=ziggurat,
        strict_bounds=False,
    )


def find_setting_heliacal_evening(
    planet: Planet, start_epoch: Epoch, city: str | dict = "Babylon", ziggurat: float = 0.0
) -> Epoch:
    """Finds the Evening Heliacal Setting/Disappearance in the West (Phenomenon Epsilon)."""
    return find_heliacal_event(
        planet,
        start_epoch,
        horizon="sunset",
        search_type="disappearance",
        city=city,
        ziggurat=ziggurat,
        strict_bounds=False,
    )
