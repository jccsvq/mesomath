"""
This module implements the Proleptic Babylonian Calendar based on the
standardized Metonic cycle and astronomical visibility.
"""

import math

from pymeeus.Epoch import Epoch
from pymeeus.Moon import Moon

from mesotimes.astronomy.moon import check_neomenia
from mesotimes.astronomy.sun import vernal_equinox


def proleptic_year_months(year: int, codes: bool = False) -> tuple[list, int]:
    """
    Return the list of month names of the proleptic Babylonian year that begins
    around the spring equinox and the number of lunar months of that year.

    :param year: Julian/Gregorian year
    :type year: int
    :param codes: Return month codes instead of names, defaults to False
    :type codes: bool, optional
    :return: List of months and number of months
    :rtype: tuple[list, int]
    """
    from mesotimes.constants import MONTH_DICT as monthdict

    # Extract semesters from monthdict
    semester1 = (
        list(monthdict.values())[:6] if not codes else list(monthdict.keys())[:6]
    )
    semester2 = (
        list(monthdict.values())[7:13] if not codes else list(monthdict.keys())[7:13]
    )

    # Metonic cycle year number
    # For year 49 CE was number 17
    mn = (year + 5) % 19 + 1

    # Leap months
    if mn in {3, 6, 8, 11, 14, 19}:
        # Addaru II
        leap_month = ["Addaru II"] if not codes else ["12.5"]
        return semester1 + semester2 + leap_month, 13
    elif mn == 17:
        # Ululu II
        leap_month = ["Ululu II"] if not codes else ["6.5"]
        return semester1 + leap_month + semester2, 13
    else:
        # No leap month
        return semester1 + semester2, 12


