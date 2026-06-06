"""This module implements the analysis of the Babylonian lunar month"""

import sqlite3
from pathlib import Path
from importlib.resources import files

from mesotimes.astronomy.core import jde2date, mesopotamian_cities
from mesotimes.astronomy.moon import (
    calculate_kur,
    calculate_mi_mush,
    calculate_shu_interval,
    check_neomenia,
)
from pymeeus.Epoch import Epoch
from pymeeus.Moon import Moon


class LunarAlmanac:
    """Manages the analysis of a Babylonian lunar month."""

    def __init__(
        self,
        year: int,
        month: int,
        city: str = "Babylon",
        ziggurat: float = 0.0,
        db_filename: str = "mesotimes.sqlite",
        AoV: float = 12.0,
        uncertainty: float = 0.833,
    ):
        """Instance creator

        :param year: Year (julian/gregorian)
        :type year: int
        :param month: Month (julian/gregorian)
        :type month: int
        :param city: City name, defaults to "Babylon"
        :type city: str, optional
        :param ziggurat: Height above the ground, defaults to 0.0
        :type ziggurat: float, optional
        :param db_filename: mesotimes SQLite database filename, defaults to "mesotimes.sqlite"
        :type db_filename: str, optional
        :param AoV: Arc of vision in degrees (for neomenia), defaults to 12.0
        :type AoV: float, optional
        :param uncertainty: Uncertainty or marginal visibility factor, defaults to 0.833
        :type uncertainty: float, optional
        :raises FileNotFoundError: Database not found
        """
        self.year = year
        self.month = month
        self.city = city
        self.ziggurat = ziggurat
        self.AoV = AoV  # USH in degrees
        self.uncertainty = uncertainty

        target_epoch = Epoch(self.year, self.month, 1)
        # Search for the New Moon anchor
        nm_date = Moon.moon_phase(target_epoch - 15.0, target="new")

        # CLEAN EXTRACTION: We obtain only the whole part of the date
        y, m, d_float = nm_date.get_date()
        # We created a new Epoch at 00:00:00 on that day
        self.nm_anchor = Epoch(y, m, int(d_float), 0, 0, 0)

        # DATABASE CONNECTOR
        # 1. We dynamically and safely locate the resource within the package
        # This works locally (editable), in virtual environments, installed wheels, or containers.
        self.db_path = Path(files("mesotimes").joinpath("db", db_filename))

        # 2. Explicit security control in case the file gets corrupted or deleted
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database critical error: '{db_filename}' not found inside mesotimes/db/. "
                f"Resolved path was: {self.db_path}"
            )

    def scan_month(self) -> dict:
        """Search for astronomical events in the Babylonian month.

        :return: Dictionary with astronomical events
        :rtype: dict
        """
        results = {"na": None, "opposition": [], "kur": None}

        # 1. NEOMENIA (Day 1)
        for i in range(1, 4):
            # By using self.nm_anchor (which is 00:00:00), +i always gives midnight

            test_date = (
                self.nm_anchor + i
            )  # Epoch handles the month/year change automatically
            y, m, d = test_date.get_date()[:3]
            na, alt = check_neomenia(
                y,
                m,
                d,
                self.city,
                verbose=False,
                AoV=self.AoV,
                uncertainty=self.uncertainty,
            )
            if na > 12.0 and alt > 0:
                results["na"] = (f"{y}/{m}/{int(d)}", na)
                self.day_1_jde = test_date.jde()
                break

        # 2. OPPOSITION (Day 14-15)
        if hasattr(self, "day_1_jde"):
            for i in range(13, 16):
                # i=13 corresponds to the 14th day of the Babylonian month
                current_jde = self.day_1_jde + i
                y, m, d = Epoch(current_jde).get_date()[:3]

                mush = calculate_mi_mush(y, m, d, self.city)[0]
                shu = calculate_shu_interval(y, m, d, self.city)

                # Relevance filter: we only save what an observer would report
                current_day_data = {"date": f"{y}/{m}/{int(d)}"}

                if abs(mush) < 150:  # Less than 2.5 hours
                    current_day_data["mi_mush"] = mush
                if abs(shu) < 150:
                    current_day_data["shu"] = shu

                if "mi_mush" in current_day_data or "shu" in current_day_data:
                    results["opposition"].append(current_day_data)

        # 3. LAST VISIBILITY (Day 28-29)
        for i in range(27, 30):
            current_jde = self.day_1_jde + i
            y, m, d = Epoch(current_jde).get_date()[:3]
            kur = calculate_kur(y, m, d, self.city)[0]
            if kur > 0:
                results["kur"] = (f"{y}/{m}/{int(d)}", kur)

        # Special events store
        results["eclipses"] = []

        # 1. Solar Eclipse in Neomenia or end of the month?
        for jde in [self.nm_anchor.jde(), self.day_1_jde + 28]:
            y, m, d = Epoch(jde).get_date()[:3]
            ecl = self._query_eclipse(y, m, int(d))
            if ecl and "Solar" in ecl["type"]:
                results["eclipses"].append(ecl)

        # 2. Lunar Eclipse in the Full Moon?
        if hasattr(self, "day_1_jde"):
            # We scan the opposition window (Days 13, 14, 15)
            for i in range(13, 16):
                y, m, d = Epoch(self.day_1_jde + i).get_date()[:3]
                ecl = self._query_eclipse(y, m, int(d))
                if ecl and "Lunar" in ecl["type"]:
                    results["eclipses"].append(ecl)

        results["length"] = self.determine_month_length()
        self.data = results
        return results

    def to_tablet(self):
        """
        Generate a monthly report in the format of a Babylonian chronicle.
        """
        if not hasattr(self, "data"):
            self.scan_month()

        header = f"--- ASTRONOMICAL DIARY: YEAR {self.year}, MONTH {self.month} ---"
        print(f"\n{header}")
        print(
            f"City: {self.city}  | Coordinates: (Lat: {mesopotamian_cities[self.city]['latitude']})"
        )
        print("-" * len(header))

        # 1. Neomenia (Day 1)
        if self.data["na"]:
            date, val = self.data["na"]
            ush = val / 4.0
            status = "VISIBLE" if ush > 3 else "UNCERTAIN"
            print(f"[Day 01]  NA: {ush:5.2f} UŠ | Date: {date} ({status})")

        # 2. Opposition (Day 14-15)
        for entry in self.data["opposition"]:
            date = entry["date"]
            if "mi_mush" in entry:
                ush = entry["mi_mush"] / 4.0
                label = "  ME" if ush > 0 else " GE₆"  # Actual Babylonian terminology
                print(f"[Full ] {label:2}: {abs(ush):5.2f} UŠ | Date: {date}")
            if "shu" in entry:
                ush = entry["shu"] / 4.0
                print(f"[Full ]  ŠÚ: {ush:5.2f} UŠ | Date: {date}")

        # 3. Disappearance (Day 28-29)
        if self.data["kur"]:
            date, val = self.data["kur"]
            ush = val / 4.0
            print(f"[Day 28] KUR: {ush:5.2f} UŠ | Date: {date} (Last Vis.)")

        print("-" * len(header))

        length_str = "Hollow" if self.data["length"] == 29 else "Full"
        print(f"Month Duration: {self.data['length']} days ({length_str})")

        if self.data.get("eclipses"):
            print("\n[!] PROPHETIC EVENTS (Eclipses):")
            for e in self.data["eclipses"]:
                print(
                    f"    - {e['type']} detected on {e['year']}/{e['month']}/{e['day']}"
                )
                print(f"      Magnitude: {e['mag']}")

    def determine_month_length(self) -> int:
        """
        Determine if the month is 'Full' (30 days) or 'Hollow' (29 days).
        Calculate the visibility of the next crescent.

        :return: Length of the month in days
        :rtype: int
        """
        # 1. Next New Moon (approximately 29.5 days later)
        next_nm_date = Moon.moon_phase(self.nm_anchor + 25.0, target="new")
        y, m, d_float = next_nm_date.get_date()
        next_nm_anchor = Epoch(y, m, int(d_float), 0, 0, 0)

        # 2. Day 1 of the NEXT month
        next_day_1_jde = None
        for i in range(1, 4):
            test_date = next_nm_anchor + i
            ny, nm, nd = test_date.get_date()[:3]
            na, alt = check_neomenia(
                ny,
                nm,
                nd,
                city=self.city,
                ziggurat=self.ziggurat,
                verbose=False,
                AoV=self.AoV,
                uncertainty=self.uncertainty,
            )
            # Threshold based on dynamic AoV
            if na > (4 * self.AoV) and alt > 0:
                next_day_1_jde = test_date.jde()
                break

        # 3. Difference calculation
        if next_day_1_jde and hasattr(self, "day_1_jde"):
            length = int(next_day_1_jde - self.day_1_jde)
            return length

        return 30  # Default value if there is a visibility error

    def _query_eclipse(self, y: int, m: int, d: int) -> dict | None:
        """
        Query the database for a specific day, search for eclipses that were visible from Kish.

        :param y: Year (julian)
        :type y: int
        :param m: Month (julian)
        :type m: int
        :param d: Day (julian)
        :type d: int
        :return: Eclipse for the date if it exists, None otherwise
        :rtype: dict | None
        """
        query = "SELECT * FROM kishecl WHERE year = ? AND month = ? AND day = ?"
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: {
                "year": row[0],
                "month": row[1],
                "day": row[2],
                "type": row[3],
                "mag": row[4],
            }
            cursor = conn.cursor()
            cursor.execute(query, (y, m, d))
            return cursor.fetchone()  # Returns dict or None


def jde2lunar_almanac(
    jde: float,
    city: str = "Babylon",
    ziggurat: float = 0.0,
    AoV: float = 12.0,
    uncertainty: float = 0.833,
) -> LunarAlmanac:
    """"""
    y, m, d = jde2date(jde)
    return LunarAlmanac(y, m, city, ziggurat, AoV=AoV, uncertainty=uncertainty)
