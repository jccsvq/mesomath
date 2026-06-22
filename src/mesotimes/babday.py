"""`babday.py` - This module handles Babylonian days between two sunsets"""

import re
from functools import total_ordering

from mesotimes.astronomy.sun import bab_day_duration


@total_ordering
class BabylonianDay:
    """
    Represents a Babylonian day, which begins at sunset and ends at the next sunset.
    """

    def __init__(
        self, jd: float, city: str | dict = "Babylon", ziggurat: float = 0.0, title=None
    ):
        """
        Initializes the Babylonian day for a given Julian Date.

        :param jd: Julian Day (JD)
        :param city: Observatory city name, defaults to "Babylon"
        :param ziggurat: Height above terrain in meters, defaults to 0.0
        """
        from math import floor

        self.jd = jd
        self.city = city
        self.ziggurat = ziggurat
        self.title = title

        (
            self.duration,  # Babylonian day duration in hours
            self.diurnal,  # Babylonian day diurnal period duration in hours
            self.nocturnal,  # Babylonian day nocturnal period duration in hours
            self.set1,  # Babylonian day start UT (previous day)
            self.rise2,  # Babylonian day sunrise UT
            self.transit2,  # Babylonian day sun transit UT
            self.set2,  # Babylonian day end UT
        ) = bab_day_duration(jd, city, ziggurat)

        # 1. UT midnight (00:00) of the current day
        midnight_today = floor(self.jd - 0.5) + 0.5

        # 2. The start of the Babylonian day is the sunset of the previous day
        # (Today's midnight - 1 day + hours from set1)
        self.start_jd = (midnight_today - 1.0) + (self.set1 / 24.0)

        # 3. The end of the Babylonian day is the sunset of the current day
        # (Midnight today + hours from set2)
        self.end_jd = midnight_today + (self.set2 / 24.0)
        self.sunrise_jd = midnight_today + (self.rise2 / 24.0)

    def get_vigil(self, target_jd: float) -> str:
        """
        Identifies the night vigil for a specific Julian Date.
        """
        # 1. We check if it is daytime (between sunrise and sunset)
        if self.sunrise_jd <= target_jd < self.end_jd:
            return "Daytime"

        # 2. We check if we are at night (between the start of the day and sunrise)
        if self.start_jd <= target_jd < self.sunrise_jd:
            # Total duration of the night in days (fraction of JD)
            night_duration_jd = self.sunrise_jd - self.start_jd
            vigil_duration_jd = night_duration_jd / 3.0

            # How much time has passed since the sunset
            elapsed = target_jd - self.start_jd
            v_num = int(elapsed / vigil_duration_jd) + 1

            names = {
                1: "First Vigil (barārītu)",
                2: "Middle Vigil (enmaššītu)",
                3: "Morning Vigil (šadduru)",
            }
            return names.get(v_num, "Morning Vigil (šadduru)")

        return "Outside of this Babylonian Day"

    @property
    def info(self):
        """
        Prints information about the Babylonian day.
        """

        def h2hms(h):
            mnt, sec = divmod(h * 3600, 60)
            hrs, mnt = divmod(mnt, 60)
            return f"{int(hrs):02d}:{int(mnt):02d}:{int(sec):02d}"

        print(f"Babylonian day in {self.city}")
        # print(self.Babylonian)
        if self.title:
            print(self.title)
        print(f"{'=' * 62}")
        print(f"Babylonian day duration: {h2hms(self.duration)}")
        print(f"       Diurnal duration: {h2hms(self.diurnal)}")
        print(f"     Nocturnal duration: {h2hms(self.nocturnal)}")
        print(f"   Start (previous day): {h2hms(self.set1)} (UT) {self.start_jd} (JD)")
        print(
            f"                Sunrise: {h2hms(self.rise2)} (UT) {self.sunrise_jd} (JD)"
        )
        print(f"                Transit: {h2hms(self.transit2)} (UT)")
        print(f"                    End: {h2hms(self.set2)} (UT) {self.end_jd} (JD)")

    def ut_to_ush(self, ut_hour: float) -> float:
        """
        Converts a raw UT decimal hour to Babylonian USH (UŠ),
        automatically resolving whether it belongs to the evening of the
        previous civil day or the morning of the current one.

        :param ut_hour: UT time in decimal hours (0.0 to 24.0)
        :type ut_hour: float
        :return: Babylonian USH time in degrees
        :rtype: float
        """
        if not (0.0 <= ut_hour <= 24.0):
            raise ValueError("UT hour must be between 0.0 and 24.0")

        import math

        midnight_today = math.floor(self.jd - 0.5) + 0.5

        # Option A: The UT time belongs to the current civil day (e.g., 03:00 AM today)
        jd_option_a = midnight_today + (ut_hour / 24.0)

        # Option B: The UT time belongs to the previous civil day (e.g., 9:00 PM yesterday)
        jd_option_b = (midnight_today - 1.0) + (ut_hour / 24.0)

        # Evaluate which of the two JDs falls within this Babylonian day
        if self.start_jd <= jd_option_a <= self.end_jd:
            return self.jd_to_ush(jd_option_a)
        elif self.start_jd <= jd_option_b <= self.end_jd:
            return self.jd_to_ush(jd_option_b)
        else:
            raise ValueError(
                f"The UT hour {ut_hour} does not fall within this Babylonian day "
                f"at {self.city} (Starts: {self.set1:.2f} UT, Ends: {self.set2:.2f} UT)"
            )

    def ush_to_ut(self, ush: float) -> float:
        """
        Converts Babylonian USH (UŠ) time degrees to UT decimal hours
        corresponding to the current Babylonian day.

        :param ush: USH (UŠ) time in degrees (0.0 to 360.0)
        :type ush: float
        :return: UT time in decimal hours
        :rtype: float
        """
        if not (0.0 <= ush <= 360.0):
            raise ValueError("USH degrees must be between 0.0 and 360.0")

        # Raw hours elapsed since 00:00 UT on the start day
        raw_hours = (ush / 360.0) * self.duration + self.set1

        return raw_hours % 24.0

    def jd_to_ush(self, target_jd: float) -> float:
        """
        Converts an absolute Julian Date (JD) to Babylonian USH (UŠ) time degrees
        relative to this specific Babylonian day.

        :param target_jd: Julian Date to convert
        :type target_jd: float
        :return: Babylonian USH time in degrees (0.0 to 360.0)
        :rtype: float
        :raises ValueError: If the target_jd falls outside this Babylonian day's boundaries
        """
        if not (self.start_jd <= target_jd <= self.end_jd):
            raise ValueError(
                f"Target JD {target_jd} is outside the boundaries of this Babylonian day "
                f"[{self.start_jd} - {self.end_jd}]"
            )

        # Days elapsed since the start of the Babylonian day (sunset 1)
        elapsed_days = target_jd - self.start_jd

        # Total duration of the Babylonian day expressed in days (fraction of JD)
        duration_days = self.duration / 24.0

        # Scale ratio at 360 degrees
        return (elapsed_days / duration_days) * 360.0

    def ush_to_jd(self, ush: float) -> float:
        """
        Converts Babylonian USH to an absolute Julian Date (JD).

        :param ush: USH (UŠ) time in degrees
        :type ush: float
        :return: Julian day
        :rtype: float
        """
        fraction_of_day = ush / 360.0
        duration_in_days = self.duration / 24.0
        return self.start_jd + (fraction_of_day * duration_in_days)

    def get_time_units(self, target_jd: float) -> dict:
        """
        Calculates time elapsed since sunset in USH and BERU.
        """
        if not (self.start_jd <= target_jd < self.end_jd):
            return {"error": "Outside of this Babylonian day"}

        # Fraction of day elapsed
        elapsed_days = target_jd - self.start_jd

        # Conversion to USH (360 degrees per actual day length)
        # We use the actual duration calculated by bab_day_duration
        duration_days = self.duration / 24.0
        ush = (elapsed_days / duration_days) * 360.0

        # Conversion to BERU (1 BERU = 30 USH)
        beru = ush / 30.0

        return {
            "ush": round(ush, 2),
            "beru": round(beru, 2),
            "vigil": self.get_vigil(target_jd),
        }

    def __repr__(self):
        return (
            f"<BabylonianDay at {self.city}: Start(UT)={self.set1:.4f}, "
            f"End(UT)={self.set2:.4f}, Duration={self.duration:.4f}h>"
        )

    def __eq__(self, other):
        if not isinstance(other, BabylonianDay):
            return NotImplemented
        return self.jd == other.jd

    def __lt__(self, other):
        if not isinstance(other, BabylonianDay):
            return NotImplemented
        return self.jd < other.jd

    def __sub__(self, other):
        """Returns BabylonianDay instance `other` days before the current date"""

        if isinstance(other, int):
            new_jd = self.jd - other
            # Check if the title already has a "days offset" at the end: [+-] X days
            match = re.search(r"([+-]\s*\d+)\s*days$", self.title)
            if match:
                # Extract the current offset and calculate the new net
                current_offset = int(match.group(1).replace(" ", ""))
                new_offset = current_offset - other
                # Replace the final part of the string
                base_title = self.title[: match.start()].strip()
                # If the net is 0, clean the 0 days to leave the original title
                sign = "+" if new_offset >= 0 else "-"
                new_title = (
                    f"{base_title} {sign} {abs(new_offset)} days"
                    if new_offset != 0
                    else base_title
                )
            else:
                new_title = f"{self.title} - {other} days"

            return BabylonianDay(
                new_jd, city=self.city, ziggurat=self.ziggurat, title=new_title
            )
        return NotImplemented

    def __add__(self, other):
        """Returns BabylonianDay instance `other` days after the current date"""
        if isinstance(other, int):
            new_jd = self.jd + other

            # Check if the title already has a "days offset" at the end: [+-] X days
            match = re.search(r"([+-]\s*\d+)\s*days$", self.title)
            if match:
                # Extract the current offset and calculate the new net
                current_offset = int(match.group(1).replace(" ", ""))
                new_offset = current_offset + other
                # Replace the final part of the string
                base_title = self.title[: match.start()].strip()
                # If the net is 0, clean the 0 days to leave the original title
                sign = "+" if new_offset >= 0 else "-"
                new_title = (
                    f"{base_title} {sign} {abs(new_offset)} days"
                    if new_offset != 0
                    else base_title
                )
            else:
                new_title = f"{self.title} + {other} days"

            return BabylonianDay(
                new_jd, city=self.city, ziggurat=self.ziggurat, title=new_title
            )
        return NotImplemented

    def __hash__(self):
        return hash(self.jd)
