"""
`astronomy/planets/inferiors.py` - Inferior planets implementation.
"""

# import math
from mesotimes.astronomy.planets.base import Planet
from pymeeus.Epoch import Epoch
from pymeeus.Mercury import Mercury
from pymeeus.Venus import Venus


class InferiorPlanet(Planet):
    """Base class for planets closer to the Sun than the Earth (Venus, Mercury)."""


    def __init__(self, name: str, arc_of_vision: float, debug: bool = False):
        super().__init__(name=name, arc_of_vision=arc_of_vision, debug=debug)
        # Placeholder overridden by concrete subclass instances
        self._pymeeus_planet = None

    def get_geocentric_position(self, epoch: Epoch):
        """Wraps PyMeeus native geocentric calculation using the instance."""
        return self._pymeeus_planet.geocentric_position(epoch)

    def get_inferior_conjunction(self, epoch: Epoch):
        """Wraps PyMeeus native inferior conjunction calculation using the instance."""
        return self._pymeeus_planet.inferior_conjunction(epoch)

    def get_superior_conjunction(self, epoch: Epoch):
        """Wraps PyMeeus native superior conjunction calculation using the instance."""
        return self._pymeeus_planet.superior_conjunction(epoch)

    def get_western_elongation_time(self, epoch: Epoch):
        """Wraps PyMeeus native western elongation calculation using the instance."""
        time, _ = self._pymeeus_planet.western_elongation(epoch)
        return time

    def get_western_elongation(self, epoch: Epoch):
        """Wraps PyMeeus native western elongation calculation using the instance."""
        _, elon = self._pymeeus_planet.western_elongation(epoch)
        return elon

    def get_eastern_elongation_time(self, epoch: Epoch):
        """Wraps PyMeeus native eastern elongation calculation using the instance."""
        time, _ = self._pymeeus_planet.eastern_elongation(epoch)
        return time

    def get_eastern_elongation(self, epoch: Epoch):
        """Wraps PyMeeus native eastern elongation calculation using the instance."""
        _, elon = self._pymeeus_planet.eastern_elongation(epoch)
        return elon

    def get_station_longitude_1(self, epoch: Epoch):
        """Wraps PyMeeus native station longitude 1 calculation using the instance."""
        return self._pymeeus_planet.station_longitude_1(epoch)

    def get_station_longitude_2(self, epoch: Epoch):
        """Wraps PyMeeus native station longitude 2 calculation using the instance."""
        return self._pymeeus_planet.station_longitude_2(epoch)

    @property
    def phenomena_list(self):
        """"""
        return [
        self.get_inferior_conjunction,
        self.get_superior_conjunction,
        self.get_western_elongation_time,
        self.get_western_elongation,
        self.get_eastern_elongation_time,
        self.get_eastern_elongation,
        self.get_station_longitude_1,
        self.get_station_longitude_2,
    ]

class MesopotamianVenus(InferiorPlanet):
    """Venus computations tailored for Babylonian astronomical phenomena (The Ninsianna diary)."""

    def __init__(self, debug: bool = False) -> None:
        # Venus has a standard Babylonian Arc of Vision (Av) of 6.0 degrees
        super().__init__(name="Venus", arc_of_vision=6.0, debug=debug)
        self._pymeeus_planet = Venus()


class MesopotamianMercury(InferiorPlanet):
    """Mercury computations tailored for Babylonian astronomical phenomena."""

    def __init__(self, debug: bool = False) -> None:
        # Mercury requires a much larger Arc of Vision due to its proximity to solar glare
        super().__init__(name="Mercury", arc_of_vision=12.0, debug=debug)
        self._pymeeus_planet = Mercury()
