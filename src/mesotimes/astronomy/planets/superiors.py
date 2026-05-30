"""
`astronomy/planets/superiors.py` - Superior planets implementation.
"""

import math
from pymeeus.Epoch import Epoch
from pymeeus.Mars import Mars
from pymeeus.Jupiter import Jupiter
from pymeeus.Saturn import Saturn

from mesotimes.astronomy.planets.base import Planet


class SuperiorPlanet(Planet):
    """Base class for planets further from the Sun than the Earth (Mars, Jupiter, Saturn)."""

    def __init__(self, name: str, arc_of_vision: float, debug: bool = False):
        super().__init__(name=name, arc_of_vision=arc_of_vision, debug=debug)
        # This placeholder will be overridden by the concrete subclass instances
        self._pymeeus_planet = None

    def get_geocentric_position(self, epoch: Epoch):
        """Wraps PyMeeus native geocentric calculation using the instance."""
        return self._pymeeus_planet.geocentric_position(epoch)

    def get_conjunction(self, epoch: Epoch):
        """Wraps PyMeeus native conjunction calculation using the instance."""
        return self._pymeeus_planet.conjunction(epoch)

    def get_opposition(self, epoch: Epoch):
        """Wraps PyMeeus native opposition calculation using the instance."""
        return self._pymeeus_planet.opposition(epoch)

    def get_station_longitude_1(self, epoch: Epoch):
        """Wraps PyMeeus native station longitude 1 calculation using the instance."""
        return self._pymeeus_planet.station_longitude_1(epoch)

    def get_station_longitude_2(self, epoch: Epoch):
        """Wraps PyMeeus native station longitude 2 calculation using the instance."""
        return self._pymeeus_planet.station_longitude_2(epoch)

    def is_in_opposition(self, epoch: Epoch, tolerance_deg: float = 0.5) -> bool:
        """
        Checks if the planet is in acronychal opposition (Theta phenomena).
        Elongation close to 180 degrees.
        """
        _, _, elon = self.get_geocentric_position(epoch)
        return math.isclose(elon(), 180.0, abs_tol=tolerance_deg)

    @property
    def phenomena_list(self):
        """"""
        return [
            self.get_conjunction,
            self.get_opposition,
            self.get_station_longitude_1,
            self.get_station_longitude_2,
        ]




class MesopotamianMars(SuperiorPlanet):
    """Mars computations tailored for Babylonian astronomical phenomena."""

    def __init__(self, debug: bool = False) -> None:
        super().__init__(name="Mars", arc_of_vision=14.0, debug=debug)
        self._pymeeus_planet = Mars()


class MesopotamianJupiter(SuperiorPlanet):
    """Jupiter computations tailored for Babylonian astronomical phenomena."""

    def __init__(self, debug: bool = False) -> None:
        super().__init__(name="Jupiter", arc_of_vision=9.0, debug=debug)
        self._pymeeus_planet = Jupiter()


class MesopotamianSaturn(SuperiorPlanet):
    """Saturn computations tailored for Babylonian astronomical phenomena."""

    def __init__(self, debug: bool = False) -> None:
        super().__init__(name="Saturn", arc_of_vision=11.0, debug=debug)
        self._pymeeus_planet = Saturn()