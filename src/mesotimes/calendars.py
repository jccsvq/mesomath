import sqlite3
from pathlib import Path
from importlib.resources import files
from math import floor

import juliandate as jd


def moon_age(jd: float, offset: float = 0.0) -> int:
    """
    Days elapsed since last New Moon

    :param jd: Julian Day
    :type jd: float
    :param offset: Allows adjustment to sunset, previous sunset, etc., defaults to 0.0
    :type offset: float, optional
    :return: Moon age in days
    :rtype: int
    """
    # Verify that jd is in the range of P&P 1971 chronology
    assert jd >= 1492870.5 and jd <= 1748872.5, "Julian Day out of range of P&P 1971 chronology"

    # Lunar Month (according to Five Millenium Cannon of Solar Eclipses)
    M = 29.530598917100200000
    # M^-1
    M_inv = 0.033863180448880300
    moon0 = -83017.290642228700000000
    _ = moon0 + (jd + offset) * M_inv
    moon = _ - floor(_)
    age = M * moon
    return round(age)


class CalendarConverter:
    """
    Central conversion engine. Uses the Julian Date (JD) as a pivot for all transformations.
    """

    @staticmethod
    def to_jd(
        year: int,
        month: int,
        day: int,
        hh: int = 0,
        mm: int = 0,
        ss: int = 0,
        calendar: str = "julian",
    ) -> float:
        """Convert a date to JD.

        :param year: year
        :type year: int
        :param month: month
        :type month: int
        :param day: day
        :type day: int
        :param hh: hours, defaults to 0
        :type hh: int, optional
        :param mm: minutes, defaults to 0
        :type mm: int, optional
        :param ss: seconds, defaults to 0
        :type ss: int, optional
        :param calendar: Type of calendar system, defaults to "julian"
        :type calendar: str, optional
        :raises ValueError: Unsupported calendar
        :return: Julian Day Number JD
        :rtype: float
        """
        if calendar == "julian":
            # P&D usan Juliano Proléptico
            return jd.from_julian(year, month, day, hh, mm, ss)
        elif calendar == "gregorian":
            return jd.from_gregorian(year, month, day, hh, mm, ss)
        else:
            raise ValueError("Unsupported calendar system")

    @staticmethod
    def from_jd(jdate: float, calendar="julian") -> tuple[int, int, int, int, int, int]:
        """Convert JD to a readable date.

        :param jdate: Julian Day Number JD
        :type jdate: float
        :param calendar: Type of calendar system, defaults to "julian"
        :type calendar: str, optional
        :raises ValueError: Unsupported calendar
        :return: year, month, day, hh, mm, ss
        :rtype: tuple[int, int, int, int, int, int]
        """
        if calendar == "julian":
            return jd.to_julian(jdate)
        elif calendar == "gregorian":
            return jd.to_gregorian(jdate)
        else:
            raise ValueError("Unsupported calendar system")

    @staticmethod
    def days_between(date1, date2):
        """Simple utility to compare dates."""
        return abs(date1 - date2)


class BabylonianConverter:
    """
    Central conversion engine. Uses the Julian Date (JD) as a pivot for all transformations.
    """

    def __init__(self, db_filename: str = "mesotimes.sqlite"):
        """Instance creator

        :param db_filename: database filename, defaults to "mesotimes.sqlite"
        :type db_filename: str, optional
        :raises FileNotFoundError: Database not found
        """


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

    def _get_connection(self):
        """Sqlite3 database connector"""
        return sqlite3.connect(self.db_path)

    def to_jd(
        self,
        king_code: str,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> float:
        """
        Convert Babylonian Date to JD.

        :param king_code: King code
        :type king_code: str
        :param year: King yearyear
        :type year: int
        :param month: King month
        :type month: int
        :param day: King day
        :type day: int
        :param hour: hours, defaults to 0
        :type hour: int, optional
        :param minute: minutes, defaults to 0
        :type minute: int, optional
        :param second: seconds, defaults to 0
        :type second: int, optional
        :raises ValueError: Date not found in records
        :return: Julian Day Number JD
        :rtype: float
        """
        query = """
            SELECT jdat00h FROM kingdates 
            WHERE king_code = ? AND king_year = ? AND king_month = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (king_code, int(year), month))
            row = cursor.fetchone()

        if not row:
            raise ValueError(f"Date not found in records: {king_code} {year}-{month}")

        jdat00h = float(row[0])
        fraction = (hour / 24.0) + (minute / 1440.0) + (second / 86400.0)

        # Day 1 is JDat00h, therefore day 'n' is JDat00h + (n-1)
        return jdat00h + (int(day) - 1) + fraction

    def from_jd(self, jd: float) -> dict:
        """
        Convert JD to Babylonian Date.

        :param jd: Julian Day Number
        :type jd: float
        :return: dict with king_code, year, month, day
        :rtype: dict
        """
        # We look for the nearest beginning of the month that is <= to the JD
        query = """
            SELECT king_code, king_year, king_month, JDat00h 
            FROM kingdates 
            WHERE JDat00h <= ? 
            ORDER BY JDat00h DESC LIMIT 1
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (str(jd),))
            row = cursor.fetchone()

        if not row:
            return None  # O lanzar error si el JD está fuera de rango

        king_code, year, month, jdat00h = row

        # We calculate the day (the remainder of the integer part)
        # We use round to avoid floating point precision errors
        day = int(round(jd - float(jdat00h))) + 1

        return {"king_code": king_code, "year": year, "month": month, "day": day}

    def babylonian_to_julian(self, king_code: str, year: int, month: int, day: int)-> str:
        """Convert Babylonian Date to Julian YYYY-MM-DD format.

        :param king_code: King code
        :type king_code: str
        :param year: King year
        :type year: int
        :param month: King month
        :type month: int
        :param day: King day
        :type day: int
        :return: String in YYYY-MM-DD format
        :rtype: str
        """        
        jd_val = self.to_jd(king_code, year, month, day)
        # jd.to_julian returns (y, m, d)
        y, m, d, hh, mm, ss, _ = jd.to_julian(jd_val)
        return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"

    def julian_to_babylonian(self, year: int, month: int, day: int)-> dict:
        """Convert a Julian date (Y, M, D) to Babylonian structure.

        :param year: Julian year
        :type year: int
        :param month: Julian month
        :type month: int
        :param day: Julian day
        :type day: int
        :return: Babylonian date structure
        :rtype: dict
        """        
        jd_val = jd.from_julian(year, month, day)
        return self.from_jd(jd_val)

    def list_kings(self):
        """Print the list of kings and their start date of reign."""
        # We consult the view, ordering by year so that the chronology makes sense
        query = "SELECT king_code, king, jyear, jmonth, jday FROM king_period_start ORDER BY jyear ASC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            kings = cursor.fetchall()

            print(f"{'Code':<10} | {'King Name':<25} | {'Start Date (J)'}")
            print("-" * 60)

            for code, name, year, month, day in kings:
                date_str = f"{year}/{month:02}/{day:02}"
                print(f"{code:<10} | {name:<25} | {date_str}")