class ProlepticBabylonianCalendar:
    """
    Reconstructs the Babylonian calendar for years outside the historical
    canon using the 19-year Metonic cycle and lunar visibility.
    """

    def __init__(
        self,
        year: int,
        city: str | dict = "Babylon",
        ziggurat: float = 0.0,
        AoV: float = 12.0,
        uncertainty: float = 0.833,
    ):
        """
        Initializes the calendar for a specific astronomical year.

        :param year: Astronomical year
        :type year: int
        :param city: Observation site, defaults to "Babylon"
        :type city: str | dict, optional
        :param ziggutat: Observer height above terrain in meters, defaults to 0.0
        :type ziggurat: float, optional
        :param AoV: Arc of Vision in degrees, defaults to 12.0
        :type AoV: float, optional
        :param uncertainty: Uncertainty or marginal visibility factor, defaults to 0.833
        :type uncertainty: float, optional
        """
        self.year = year
        self.city = city
        self.ziggurat = ziggurat
        self.AoV = AoV
        self.uncertainty = uncertainty
        self.structure = self._generate_year_structure()

    def _find_nisannu_1(self) -> float:
        """
        Finds the starting JDE of Nisannu for the current year.

        :return: JDE of Nisannu 1
        :rtype: float
        """
        jde_equinox = vernal_equinox(self.year)
        approx_nm = Moon.moon_phase(Epoch(jde_equinox), target="new")

        # Search starting from the first possible sunset after New Moon
        current_jde = math.floor(approx_nm.jde()) + 0.5
        for attempt in range(0, 35):
            test_jde = current_jde + attempt
            e = Epoch(test_jde)
            y, m, d = e.get_date()[:3]

            na, alt = check_neomenia(
                y,
                m,
                int(d),
                city=self.city,
                ziggurat=self.ziggurat,
                AoV=self.AoV,
                uncertainty=self.uncertainty,
                verbose=False,
            )

            if na > (4 * self.AoV) and alt > 0:
                return Epoch(y, m, int(d), 0, 0, 0).jde()
        return None

    def _generate_year_structure(self) -> list[dict]:
        """
        Generates the months, their starting dates and lengths.

        :return: List of dictionaries with month info
        :rtype: list[dict]
        """
        month_names, total_months = proleptic_year_months(self.year)
        calendar = []
        current_day_1 = self._find_nisannu_1()

        for i in range(total_months):
            # To find the next month's start, we look at the next lunation
            next_nm = Moon.moon_phase(Epoch(current_day_1 + 25), target="new")
            next_day_1 = None

            # Visibility search for next month
            search_start = math.floor(next_nm.jde()) + 0.5
            for d in range(0, 5):
                test_e = Epoch(search_start + d)
                y, m, day = test_e.get_date()[:3]
                na, alt = check_neomenia(
                    y,
                    m,
                    int(day),
                    city=self.city,
                    ziggurat=self.ziggurat,
                    AoV=self.AoV,
                    uncertainty=self.uncertainty,
                    verbose=False,
                )
                if na > (4 * self.AoV) and alt > 0:
                    next_day_1 = Epoch(y, m, int(day), 0, 0, 0).jde()
                    break

            duration = int(next_day_1 - current_day_1)
            calendar.append(
                {
                    "index": i + 1,
                    "name": month_names[i],
                    "jde_start": current_day_1,
                    "date_iso": Epoch(current_day_1).get_date(),
                    "length": duration,
                }
            )
            current_day_1 = next_day_1

        return calendar

    def get_month(self, name_or_index: str | int) -> dict | None:
        """
        Retrieves data for a specific month by its name or 1-based index.

        :param name_or_index: Month name or 1-based index
        :type name_or_index: str | int
        :return: Dictionary with month info or None if not found
        :rtype: dict | None
        """
        for m in self.structure:
            if m["name"] == name_or_index or m["index"] == name_or_index:
                return m
        return None

    def convert_to_babylonian(self, date_input: Epoch | float) -> dict | None:
        """
        Converts a Julian/Gregorian date to the Babylonian proleptic calendar.

        :param date_input: Can be a pymeeus Epoch or a float (JDE)
        :type date_input: Epoch | float
        :return: Dictionary with Babylonian date info or None if out of range
        :rtype: dict | None
        """
        if isinstance(date_input, Epoch):
            target_jde = date_input.jde()
        else:
            target_jde = float(date_input)

        # The Babylonian day begins at sunset.
        # If the JDE is < .5, it technically belongs to the previous Babylonian day.
        # We adjust so that the search is consistent with the civil calendar.
        search_jde = target_jde

        for m in self.structure:
            start = m["jde_start"]
            end = start + m["length"]

            if start <= search_jde < end:
                day = int(search_jde - start) + 1
                return {
                    "year": self.year,
                    "month_name": m["name"],
                    "month_index": m["index"],
                    "day": day,
                    "jde": target_jde,
                }
        return None

    def print_year_table(self):
        """
        Prints a human-readable table of the Babylonian year structure.
        """
        header = f"--- PROLEPTIC BABYLONIAN CALENDAR: YEAR {self.year} ---"
        print(f"\n{header}")
        print(
            f"{'#':<3} {'Month Name':<12} {'Start Date (Y/M/D)':<20} {'JDE Start':<15} {'Length':<6}"
        )
        print("-" * int(len(header) * 1.5))

        for m in self.structure:
            y, month, d = m["date_iso"]
            date_str = f"{y}/{month:02d}/{int(d):02d}"
            print(
                f"{m['index']:<3} {m['name']:<12} {date_str:<20} {m['jde_start']:<15.1f} {m['length']:<6} days"
            )

        # Calculation of the end of the year (beginning of the following Nisannu)
        last_month = self.structure[-1]
        end_jde = last_month["jde_start"] + last_month["length"]
        ey, em, ed = Epoch(end_jde).get_date()[:3]

        print("-" * int(len(header) * 1.5))
        print(
            f"Year ends on: {int(ey)}/{int(em):02d}/{int(ed):02d} (JDE {end_jde:.1f})"
        )
        total_days = sum(m["length"] for m in self.structure)
        print(
            f"Total year duration: {total_days} days ({'Leap year' if len(self.structure) > 12 else 'Common year'})"
        )

    def __repr__(self):
        return f"<ProlepticBabylonianCalendar for Year {self.year} ({len(self.structure)} months)>"


# if __name__ == "__main__":
