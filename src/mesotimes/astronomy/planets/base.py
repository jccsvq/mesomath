"""
`astronomy/planets/base.py` - Abstract base class for planetary ephemerides.
"""

from abc import ABC, abstractmethod
import math
from pymeeus.Epoch import Epoch
from pymeeus import Coordinates
from mesotimes.astronomy.core import mesopotamian_cities, get_horizon_dip


class Planet(ABC):
    """Abstract Base Class representing a planet in Mesopotamian astronomy."""

    def __init__(self, name: str, arc_of_vision: float, debug: bool = False):
        self.name = name
        self.arc_of_vision = arc_of_vision  # Babylonian planetary Arc of Vision (Av)
        self.debug = debug

    @abstractmethod
    def get_geocentric_position(self, epoch: Epoch):
        """
        Must be implemented by each specific planet.
        Should return (ra, dec, elon) from PyMeeus.
        """
        pass

    def calculate_apparent_altitude(
        self, epoch: Epoch, city: str = "Babylon", ziggurat: float = 0.0
    ) -> float:
        """
        SHARED CODE: Converts equatorial geocentric coordinates to horizontal altitude.
        Calculates the local hour angle using rigorous sidereal time mechanics,
        incorporating refraction and ziggurat horizon dip corrections.
        """
        # 1. Geographic parameters and horizon dip correction
        lat = float(mesopotamian_cities[city]["latitude"])
        lon = float(mesopotamian_cities[city]["longitude"])
        alt = float(mesopotamian_cities[city]["altitude"]) + ziggurat
        
        # Horizon dip lowers the reference plane (making the threshold angle more negative)
        horizon_correction = -0.833 - get_horizon_dip(alt)
        
        # 2. Retrieve equatorial coordinates from the specific planet implementation
        ra_obj, dec_obj, _ = self.get_geocentric_position(epoch)
        ra_hours = ra_obj.get_ra()       # Right ascension in decimal hours
        dec_deg = float(dec_obj)         # Declination extracted as raw decimal degrees
        
        if self.debug:
            print(f"[DEBUG] {ra_hours = } {dec_deg = }")

        # 3. Compute Greenwich Apparent Sidereal Time (GAST)
        true_obliquity = Coordinates.true_obliquity(epoch)
        nutation_longitude = Coordinates.nutation_longitude(epoch)
        # CRITICAL: PyMeeus returns sidereal time in decimal fractions of a day [0, 1).
        # We multiply by 24.0 to scale it into standard astronomical hours.
        gast_hours = epoch.apparent_sidereal_time(true_obliquity, nutation_longitude) * 24.0

        # 4. Compute Local Hour Angle (LHA) in degrees
        lon_hours = lon / 15.0
        last_hours = (gast_hours + lon_hours) % 24.0
        ha_degrees = (last_hours - ra_hours) * 15.0
        
        if self.debug:
            print(
                f"[DEBUG] {lon_hours = } {lat = } {last_hours = } "
                f"{ha_degrees = } {gast_hours = }"
            )

        # 5. Spherical trigonometry transformation to geometric Horizontal Altitude
        phi_rad = math.radians(lat)
        dec_rad = math.radians(dec_deg)
        ha_rad = math.radians(ha_degrees)

        sin_alt = math.sin(phi_rad) * math.sin(dec_rad) + math.cos(phi_rad) * math.cos(dec_rad) * math.cos(ha_rad)
        geometric_alt_deg = math.degrees(math.asin(sin_alt))

        # 6. Apply refraction and elevation context adjustments.
        # If the horizon drops due to a ziggurat vantage point, the target's apparent altitude INCREASES.
        apparent_alt_deg = geometric_alt_deg - horizon_correction
        
        if self.debug:
            print(
                f"[DEBUG] {geometric_alt_deg = } {horizon_correction = } "
                f"{apparent_alt_deg = }"
            )

        if self.debug:
            print(f"{self.name} {epoch() =} {apparent_alt_deg =}")
            print(f"     {ra_hours =} {dec_deg =}")
        return apparent_alt_deg

    def is_visible_at_twilight(
        self, epoch_sunset_or_sunrise: Epoch, city: str = "Babylon", ziggurat: float = 0.0
    ) -> bool:
        """
        Determines if the planet is optically visible during the critical historical twilight.
        
        This checks if the planet's apparent altitude is above the horizon at the precise
        instant when the Sun is depressed by the planet's specific Arc of Vision (Av).
        
        :param epoch_sunset_or_sunrise: The Epoch of sunset (for evening stars) or sunrise (for morning stars).
        :param city: The Mesopotamian site registry string.
        :param ziggurat: Observer's elevation in meters.
        :return: True if the planet breaks through the solar glare, False otherwise.
        """
        # 1. Calculate the planet's current altitude at this twilight epoch
        planet_alt = self.calculate_apparent_altitude(
            epoch=epoch_sunset_or_sunrise, city=city, ziggurat=ziggurat
        )
        
        # 2. To be visible, the body must have cleared the adjusted local horizon
        if planet_alt <= 0.0:
            return False
            
        # 3. Verify if the planet's altitude exceeds the required vertical separation
        # from the Sun. In Babylonian mathematical astronomy, at the moment of the planet's 
        # rising/setting, the Sun must be at least -ArcOfVision below the horizon.
        # Alternatively, if evaluated at standard sunset/sunrise, the planet's altitude 
        # must be >= self.arc_of_vision.
        return planet_alt >= self.arc_of_vision