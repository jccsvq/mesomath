"""
`date.py` - Core chronological interface for the mesotimes ecosystem.
"""

from __future__ import annotations

from typing import Any

# Indexed base converters and imports
from juliandate import to_gregorian, to_julian

from mesotimes.almanac import LunarAlmanac
from mesotimes.astronomy.core import delta_t, delta_t_sigma, mesopotamian_cities
from mesotimes.astronomy.moon import (
    calculate_full_moon_na,
    calculate_kur,
    calculate_mi_mush,
    check_neomenia,
)

# Imports of calculation engines (Pure calculation, return data)
from mesotimes.astronomy.sun import (
    bab_day_duration,
    get_season_day_str,
    sun_rise_transit_set,
)
from mesotimes.babday import BabylonianDay
from mesotimes.calendars import BabylonianConverter, CalendarConverter

# Constantes del proyecto
from mesotimes.constants import KING_DICT, MONTH_DICT
from mesotimes.proleptic import ProlepticBabylonianCalendar
from pymeeus.Epoch import Epoch


class ChronDate:
    """Main user-facing chronological anchor.

    Acts as a Facade unifying historical calendars, lunar intervals, and
    planetary phenomena based on a continuous timeline.
    """

    _bab_conv = BabylonianConverter()
    _cal_conv = CalendarConverter()

    # Parker & Dubberstein (1971) operational limits
    MIN_JD: float = 1492870.5
    MAX_JD: float = 1748872.5
    GREGORIAN_REFORM: float = 2299161.5


    def __init__(self, jd: float) -> None:
        """Initializes a ChronDate instance via a Julian Day.

        Args:
            jd (float): Julian Day number (UT).
        """
        self.__jd: float = jd
        self.__is_PD71: bool = self.MIN_JD <= jd <= self.MAX_JD

        # Lazy evaluation cache for civil calendar transformations
        self._cached_civil_date: tuple[int, int, int, str] | None = None

    # --- Factory Constructors ---

    @classmethod
    def from_babylonian(
        cls,
        king_code: str,
        year: int,
        month: float,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> ChronDate:
        """Creates a ChronDate instance from a Babylonian historical date.

        Args:
            king_code (str): Regnal abbreviations matching canonical cuneiform records.
            year (int): Regnal year of the designated king.
            month (float): Month number (intercalary months represented as floats).
            day (int): Day of the Babylonian lunar month (1 to 30).
            hour (int, optional): Hour of the day. Defaults to 0.
            minute (int, optional): Minute of the hour. Defaults to 0.
            second (int, optional): Second of the minute. Defaults to 0.

        Returns:
            ChronDate: An initialized instance anchored to the calculated Julian Day.
        """
        jd = cls._bab_conv.to_jd(king_code, year, month, day, hour, minute, second)
        return cls(jd)

    @classmethod
    def from_julian(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> ChronDate:
        """Creates a ChronDate instance from a Proleptic Julian calendar date.

        Args:
            year (int): Astronomical year (negative for BCE dates).
            month (int): Month index (1 to 12).
            day (int): Civil day number.
            hour (int, optional): Hour of the day. Defaults to 0.
            minute (int, optional): Minute of the hour. Defaults to 0.
            second (int, optional): Second of the minute. Defaults to 0.

        Returns:
            ChronDate: An initialized instance anchored to the calculated Julian Day.
        """
        jd = cls._cal_conv.to_jd(
            year, month, day, hour, minute, second, calendar="julian"
        )
        return cls(jd)

    @classmethod
    def from_gregorian(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> ChronDate:
        """Creates a ChronDate instance from a Proleptic Gregorian calendar date.

        Args:
            year (int): Astronomical year (negative for BCE dates).
            month (int): Month index (1 to 12).
            day (int): Civil day number.
            hour (int, optional): Hour of the day. Defaults to 0.
            minute (int, optional): Minute of the hour. Defaults to 0.
            second (int, optional): Second of the minute. Defaults to 0.

        Returns:
            ChronDate: An initialized instance anchored to the calculated Julian Day.
        """
        jd = cls._cal_conv.to_jd(
            year, month, day, hour, minute, second, calendar="gregorian"
        )
        return cls(jd)

    # --------------------------------------------------------

    @classmethod
    def kings(cls) -> list[str]:
        """Lists King codes, names and period start date."""
        return cls._bab_conv.list_kings()


    # --- Calendar Properties & Cache Management ---

    @property
    def jd(self) -> float:
        """Returns the core astronomical Julian Day (UT)."""
        return self.__jd

    @property
    def is_babylonian(self) -> bool:
        """Checks if the Julian Day falls within the reliable historical constraints of P&D (1971)."""
        return self.__is_PD71

    @property
    def _civil_components(self) -> tuple[int, int, int, str]:
        """Calculates, caches, and returns standard civil calendar components.

        Differentiates between Proleptic Julian and Gregorian timelines using
        the canonical Gregorian Reform threshold.
        """
        if self._cached_civil_date is None:
            if self.__jd < self.GREGORIAN_REFORM:
                y, m, d, _, _, _, _ = to_julian(self.__jd)
                self._cached_civil_date = (int(y), int(m), int(d), "Julian")
            else:
                y, m, d, _, _, _, _ = to_gregorian(self.__jd)
                self._cached_civil_date = (int(y), int(m), int(d), "Gregorian")
        return self._cached_civil_date

    @property
    def julian(self) -> tuple[int, int, int]:
        """Returns the date in the Proleptic Julian Calendar as a (Year, Month, Day) tuple."""
        return self._cal_conv.from_jd(self.__jd, calendar="julian")

    @property
    def gregorian(self) -> tuple[int, int, int]:
        """Returns the date in the Proleptic Gregorian Calendar as a (Year, Month, Day) tuple."""
        return self._cal_conv.from_jd(self.__jd, calendar="gregorian")

    @property
    def babylonian_data(self) -> dict[str, Any]:
        """Algorithmic property that resolves the current Julian Day into raw Babylonian calendar structures.

        Falls back to a structural Proleptic Babylonian Calendar algorithm
        if the date overflows historical table boundaries.
        """
        if self.__is_PD71:
            return self._bab_conv.from_jd(self.__jd)
        else:
            pbc = ProlepticBabylonianCalendar(self._civil_components[0])
            return pbc.convert_to_babylonian(self.__jd)

    @property
    def babylonian(self) -> str:
        """Formats and wraps Babylonian calendar parameters into a readable string for REPL inspection."""
        data = self.babylonian_data
        if self.__is_PD71:
            king = KING_DICT.get(data["king_code"], "Unknown King")
            m_str = MONTH_DICT.get(str(data["month"]), "Unknown")
            return f"Year {data['year']} of {king}, month: {data['month']} ({m_str}), day: {data['day']}"
        else:
            return (
                f"Year {self._civil_components[0]} of Proleptic Babylonian Calendar, "
                f"month: {data['month_name']}, day: {data['day']}"
            )

    @property
    def season_day(self):
        """Returns a string indicating the current day within the season."""

        return get_season_day_str(
            self._civil_components[0],
            self._civil_components[1],
            self._civil_components[2],
        )

    @property
    def context(self):
        """Print historical context for this date."""
        if self.__is_PD71:
            contexts = self._get_context()
            for ctx in contexts:
                print(
                    f"({ctx['category']}): Year {ctx['rel_year']} of {ctx['name']} ({ctx['description']}))"
                )
        else:
            print("No historical context available for proleptic dates.")


    # =========================================================================
    # ALGORITHMIC METHODS (Returns pure data objects / dictionaries)
    # =========================================================================

    def _get_context(self):
        """Get historical context for this date from database

        :return: Database matches.
        :rtype: iterable
        """
        query = """
        SELECT name, category, (?-start_year+1) as rel_year, description
        FROM periods 
        WHERE ? BETWEEN start_year AND end_year
        """
        year = self._civil_components[0]
        with self._bab_conv._get_connection() as conn:
            # This makes the rows dictionaries: {'name': '...', 'category': '...'}
            conn.row_factory = lambda cursor, row: {
                "name": row[0],
                "category": row[1],
                "rel_year": row[2],
                "description": row[3],
            }
            cursor = conn.cursor()
            cursor.execute(query, (year, year))
            return cursor.fetchall()


    def get_lunar_intervals(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, float]:
        """Calculates and returns the classical Neo-Babylonian lunar intervals for the lunation.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, float]: Dictionary containing:
                - 'na': Time between sunset and moonset after New Moon (or vice versa at Full Moon).
                - 'mi_mush': Lunar visibility interval during the night.
                - 'kur': Time between moonrise and sunrise before conjunction.
        """
        y, m, d, _ = self._civil_components
        return {
            "na": calculate_full_moon_na(y, m, d, city, ziggurat),
            "mi_mush": calculate_mi_mush(y, m, d, city, ziggurat)[0],
            "kur": calculate_kur(y, m, d, city, ziggurat)[0],
        }

    def get_planetary_events(self) -> dict[str, dict[str, Any]]:
        """Finds the chronologically closest oppositions, stations, and elongations for the 5 classical planets.

        Returns:
            dict[str, dict[str, Any]]: Structured dict mapped by planet names containing event description and Julian Day.
        """
        from mesotimes.astronomy.planets.inferiors import (
            MesopotamianMercury,
            MesopotamianVenus,
        )
        from mesotimes.astronomy.planets.superiors import (
            MesopotamianJupiter,
            MesopotamianMars,
            MesopotamianSaturn,
        )

        epoch = Epoch(self.jd, utc=True)
        events: dict[str, dict[str, Any]] = {}

        # Mapping unifications from the underlying core planetary engine
        planets = {
            "Mars": MesopotamianMars(),
            "Jupiter": MesopotamianJupiter(),
            "Saturn": MesopotamianSaturn(),
            "Venus": MesopotamianVenus(),
            "Mercury": MesopotamianMercury(),
        }

        # Superior planets geometric opposition lookup loop
        for name in ["Mars", "Jupiter", "Saturn"]:
            try:
                opp_epoch = planets[name].get_opposition(epoch)
                events[name] = {"event": "Opposition", "jd": opp_epoch.jd()}
            except Exception:
                # Catching localized iterative search convergence failures within PyMeeus
                events[name] = {"event": "No visible opposition in window", "jd": None}

        return events

    def get_sun_data(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, float]:
        """Computes exact solar ephemerides in Universal Time (UT) for the instance date.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, float]: Dictionary containing 'sunrise_ut', 'transit_ut', and 'sunset_ut' as float days.
        """
        y, m, d, _ = self._civil_components
        rise_ut, transit_ut, set_ut, _, _, _ = sun_rise_transit_set(
            y, m, d, city, ziggurat
        )
        return {"sunrise_ut": rise_ut, "transit_ut": transit_ut, "sunset_ut": set_ut}

    def get_bab_day_data(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, float]:
        """Computes exact durations and boundaries of the Babylonian civil day (sunset-to-sunset).

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, float]: Dictionary containing complete diurnal/nocturnal breakdowns:
                - 'duration': Total length of the local civil day.
                - 'diurnal': Length of daylight interval.
                - 'nocturnal': Length of nighttime interval.
                - 'start_previous_sunset_ut': UT epoch marking the true start of the Babylonian day.
                - 'sunrise_ut': Middle daylight transition.
                - 'transit_ut': Solar culmination.
                - 'end_sunset_ut': UT epoch closing the current Babylonian day.
        """
        duration, diurnal, nocturnal, set1, rise2, transit2, set2 = bab_day_duration(
            self.jd, city, ziggurat
        )
        return {
            "duration": duration,
            "diurnal": diurnal,
            "nocturnal": nocturnal,
            "start_previous_sunset_ut": set1,
            "sunrise_ut": rise2,
            "transit_ut": transit2,
            "end_sunset_ut": set2,
        }

    def get_lunar_horizon_data(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, float]:
        """Computes the exact decimal Universal Time (UT) hours for lunar horizon events.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, float]: Dictionary containing 'moonrise_ut', 'transit_ut', and 'moonset_ut'.
        """
        from mesotimes.astronomy.moon import moon_rise_transit_set as mrts

        y, m, d, _ = self._civil_components
        ut_rise, ut_transit, ut_set, _, _, _ = mrts(y, m, d, city, ziggurat)
        return {"moonrise_ut": ut_rise, "transit_ut": ut_transit, "moonset_ut": ut_set}

    def get_mi_mush_data(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, Any]:
        """Computes the MI-MUSH lunar interval in both standard minutes and Babylonian UŠ units.

        MI-MUSH defines the duration of simultaneous visibility of the Sun and Moon
        on the night of the full moon.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, Any]: Calculated parameters including intervals, raw UT times, and visibility flags.
                - 'interval_minutes' (float): Visibility time in minutes.
                - 'interval_ush' (float): Visibility time in UŠ (1 UŠ = 4 minutes).
                - 'visible_simultaneously' (bool): True if structural overlapping occurs.
        """
        y, m, d, _ = self._civil_components
        mi_mush_min, moon_set_ut, sun_rise_ut = calculate_mi_mush(
            y, m, d, city, ziggurat
        )
        return {
            "interval_minutes": mi_mush_min,
            "interval_ush": mi_mush_min / 4.0,
            "moon_set_ut": moon_set_ut,
            "sun_rise_ut": sun_rise_ut,
            "visible_simultaneously": mi_mush_min > 0,
        }

    def get_kur_data(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, Any]:
        """Computes the KUR lunar interval for the last visible wane before conjunction.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, Any]: Calculated parameters including visibility thresholds.
                - 'status' (str): Evaluated atmospheric visibility ('VISIBLE', 'CRITICAL', 'INVISIBLE').
        """
        y, m, d, _ = self._civil_components
        kur_min, moon_rise_ut, sun_rise_ut = calculate_kur(y, m, d, city, ziggurat)

        if kur_min < 0:
            status = "INVISIBLE"
        elif kur_min < 48.0:
            status = "CRITICAL"
        else:
            status = "VISIBLE"

        return {
            "interval_minutes": kur_min,
            "interval_ush": kur_min / 4.0,
            "moon_rise_ut": moon_rise_ut,
            "sun_rise_ut": sun_rise_ut,
            "status": status,
        }

    def get_day_planetary_visibility(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> dict[str, dict[str, Any]]:
        """Evaluates true heliacal visibility statuses for the 5 classical planets.

        Checks geometric altitude against empirical Babylonian Arcs of Vision
        both at local astronomical dawn (Morning Star) and dusk (Evening Star).

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.

        Returns:
            dict[str, dict[str, Any]]: Nested map of planetary visibility flags and vision constraints.
        """
        from mesotimes.astronomy.planets.inferiors import (
            MesopotamianMercury,
            MesopotamianVenus,
        )
        from mesotimes.astronomy.planets.superiors import (
            MesopotamianJupiter,
            MesopotamianMars,
            MesopotamianSaturn,
        )

        y, m, d, _ = self._civil_components
        sun = self.get_sun_data(city, ziggurat)

        # Build precise local twilight Epochs anchoring the observation window
        epoch_dawn = Epoch(
            int(y), int(m), int(d) + (sun["sunrise_ut"] / 24.0), utc=True
        )
        epoch_dusk = Epoch(int(y), int(m), int(d) + (sun["sunset_ut"] / 24.0), utc=True)

        planets = [
            MesopotamianMercury(),
            MesopotamianVenus(),
            MesopotamianMars(),
            MesopotamianJupiter(),
            MesopotamianSaturn(),
        ]
        visibility_report: dict[str, dict[str, Any]] = {}

        for p in planets:
            visible_dawn = p.is_visible_at_twilight(
                epoch_dawn, city=city, ziggurat=ziggurat
            )
            visible_dusk = p.is_visible_at_twilight(
                epoch_dusk, city=city, ziggurat=ziggurat
            )

            visibility_report[p.name] = {
                "arc_of_vision": p.arc_of_vision,
                "visible_at_dawn": visible_dawn,
                "visible_at_dusk": visible_dusk,
            }

        return visibility_report

    def get_year_planetary_events(self) -> dict[str, dict[str, Any]]:
        """Calculates major orbital phenomena (Oppositions, Stations, Conjunctions) for the current year.

        Uses an intermediate mid-year search anchor to feed underlying numerical solvers.

        Returns:
            dict[str, dict[str, Any]]: Structural map containing raw PyMeeus Epoch instances (Terrestrial Time, TT).
        """
        from mesotimes.astronomy.planets.inferiors import (
            MesopotamianMercury,
            MesopotamianVenus,
        )
        from mesotimes.astronomy.planets.superiors import (
            MesopotamianJupiter,
            MesopotamianMars,
            MesopotamianSaturn,
        )

        y = self._civil_components[0]
        # Mid-year standard pivot epoch for bounded root-finding algorithms
        mid_year_epoch = Epoch(y, 6, 15.0, utc=True)

        superiors = {
            "Mars": MesopotamianMars(),
            "Jupiter": MesopotamianJupiter(),
            "Saturn": MesopotamianSaturn(),
        }
        inferiors = {"Venus": MesopotamianVenus(), "Mercury": MesopotamianMercury()}

        events: dict[str, dict[str, Any]] = {}

        # Superior Planets: Oppositions and Retrograde Stations
        for name, p in superiors.items():
            try:
                opp_epoch = p.get_opposition(mid_year_epoch)
                st1_epoch = p.get_station_longitude_1(mid_year_epoch)
                events[name] = {
                    "opposition_epoch": opp_epoch,
                    "station_1_epoch": st1_epoch,
                }
            except Exception:
                # Catching lack of seasonal occurrence within the designated window
                events[name] = {"opposition_epoch": None, "station_1_epoch": None}

        # Inferior Planets: Inferior Conjunctions
        for name, p in inferiors.items():
            try:
                inf_conj = p.get_inferior_conjunction(mid_year_epoch)
                events[name] = {"inferior_conjunction_epoch": inf_conj}
            except Exception:
                events[name] = {"inferior_conjunction_epoch": None}

        return events

    def get_year_eclipses(self) -> list[dict[str, Any]]:
        """Queries the internal historical database to retrieve all recorded eclipses

        visible from the Kish station during the current Julian year.

        Returns:
            list[dict[str, Any]]: A list of dictionaries containing:
                - 'year' (int): Historical Julian year.
                - 'month' (int): Civil month.
                - 'day' (int): Civil day.
                - 'type' (str): Eclipse nature ('SOLAR', 'LUNAR').
                - 'magnitude' (float): Calculated astronomical magnitude.
        """
        jyear = self._civil_components[0]
        query = """SELECT * FROM kishecl WHERE year = ? ORDER BY month, day;"""

        with self._bab_conv._get_connection() as conn:
            conn.row_factory = lambda cursor, row: {
                "year": row[0],
                "month": row[1],
                "day": row[2],
                "type": row[3],
                "magnitude": row[4],
            }
            cursor = conn.cursor()
            cursor.execute(query, (jyear,))
            return cursor.fetchall()

    def get_year_delta_t_data(self) -> dict[str, Any]:
        """Computes Delta T (ΔT) and its standard error (sigma) for the current year.

        Extrapolates the respective structural shifts in geographical longitude
        (angular arc drift due to Earth's rotational deceleration).

        Returns:
            dict[str, Any]: Ephemeris correction metrics containing:
                - 'delta_t_seconds' (float): Total temporal discrepancy.
                - 'delta_t_str' (str): Formatted ISO timedelta string representation.
                - 'delta_t_lon' (tuple): Resulting spatial shift in (Degrees, Minutes, Seconds) of arc.
                - 'sigma_seconds' (float | None): Uncertainty bounds if within valid matrices.
        """
        import datetime

        jyear = self._civil_components[0]

        dt = delta_t(jyear)
        dt_timedelta = datetime.timedelta(seconds=abs(dt))
        # Preserving original arithmetic sign for string representation if ΔT is negative
        dt_str = f"-{dt_timedelta}" if dt < 0 else str(dt_timedelta)
        dt_lon = self._dt2lon(dt)

        report: dict[str, Any] = {
            "delta_t_seconds": dt,
            "delta_t_str": dt_str,
            "delta_t_lon": dt_lon,
            "sigma_seconds": None,
            "sigma_str": "--",
            "sigma_lon": None,
        }

        try:
            dts = delta_t_sigma(jyear)
            dts_timedelta = datetime.timedelta(seconds=dts)
            report["sigma_seconds"] = dts
            report["sigma_str"] = str(dts_timedelta)
            report["sigma_lon"] = self._dt2lon(dts)
        except ValueError:
            # Captures out-of-bounds historical epochs lacking secure uncertainty matrices
            pass

        return report

    @staticmethod
    def sites(cities_dict: dict = mesopotamian_cities) -> None:
        """
        Prints a formatted, scannable table of Mesopotamian observatories
        and their geographical coordinates.

        :param cities_dict: Dictionary containing city metadata and coordinates.
        :type cities_dict: dict
        """
        # Header definition with fixed-width columns for CLI alignment
        print("\n" + "=" * 90)
        print(f"{'MESOPOTAMIAN OBSERVATORIES & SITES':^90}")
        print("=" * 90)

        # Table Header
        header = f"{'City':<12} | {'Latitude':<9} | {'Longitude':<9} | {'Elevation':<9} | {'Modern Location / Description'}"
        print(header)
        print("-" * 90)

        # Iterate and format each city record
        for city, data in cities_dict.items():
            # Format latitude (N) and longitude (E) strings
            lat_str = f"{data['latitude']:>7.4f}°N"
            lon_str = f"{data['longitude']:>7.4f}°E"
            alt_str = f"{data['altitude']:>4} m"

            # Main line with coordinates
            print(
                f"{city:<12} | {lat_str:<9} | {lon_str:<9} | {alt_str:<9} | {data['modern_name']}"
            )
            # Sub-line with historical description for extra context without text wrapping issues
            print(
                f"{'':<12} | {'':<9} | {'':<9} | {'':<9} | \033[3m{data['description']}\033[0m"
            )
            print("-" * 90)



    @staticmethod
    def _dt2lon(seconds: float) -> tuple[float, float, float]:
        """Helper to map clock seconds into angular degrees, minutes, and seconds of arc.

        1 temporal second equals 15 seconds of arc (360° / 24h = 15°/h = 15'/min = 15"/s).
        """
        total_arc_seconds = abs(seconds) * 15.0
        degrees = total_arc_seconds // 3600
        remainder = total_arc_seconds % 3600
        minutes = remainder // 60
        secs = remainder % 60
        return degrees, minutes, secs

    def get_julian_month_phases(self) -> list[dict[str, Any]]:
        """Calculates exact lunar phases falling within the current civil month.

        Implements a continuous dynamic grid sweep to eliminate boundary blind spots
        caused by timezone transitions and delta T shifts.

        Returns:
            list[dict[str, Any]]: Cronologically sorted dictionaries detailing phase names,
                underlying PyMeeus UT Epochs, and formatted date strings.
        """
        from pymeeus.Epoch import Epoch
        from pymeeus.Moon import Moon

        y, m, _, _ = self._civil_components

        phase_types = ["new", "first", "full", "last"]
        phase_names = {
            "new": "New Moon",
            "first": "First Quarter",
            "full": "Full Moon",
            "last": "Last Quarter",
        }

        phases_in_month = []
        processed_jds: set[float] = set()

        # 1. Establish a central anchor on the 15th day of the target month
        mid_month = Epoch(y, m, 15, utc=True)
        jd_start = mid_month()

        # 2. Continuous 42-day sweep grid to safely bridge lunation step scales
        search_offsets = [-21, -14, -7, 0, 7, 14, 21]

        for offset in search_offsets:
            anchor_epoch = Epoch(jd_start + offset, utc=True)

            for target in phase_types:
                try:
                    res_epoch = Moon.moon_phase(anchor_epoch, target=target)

                    if res_epoch is not None:
                        jd_rounded = round(res_epoch(), 4)

                        if jd_rounded not in processed_jds:
                            # Apply Delta T correction to recover precise Universal Time (UT)
                            y_t, m_t, _ = res_epoch.get_date()
                            jd_ut = res_epoch() - (delta_t(y_t, m_t) / 86400.0)
                            ep_ut = Epoch(jd_ut, utc=True)

                            y_ut, m_ut, d_ut = ep_ut.get_date()

                            # Strict filter: corrected UT phase must belong to the active month scope
                            if int(y_ut) == y and int(m_ut) == m:
                                processed_jds.add(jd_rounded)
                                phases_in_month.append(
                                    {
                                        "phase": phase_names[target],
                                        "epoch_ut": ep_ut,
                                        "date_str": f"{int(y_ut):04d}-{int(m_ut):02d}-{d_ut:05.2f}",
                                    }
                                )
                except Exception:
                    continue

        phases_in_month.sort(key=lambda x: x["epoch_ut"]())
        return phases_in_month

    def get_babylonian_month_data(
        self,
        city: str = "Babylon",
        ziggurat: float = 0.0,
        db_filename: str = "mesotimes.sqlite",
        AoV: float = 12.0,
        uncertainty: float = 0.833,
    ) -> LunarAlmanac:
        """Initializes and synchronizes a LunarAlmanac instance for the current civil month.

        Applies an automated algorithmic epoch advancement check if the localized
        first crescent visibility (neomenia) has drifted into adjacent lunations.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
            db_filename (str, optional): SQLite database filename path. Defaults to "mesotimes.sqlite".
            AoV (float, optional): Empirical Arc of Vision in degrees for neomenia. Defaults to 12.0.
            uncertainty (float, optional): Marginal visibility filtering factor. Defaults to 0.833.

        Returns:
            LunarAlmanac: A fully scanned and synchronized lunar almanac instance.
        """
        from mesotimes.almanac import LunarAlmanac

        b_year = self._civil_components[0]
        b_month = self._civil_components[1]

        # 1. Initial lookup pivot
        alm = LunarAlmanac(
            b_year,
            b_month,
            city=city,
            ziggurat=ziggurat,
            db_filename=db_filename,
            AoV=AoV,
            uncertainty=uncertainty,
        )
        alm.scan_month()

        # 2. Heuristic lunation boundary offset control
        if alm.data.get("na") is not None:
            tab_date_str = alm.data["na"][0]
            try:
                parts = tab_date_str.strip().split("/")
                tab_month = int(parts[1])

                # Force synchronization forward if almanac anchors on previous historical lunation
                if tab_month < b_month and self._civil_components[2] <= 5:
                    b_month += 1
                    if b_month > 12:
                        b_month = 1
                        b_year += 1
                    alm = LunarAlmanac(
                        b_year,
                        b_month,
                        city=city,
                        ziggurat=ziggurat,
                        db_filename=db_filename,
                        AoV=AoV,
                        uncertainty=uncertainty,
                    )
                    alm.scan_month()
            except (ValueError, IndexError):
                pass

        return alm

    def bab_day_instance(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> BabylonianDay:
        """Instantiates a localized BabylonianDay framework matching this instance's Julian Day.

        Args:
            city (str, optional): Ancient observation site registry name. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above terrain in meters. Defaults to 0.0.

        Returns:
            BabylonianDay: A localized day metrics framework mapping sunset-to-sunset boundaries.
        """
        return BabylonianDay(self.jd, city, ziggurat, title=self.babylonian)

    # =========================================================================
    # INFORMATIVE METHODS / REPORTS (Interactive REPL User Interfaces)
    # =========================================================================

    def day_ephemeris(self, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Prints a comprehensive astronomical profile for the local Mesopotamian sky.

        Outputs solar context, lunar intervals, and twilight planetary visibilities
        for this specific Julian Day to the standard output.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
        """
        y, m, d, calendar = self._civil_components
        sun = self.get_sun_data(city, ziggurat)
        lunar_intervals = self.get_lunar_intervals(city, ziggurat)
        planets_vis = self.get_day_planetary_visibility(city, ziggurat)

        print("\n" + "=" * 65)
        print(f"{f'MESOPOTAMIAN DAILY EPHEMERIS: {city.upper()}':^65}")
        print("=" * 65)
        print(
            f"  Julian Day:  {self.jd:<15} | Civil Calendar: {calendar} ({y}/{m}/{d})"
        )
        print(f"  Chronology:  {self.babylonian}")
        print("-" * 65)
        print("  SOLAR CONTEXT:")
        print(
            f"    Sunrise : {self._format_hours(sun['sunrise_ut'])} UT | Sunset : {self._format_hours(sun['sunset_ut'])} UT"
        )
        print(
            f"    Transit : {self._format_hours(sun['transit_ut'])} UT | Season : {get_season_day_str(y, m, d, calendar.lower())}"
        )
        print("-" * 65)
        print("  LUNAR INTERVALS (Phenomena in current lunation):")
        print(
            f"    [Neomenia] NA Interval: {lunar_intervals['na']:.2f} min (Time from Sunset to Moonset)"
        )
        print(
            f"    [Mid-Month] MI-MUSH:    {lunar_intervals['mi_mush']:.2f} min (Simultaneous visibility)"
        )
        print(
            f"    [End-Month] KUR:        {lunar_intervals['kur']:.2f} min (Dawn crescent disappearance)"
        )
        print("-" * 65)
        print("  PLANETARY VISIBILITY ( Twilight vs. Arc of Vision ):")

        for name, data in planets_vis.items():
            # ANSI colored terminal escapes for dynamic interaction states
            dawn_str = (
                "\033[92mVISIBLE (Morning Star)\033[0m"
                if data["visible_at_dawn"]
                else "Invisible"
            )
            dusk_str = (
                "\033[94mVISIBLE (Evening Star)\033[0m"
                if data["visible_at_dusk"]
                else "Invisible"
            )

            if data["visible_at_dawn"]:
                status = dawn_str
            elif data["visible_at_dusk"]:
                status = dusk_str
            else:
                status = "Invisible / Glare"

            print(
                f"    * {name:<10} -> {status:<35} (Required Av: {data['arc_of_vision']}°)"
            )
        print("=" * 65 + "\n")

    def year_almanac(self, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Assembles and prints global solstices, equinoxes, planetary nodes, and annual eclipses.

        Preceded by a critical diagnosis of Earth's rotational deceleration parameter Delta T (ΔT).

        Args:
            city (str, optional): Ancient observation site registry name. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above terrain in meters. Defaults to 0.0.
        """
        from mesotimes.astronomy.sun import (
            autumnal_equinox,
            summer_solstice,
            vernal_equinox,
            winter_solstice,
        )

        y = self._civil_components[0]
        dt_data = self.get_year_delta_t_data()
        p_events = self.get_year_planetary_events()
        eclipses = self.get_year_eclipses()

        print("\n" + "=" * 65)
        print(f"{f'BABYLONIAN YEAR ALMANAC FOR YEAR {y}':^65}")
        print("=" * 65)

        print("  CHRONOLOGICAL ROOT & EARTH ROTATION CONTEXT:")
        print(
            f"    Delta T (ΔT) approx. : {dt_data['delta_t_seconds']:.2f} seconds ({dt_data['delta_t_str']})"
        )

        d_lon = dt_data["delta_t_lon"]
        print(
            f"    Longitude Shift      : {round(d_lon[0])}° {round(d_lon[1])}' {round(d_lon[2])}\""
        )

        if dt_data["sigma_seconds"] is not None:
            s_lon = dt_data["sigma_lon"]
            print(
                f"    Uncertainty (σ)      : {dt_data['sigma_seconds']:.2f} seconds ({dt_data['sigma_str']})"
            )
            print(
                f"    Uncertainty in Arc   : {round(s_lon[0])}° {round(s_lon[1])}' {round(s_lon[2])}\""
            )
        else:
            print("    Uncertainty (σ)      : -- (Out of bounds)")
        print("-" * 65)

        def _epoch_to_string(epoch: Epoch | None) -> str:
            """Formats a PyMeeus Epoch instance into a standardized uniform civil date string."""
            if epoch is None:
                return "N/A"
            y_civil, m_civil, d_civil = epoch.get_date()
            return f"{int(y_civil):04d}-{int(m_civil):02d}-{d_civil:05.2f}"

        # 1. Cardinal Solar Points
        print("  CARDINAL SOLAR POINTS:")
        print(
            f"    Vernal Equinox   : {_epoch_to_string(Epoch(vernal_equinox(y), utc=True))}"
        )
        print(
            f"    Summer Solstice  : {_epoch_to_string(Epoch(summer_solstice(y), utc=True))}"
        )
        print(
            f"    Autumnal Equinox : {_epoch_to_string(Epoch(autumnal_equinox(y), utc=True))}"
        )
        print(
            f"    Winter Solstice  : {_epoch_to_string(Epoch(winter_solstice(y), utc=True))}"
        )
        print("-" * 65)

        # 2. Critical Planetary Phenomena (Sarsu - UT Clock)
        print("  CRITICAL PLANETARY PHENOMENA (Sarsu - UT Clock):")
        for name, data in p_events.items():
            if "opposition_epoch" in data:
                ep_opp = data["opposition_epoch"]
                ep_st1 = data["station_1_epoch"]
                opp_ut_str, st1_ut_str = "N/A", "N/A"

                if ep_opp is not None:
                    jd_opp_ut = ep_opp() - (
                        delta_t(ep_opp.get_date()[0], ep_opp.get_date()[1]) / 86400.0
                    )
                    opp_ut_str = _epoch_to_string(Epoch(jd_opp_ut, utc=True))
                if ep_st1 is not None:
                    jd_st1_ut = ep_st1() - (
                        delta_t(ep_st1.get_date()[0], ep_st1.get_date()[1]) / 86400.0
                    )
                    st1_ut_str = _epoch_to_string(Epoch(jd_st1_ut, utc=True))

                print(
                    f"    * {name:<8} Opposition: {opp_ut_str} | Station 1: {st1_ut_str}"
                )

            elif "inferior_conjunction_epoch" in data:
                ep_conj = data["inferior_conjunction_epoch"]
                conj_ut_str = "N/A"
                if ep_conj is not None:
                    jd_conj_ut = ep_conj() - (
                        delta_t(ep_conj.get_date()[0], ep_conj.get_date()[1]) / 86400.0
                    )
                    conj_ut_str = _epoch_to_string(Epoch(jd_conj_ut, utc=True))

                print(f"    * {name:<8} Inf. Conj. : {conj_ut_str}")
        print("-" * 65)

        # 3. Historical Eclipse Database Catalogue
        print("  ECLIPSES VISIBLE FROM KISH (Historical Database):")
        if len(eclipses) > 0:
            for eco in eclipses:
                print(
                    f"    * Date: {y:04d}-{eco['month']:02d}-{eco['day']:02d} | "
                    f"Type: {eco['type']:<7} | Observed Mag: {eco['magnitude']}"
                )
        else:
            print("    * No eclipses registered/visible for this year context.")
        print("=" * 65 + "\n")

    def month_almanac(
        self,
        city: str = "Babylon",
        ziggurat: float = 0.0,
        db_filename: str = "mesotimes.sqlite",
        AoV: float = 12.0,
        uncertainty: float = 0.833,
        full: bool = False,
    ) -> None:
        """Prints a structured analytical summary of lunar phases for the current civil month.

        Triggers an automated virtual tablet matrix reconstruction on the terminal.

        Args:
            city (str, optional): Target ancient observation city. Defaults to "Babylon".
            ziggurat (float, optional): Observer height in meters. Defaults to 0.0.
            db_filename (str, optional): Internal SQLite filename database. Defaults to "mesotimes.sqlite".
            AoV (float, optional): Empirical Arc of Vision constraint. Defaults to 12.0.
            uncertainty (float, optional): Marginal parsing threshold index. Defaults to 0.833.
            full (bool, optional): If True, dumps raw sequential lunar phase steps. Defaults to False.
        """
        y, m, _, calendar = self._civil_components
        phases = self.get_julian_month_phases()

        if full:
            print("\n" + "=" * 55)
            print(f"{f'LUNAR PHASES FOR {calendar.upper()} MONTH: {m}/{y}':^55}")
            print("=" * 55)

            if phases:
                for p in phases:
                    print(f"    * {p['date_str']} -> {p['phase']}")
            else:
                print("    No phases found for this specific month matrix.")
            print("=" * 55 + "\n")

        print("\nLaunching tablet reconstruction for Babylonian month context...")

        # Recover synchronized almanac context pipeline
        alm = self.get_babylonian_month_data(
            city=city,
            ziggurat=ziggurat,
            db_filename=db_filename,
            AoV=AoV,
            uncertainty=uncertainty,
        )

        # Execute cuneiform tablet layout rendering stream
        alm.to_tablet()

    def lunar_info(
        self,
        city: str = "Babylon",
        ziggurat: float = 0.0,
        AoV: float = 12.0,
        uncertainty: float = 0.833,
    ) -> None:
        """Generates a monthly analytical report structured as a Babylonian cuneiform tablet.

        Args:
            city (str, optional): Target ancient observation city. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
            AoV (float, optional): Empirical Arc of Vision constraint. Defaults to 12.0.
            uncertainty (float, optional): Marginal visibility filtering factor. Defaults to 0.833.
        """
        alm = self.get_babylonian_month_data(
            city=city, ziggurat=ziggurat, AoV=AoV, uncertainty=uncertainty
        )
        alm.to_tablet()

    def sun_rise_transit_set(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> None:
        """Prints the specific solar transit metrics alongside the three ancient Night Watches.

        Calculates the exact temporal division for the maṣṣarātu based on fluid
        nocturnal arcs.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
        """
        y, m, d, calendar = self._civil_components
        sun = self.get_sun_data(city, ziggurat)

        # Retrieve structural station altitude
        alt_base = mesopotamian_cities[city]["altitude"] + ziggurat

        print("\n--- Sunrise, Transit and Sunset ---")
        print(f"  City: {city} at {alt_base:.1f} meters above sea level")
        print(f"  Date    ({calendar}): {y}/{m}/{d}")
        print(f"  Chronology: {self.babylonian}")
        print(
            f"  UT Time: Sunrise {self._format_hours(sun['sunrise_ut'])}, "
            f"Transit {self._format_hours(sun['transit_ut'])}, "
            f"Sunset {self._format_hours(sun['sunset_ut'])}"
        )

        # --- Algorithmic Calculation of Night Watches (Maṣṣartu) ---
        if sun["sunrise_ut"] < sun["sunset_ut"]:
            night_duration = (sun["sunrise_ut"] + 24.0) - sun["sunset_ut"]
        else:
            night_duration = sun["sunrise_ut"] - sun["sunset_ut"]

        watch_length = night_duration / 3.0

        w1_start = sun["sunset_ut"]
        w1_end = (sun["sunset_ut"] + watch_length) % 24
        w2_end = (sun["sunset_ut"] + 2 * watch_length) % 24
        w3_end = sun["sunrise_ut"]

        print("\n--- Night Watches (maṣṣarātu) ---")
        print(
            f"  Total Night Duration: {self._format_hours(night_duration)} hours "
            f"(Each watch: {self._format_hours(watch_length)})"
        )
        print(
            f"    1st Watch (rēštītu):    {self._format_hours(w1_start)} to {self._format_hours(w1_end)}"
        )
        print(
            f"    Middle Watch (qablītu): {self._format_hours(w1_end)} to {self._format_hours(w2_end)}"
        )
        print(
            f"    Last Watch (namārītu):  {self._format_hours(w2_end)} to {self._format_hours(w3_end)}"
        )

    def bab_day_info(self, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Prints a comprehensive dashboard for the localized sunset-to-sunset Babylonian day.

        Args:
            city (str, optional): Target ancient observation city. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above terrain in meters. Defaults to 0.0.
        """
        bd = self.get_bab_day_data(city, ziggurat)

        print(f"\nBabylonian day in {city}")
        print(self.babylonian)
        print(self.season_day)
        print(f"{'=' * 60}")
        print(f"Babylonian day duration: {self._format_hours(bd['duration'])}")
        print(f"        Diurnal duration: {self._format_hours(bd['diurnal'])}")
        print(f"      Nocturnal duration: {self._format_hours(bd['nocturnal'])}")
        print(
            f"   Start (previous day): {self._format_hours(bd['start_previous_sunset_ut'])} (UT)"
        )
        print(f"                Sunrise: {self._format_hours(bd['sunrise_ut'])} (UT)")
        print(f"                Transit: {self._format_hours(bd['transit_ut'])} (UT)")
        print(
            f"                    End: {self._format_hours(bd['end_sunset_ut'])} (UT)"
        )

    def moon_rise_transit_set(
        self, city: str = "Babylon", ziggurat: float = 0.0
    ) -> None:
        """Dumps local lunar horizon ephemerides directly to the REPL pipeline.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
        """
        y, m, d, calendar = self._civil_components
        lunar = self.get_lunar_horizon_data(city, ziggurat)
        alt_base = mesopotamian_cities[city]["altitude"] + ziggurat

        print("\n--- Lunar Horizon & Meridian Events ---")
        print(
            f"  Site: {city} ({alt_base:.1f} m.a.s.l.) | Date ({calendar}): {y}/{m}/{d}"
        )
        print(
            f"     UT Time:   Moonrise {self._format_hours(lunar['moonrise_ut'])}, "
            f"Transit {self._format_hours(lunar['transit_ut'])}, "
            f"Moonset {self._format_hours(lunar['moonset_ut'])}"
        )

    def mi_mush(self, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Prints a detailed mathematical audit of the lunar opposition interval 'MI-MUSH'.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
        """
        y, m, d, _ = self._civil_components
        mm = self.get_mi_mush_data(city, ziggurat)

        print(f"\n--- Mi-Mush Analysis: {city} {y}/{m}/{d} ---")
        print(f"  Sun Rise (UT):  {self._format_hours(mm['sun_rise_ut'])}")
        print(f"  Moon Set (UT):  {self._format_hours(mm['moon_set_ut'])}")
        print(
            f"  Interval:       {mm['interval_minutes']:.2f} min ({mm['interval_ush']:.2f} ush)"
        )

        if mm["visible_simultaneously"]:
            print("  Status: Moon and Sun visible simultaneously (Opposition balance).")
        else:
            print("  Status: Moon set before Sunrise.")

    def kur(self, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Prints a mathematical audit of the late-lunation disappearance interval 'KUR'.

        Args:
            city (str, optional): Target Mesopotamian city registry. Defaults to "Babylon".
            ziggurat (float, optional): Observer height above ground level in meters. Defaults to 0.0.
        """
        y, m, d, _ = self._civil_components
        k = self.get_kur_data(city, ziggurat)

        print(f"\n--- KUR Analysis (Last Visibility): {city} {y}/{m}/{d} ---")
        print(f"  Moon Rise (UT): {self._format_hours(k['moon_rise_ut'])}")
        print(f"  Sun Rise (UT):  {self._format_hours(k['sun_rise_ut'])}")
        print(
            f"  Interval:       {k['interval_minutes']:.2f} min ({k['interval_ush']:.2f} ush)"
        )

        if k["status"] == "INVISIBLE":
            print("  Status: INVISIBLE (Moon rises after Sunrise).")
        elif k["status"] == "CRITICAL":
            print("  Status: CRITICAL (Last possible visibility window).")
        else:
            print("  Status: Visible in the eastern dawn sky.")

    def neomenia(
        self,
        city: str = "Babylon",
        ziggurat: float = 0.0,
        AoV: float = 12.0,
        uncertainty: float = 0.833,
    ) -> None:
        """Executes and renders standard visibility criteria matrices for the primary Neomenia.

        Args:
            city (str, optional): Target ancient observation city. Defaults to "Babylon".
            ziggurat (float, optional): Observer height in meters. Defaults to 0.0.
            AoV (float, optional): Empirical Arc of Vision constraint. Defaults to 12.0.
            uncertainty (float, optional): Marginal parsing threshold index. Defaults to 0.833.
        """
        y, m, d, _ = self._civil_components
        check_neomenia(y, m, d, city, ziggurat, AoV, uncertainty)

    def _run_planet_almanac(self, planet_instance: Any, title: str) -> None:
        """Private generic template dispatcher that dynamic loops through standard planet phenomena lists.

        Recalculates Delta T independently for each node collision to safely isolate civil UT frames.
        """
        from pymeeus.Angle import Angle
        from pymeeus.Epoch import Epoch

        epoch_seed = Epoch(self.jd)

        print("\n==========================================================")
        print(f"{f'ASTRONOMICAL EVENTS FOR {title.upper()}':^58}")
        print("==========================================================")
        print(
            f" Reference Date: {self._civil_components[1]}/{self._civil_components[0]} (JD {self.jd})"
        )
        print("----------------------------------------------------------")

        for method in planet_instance.phenomena_list:
            result = method(epoch_seed)

            phenomenon_name = (
                method.__name__.replace("get_", "")
                .replace("_", " ")
                .replace(" time", "")
                .title()
            )

            if isinstance(result, Epoch):
                y, m, d_float = result.get_date()

                # Granular localized Delta T extraction injection
                dt_seconds = delta_t(y, m)
                ut_epoch = result - (dt_seconds / 86400.0)
                y_ut, m_ut, d_ut_float = ut_epoch.get_date()

                print(
                    f"  [Time] {phenomenon_name:<25} -> "
                    f"{y_ut}/{m_ut:02}/{int(d_ut_float):02}  ({d_ut_float % 1 * 24:02.0f}h UT)"
                )

            elif isinstance(result, Angle) or hasattr(result, "dms"):
                # Safe structure parsing extraction for coordinate geometries
                val = result() if callable(result) else float(result)
                print(f"  [Space] {phenomenon_name:<24} -> {val:.3f}°")

        print("==========================================================\n")

    # =========================================================================
    # INDIVIDUAL PLANETARY DISPATCHERS (Clean ChronDate Wrappers)
    # =========================================================================

    def mars_almanac(self) -> None:
        """Prints all analytical astronomical phenomena for Mars within this temporal frame."""
        from mesotimes.astronomy.planets.superiors import MesopotamianMars

        self._run_planet_almanac(MesopotamianMars(), "Mars")

    def jupiter_almanac(self) -> None:
        """Prints all analytical astronomical phenomena for Jupiter within this temporal frame."""
        from mesotimes.astronomy.planets.superiors import MesopotamianJupiter

        self._run_planet_almanac(MesopotamianJupiter(), "Jupiter")

    def saturn_almanac(self) -> None:
        """Prints all analytical astronomical phenomena for Saturn within this temporal frame."""
        from mesotimes.astronomy.planets.superiors import MesopotamianSaturn

        self._run_planet_almanac(MesopotamianSaturn(), "Saturn")

    def mercury_almanac(self) -> None:
        """Prints all analytical astronomical phenomena for Mercury within this temporal frame."""
        from mesotimes.astronomy.planets.inferiors import MesopotamianMercury

        self._run_planet_almanac(MesopotamianMercury(), "Mercury")

    def venus_almanac(self) -> None:
        """Prints all analytical astronomical phenomena for Venus within this temporal frame."""
        from mesotimes.astronomy.planets.inferiors import MesopotamianVenus

        self._run_planet_almanac(MesopotamianVenus(), "Venus")

    @staticmethod
    def _format_hours(decimal_hours: float) -> str:
        """Internal helper to format decimal raw hours into standard sexagesimal terminal clocks.

        Args:
            decimal_hours (float): Time representation in decimal format.

        Returns:
            str: Normalized time string in "HH:MM" format, or "N/A" if input is NaN.
        """
        import math

        if math.isnan(decimal_hours):
            return "N/A"
        h = int(decimal_hours)
        m = int(round((decimal_hours - h) * 60))
        if m == 60:
            h += 1
            m = 0
        return f"{h:02d}:{m:02d}"

    def night_at_a_glance(self, city: str = "Babylon") -> None:
        """Draws a visual ASCII horizontal timeline visibility chart of the Mesopotamian planets.

        Optimizes calculation performance across the diurnal/nocturnal transition by
        caching body equatorial positions (RA/Dec) once per execution frame.

        Args:
            city (str, optional): Target Mesopotamian observation site. Defaults to "Babylon".
        """
        from mesotimes.astronomy.core import (
            equatorial_to_horizontal_at_instant,
            get_body_equatorial_at_midnight,
        )
        from mesotimes.astronomy.planets.inferiors import (
            MesopotamianMercury,
            MesopotamianVenus,
        )
        from mesotimes.astronomy.planets.superiors import (
            MesopotamianJupiter,
            MesopotamianMars,
            MesopotamianSaturn,
        )
        from pymeeus.Epoch import Epoch

        # Instantiate structural celestial planet objects
        mercury_obj = MesopotamianMercury()
        venus_obj = MesopotamianVenus()
        mars_obj = MesopotamianMars()
        jupiter_obj = MesopotamianJupiter()
        saturn_obj = MesopotamianSaturn()

        # 1. Coordinate spatial georeferencing
        city_lon = float(mesopotamian_cities[city]["longitude"])
        city_lat = float(mesopotamian_cities[city]["latitude"])
        local_tz_hours = round(city_lon / 15.0)

        # 2. Sync frame limits with internal localized day coordinates
        if (self.jd % 1) >= 0.5:
            jd_midnight_ut = int(self.jd) + 0.5
        else:
            jd_midnight_ut = int(self.jd) - 0.5

        y, m, d = Epoch(jd_midnight_ut).get_date()
        date_str = f"{int(y)}-{m:02d}-{int(d):02d}"

        jd_midnight_local = jd_midnight_ut - (local_tz_hours / 24.0)
        base_jd = jd_midnight_local - 0.5

        ut_hours_row = []
        loc_hours_row = []
        for block in range(49):
            loc_h = (12 + int(block * 0.5)) % 24
            ut_h = (loc_h - local_tz_hours) % 24
            if (block % 4) == 0:
                ut_hours_row.append(f"{ut_h:02d}  ")
                loc_hours_row.append(f"{loc_h:02d}  ")

        header = (
            "\n===================================================================\n"
            f"          NIGHT AT A GLANCE: {city.upper()} ({date_str})\n"
            "===================================================================\n"
            f"UT Hours:  {''.join(ut_hours_row)}\n"
            f"Local H.:  {''.join(loc_hours_row)}\n"
            "-------------------------------------------------------------------"
        )
        print(header)

        # 3. CRITICAL PERFORMANCE CACHE: Calculate RA/Dec ONCE at localized midnight matrix
        sun_ra, sun_dec = get_body_equatorial_at_midnight(jd_midnight_local, "sun")
        moon_ra, moon_dec = get_body_equatorial_at_midnight(jd_midnight_local, "moon")

        planets_data = []
        for p in [mercury_obj, venus_obj, mars_obj, jupiter_obj, saturn_obj]:
            p_ra, p_dec = get_body_equatorial_at_midnight(jd_midnight_local, p)
            planets_data.append({"name": p.name, "ra": p_ra, "dec": p_dec})

        # 4. Horizontal Transformation and Stream Rendering Blocks
        # Row 1: Twilight and Sunlight Arc
        sky_line = []
        for block in range(49):
            target_jd = base_jd + (block * 0.5 / 24.0)
            _, sun_alt = equatorial_to_horizontal_at_instant(
                target_jd, sun_ra, sun_dec, city_lon, city_lat
            )
            if sun_alt > 0:
                sky_line.append("#")
            elif sun_alt > -12:
                sky_line.append(":")
            elif sun_alt > -18:
                sky_line.append(".")
            else:
                sky_line.append(" ")
        print(" Sky/Sun :  " + "".join(sky_line))
        print("-" * 67)

        # Row 2: Lunar Presence Traces
        moon_line = []
        for block in range(49):
            target_jd = base_jd + (block * 0.5 / 24.0)
            _, moon_alt = equatorial_to_horizontal_at_instant(
                target_jd, moon_ra, moon_dec, city_lon, city_lat
            )
            if moon_alt > 0:
                moon_line.append("=")
            else:
                moon_line.append(" ")
        print(" Moon    :  " + "".join(moon_line))
        print("-" * 67)

        # Rows 3-7: Standard Wandering Stars Nodes (Planets)
        for p in planets_data:
            planet_sky_line = []
            for block in range(49):
                target_jd = base_jd + (block * 0.5 / 24.0)
                _, p_alt = equatorial_to_horizontal_at_instant(
                    target_jd, p["ra"], p["dec"], city_lon, city_lat
                )
                if p_alt > 0:
                    planet_sky_line.append("-")
                else:
                    planet_sky_line.append(" ")
            print(f" {p['name']:<7} :  " + "".join(planet_sky_line))

        # Global Interactive Terminal Footer Legend
        print(
            "===================================================================\n"
            "Legend:  # Day  : Civ/Nav Twilight  . Ast Twilight    Night\n"
            "         - Planet above horizon     = Moon above horizon\n"
        )

    def heliacal_phases(self, planet_name: str, city: str = "Babylon", ziggurat: float = 0.0) -> None:
        """Scans forward from the current date to resolve and print the next four heliacal phases

        of a given planet. Translates raw Epoch results into both Julian and Babylonian calendars.

        Args:
            planet_name (str): Name of the planet (mercury, venus, mars, jupiter, saturn).
            city (str, optional): Target ancient observation site. Defaults to "Babylon".
            ziggurat (float, optional): Observer height in meters. Defaults to 0.0.
        """
        from pymeeus.Epoch import Epoch
        from mesotimes.astronomy.planets.inferiors import MesopotamianMercury, MesopotamianVenus
        from mesotimes.astronomy.planets.superiors import MesopotamianMars, MesopotamianJupiter, MesopotamianSaturn
        from mesotimes.astronomy.planets.finder import (
            find_first_appearance_morning,
            find_last_appearance_evening,
            find_setting_heliacal_morning,
            find_setting_heliacal_evening,
        )

        # 1. Resolver la instancia del planeta
        mapping = {
            "mercury": MesopotamianMercury,
            "venus": MesopotamianVenus,
            "mars": MesopotamianMars,
            "jupiter": MesopotamianJupiter,
            "saturn": MesopotamianSaturn,
        }
        
        name_key = planet_name.lower().strip()
        if name_key not in mapping:
            raise ValueError(f"Unknown planet '{planet_name}'. Choose from: {list(mapping.keys())}")
        
        planet_instance = mapping[name_key]()
        seed_epoch = Epoch(self.jd)

        print("\n=======================================================")
        print(f"{f'HELIACAL STATIONS SCAN FOR {planet_instance.name.upper()}':^55}")
        print("=======================================================")
        print(f" Start Baseline: {self._civil_components[1]}/{self._civil_components[0]} (JD {self.jd})")
        print(f" Observatory   : {city} at {ziggurat:.1f}m over ground level")
        print("-------------------------------------------------------")

        # 2. Scan pipeline of the 4 fundamental phenomena
        # We define the scans with their finder functions and descriptive labels
        scans = [
            ("First Appearance (Morning/East - Γ/Ξ)", find_first_appearance_morning),
            ("Last Appearance (Evening/West - Ω/Σ)", find_last_appearance_evening),
            ("Heliacal Setting (Morning/East - Δ)", find_setting_heliacal_morning),
            ("Heliacal Setting (Evening/West - Ε)", find_setting_heliacal_evening),
        ]

        for label, finder_func in scans:
            try:
                # We fire the search engine by brute force over the daily grid
                event_epoch = finder_func(planet_instance, seed_epoch, city=city, ziggurat=ziggurat)
                
                # We fire the search engine by brute force over the daily grid
                event_date = ChronDate(event_epoch())
                y, m, d, cal = event_date._civil_components
                
                print(f"  [*] {label:<36}")
                print(f"      -> Calendar ({cal}): {y}/{m}/{int(d)} at {self._format_hours(d % 1 * 24)} UT")
                print(f"      -> Chronology  : {event_date.babylonian}")
                print("-------------------------------------------------------")
                
            except RuntimeError:
                # We capture the 60-day safety limit if the planet is stationary or in long retrograde
                print(f"  [x] {label:<36}\n      -> Not found in window (60 days limit)")
                print("-------------------------------------------------------")

        print("=======================================================\n")

    def bab_year_calendar(self, city: str = "Babylon", ziggurat: float = 0.0):
        """
        Prints a human-readable table of the Babylonian year structure.

        :param city: Observatory location, defaults to "Babylon"
        :type city: str, optional
        :param ziggurat: Altitude above the ground level in meters, defaults to 0.0
        :type ziggurat: float, optional
        """        
        if self.is_babylonian:
            # =================================================================
            # HISTORIC YEAR IMPLEMENTATION
            # =================================================================
            babdata = self.babylonian_data
            king_code = babdata["king_code"]
            current_year = babdata["year"]
            
            # 1. Fetch the starting JD of the Babylonian year (Month 1, Day 1)
            jd_ini = ChronDate.from_babylonian(king_code, current_year, 1, 1)()

            # 2. Query the empirical kingdates database
            # We fetch 14 rows to fully cover a potential 13-month embolismic leap year
            query = """
                SELECT king_month, jdat00h
                  FROM kingdates
                 WHERE jdat00h >= ?
                 ORDER BY jdat00h ASC
                 LIMIT 14;
            """
            
            with self._bab_conv._get_connection() as conn:
                # Map raw tuple columns into clean descriptive dictionaries
                conn.row_factory = lambda cursor, row: {
                    "king_month": row[0],
                    "jdat00h": row[1],
                }
                cursor = conn.cursor()
                cursor.execute(query, (jd_ini,))
                rows = cursor.fetchall()
            
            # 3. Process database rows to reconstruct the annual calendar structure
            print(f"\n--- HISTORIC BABYLONIAN CALENDAR: {KING_DICT[king_code].upper()} YEAR {current_year} ---")
            print(f"{'#':<3}{'Month Name':<15}{'Start Date (Y/M/D)':<22}{'JDE Start':<15}{'Length'}")
            print("-" * 72)
            
            total_duration = 0
            is_leap = False
            
            for i in range(len(rows) - 1):
                m_code = rows[i]["king_month"]
                jd_start = rows[i]["jdat00h"]
                jd_next = rows[i+1]["jdat00h"]
                
                # If the next row loops back to Month 1, the target historical year is complete
                if i > 0 and m_code == 1:
                    # Save the precise absolute astronomical boundary of the year end
                    year_end_jd = jd_start
                    break
                    
                # Compute month length via delta between consecutive lunar months
                length = int(jd_next - jd_start)
                total_duration += length
                
                # Suffixes .5 flag historical intercalary months (Ululu II / Addaru II)
                if m_code in [6.5, 12.5]:
                    is_leap = True
                
                # Translate code designation to localized text name
                m_name = MONTH_DICT[str(m_code)]
                
                # Convert JD boundaries to civil historical dates (Julian calendar)
                civ_y, civ_m, civ_d, _, _, _, _ = to_julian(jd_start)
                date_str = f"{civ_y}/{civ_m:02d}/{civ_d:02d}"
                
                print(f"{i+1:<3}{m_name:<15}{date_str:<22}{jd_start:<15.1f}{length} days")
                
                # Dynamically track the year-end timeline anchor
                year_end_jd = jd_next
            
            print("-" * 72)
            
            # Render annual diagnostic footer summaries
            e_y, e_m, e_d, _, _, _, _ = to_julian(year_end_jd)
            end_date_str = f"{e_y}/{e_m:02d}/{e_d:02d}"
            
            leap_str = "Leap year" if is_leap else "Regular year"
            print(f"Year ends on: {end_date_str} (JDE {year_end_jd:.1f})")
            print(f"Total year duration: {total_duration} days ({leap_str})")

        else:
            # =================================================================
            # PROLEPTIC YEAR IMPLEMENTATION
            # =================================================================
            from mesotimes.proleptic import ProlepticBabylonianCalendar
            pyear = ProlepticBabylonianCalendar(self._civil_components[0], city, ziggurat)
            pyear.print_year_table()



    # =========================================================================
    # MAGIC OPERATORS (Arithmetic, Comparison, and Object Hashing)
    # =========================================================================

    def __add__(self, days: int) -> "ChronDate":
        """Adds a specific integer number of days to the current timeline anchor.

        Returns a brand new, isolated, and immutable ChronDate instance.

        Args:
            days (int): Total days to shift forward.

        Returns:
            ChronDate: A new shifted chronological matrix state.
        """
        if not isinstance(days, int):
            return NotImplemented
        return ChronDate(self.jd + days)

    def __sub__(self, other: int | "ChronDate") -> "ChronDate" | float:
        """Overloaded subtraction operator matrix.

        1. If passed an integer, shifts the timeline backward and returns a new ChronDate.
        2. If passed another ChronDate, computes the absolute interval delta distance in days.

        Args:
            other (int | ChronDate): Right-hand operand node target.

        Returns:
            ChronDate | float: Transformed timeline state or raw floating-point days interval.
        """
        if isinstance(other, int):
            return ChronDate(self.jd - other)
        elif isinstance(other, ChronDate):
            return self.jd - other.jd
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """Evaluates whether two chronological instances share the same absolute Julian Day node."""
        if not isinstance(other, ChronDate):
            return NotImplemented
        return self.jd == other.jd

    def __lt__(self, other: object) -> bool:
        """Determines if this timeline anchor is strictly prior to another reference state."""
        if not isinstance(other, ChronDate):
            return NotImplemented
        return self.jd < other.jd

    def __le__(self, other: object) -> bool:
        """Determines if this timeline anchor is prior to or identical to another reference state."""
        if not isinstance(other, ChronDate):
            return NotImplemented
        return self.jd <= other.jd

    def __gt__(self, other: object) -> bool:
        """Determines if this timeline anchor is strictly posterior to another reference state."""
        if not isinstance(other, ChronDate):
            return NotImplemented
        return self.jd > other.jd

    def __ge__(self, other: object) -> bool:
        """Determines if this timeline anchor is posterior to or identical to another reference state."""
        if not isinstance(other, ChronDate):
            return NotImplemented
        return self.jd >= other.jd

    def __repr__(self) -> str:
        """Returns the formal, unambiguous string representation of the chronological matrix."""
        return f"ChronDate(jd={self.jd})"

    def __hash__(self) -> int:
        """Computes a secure hash of the absolute timestamp for dictionary key storage indices."""
        return hash(self.jd)

    def __call__(self) -> float:
        """Callable shorthand overlay matrix to seamlessly dump the underlying raw Julian Day."""
        return self.jd
