"""`mesotimes.astronomy.stars.py` - Implementation of stellar events."""

from pymeeus import Coordinates
from pymeeus.Angle import Angle
from pymeeus.Epoch import JDE2000, Epoch

from mesotimes.astronomy.planets.base import Planet
from mesotimes.astronomy.planets.finder import find_heliacal_event
from mesotimes.constants import BABYLONIAN_STAR_CATALOG
from mesotimes.astronomy.core import resolve_city_name, resolve_city_coordinates

from typing import Iterable, Callable, Tuple

class BabStar(Planet):
    """Class to represent a star in the Mesopotamian context."""

    def __init__(
        self,
        name: str,
        ra_j2000: Angle | float | int,
        dec_j2000: Angle | float | int,
        pm_ra_arcsec=0.0,
        pm_dec_arcsec: float = 0.0,
        arc_of_vision: float = 12.0,
        V: float|None = None,
        B_V: float|None = None,
    ):
        """Class constructor

        Args:
            name (str): Star name (from the catalog).
            ra_j2000 (Angle | float | int): Right Ascension in J2000.
            dec_j2000 (Angle | float | int): Declination in J2000.
            pm_ra_arcsec (float, optional): Proper Motion in RA in arcseconds/year. Defaults to 0.0.
            pm_dec_arcsec (float, optional): Proper Motion in Dec in arcseconds/year. Defaults to 0.0.
            arc_of_vision (float, optional): Arc of Vision for the star in degrees. Defaults to 12.0.
        """
        super().__init__(name, arc_of_vision)
        self.ra0 = (
            Angle(ra_j2000, ra=True) if isinstance(ra_j2000, (int, float)) else ra_j2000
        )
        self.dec0 = (
            Angle(dec_j2000) if isinstance(dec_j2000, (int, float)) else dec_j2000
        )

        # We record the proper motions strictly as annual arcseconds
        self.pm_ra = (
            Angle(0, 0, pm_ra_arcsec)
            if isinstance(pm_ra_arcsec, (int, float))
            else pm_ra_arcsec
        )
        self.pm_dec = (
            Angle(0, 0, pm_dec_arcsec)
            if isinstance(pm_dec_arcsec, (int, float))
            else pm_dec_arcsec
        )
        self.V = V
        self.B_V = B_V

    @classmethod
    def from_catalog(cls, star_name: str) -> object:
        """Factory method to instantiate any star from the Babylonian database.

        Args:
            star_name (str): Star name in the catalog.

        Raises:
            ValueError: _description_

        Returns:
            BabStar: BabStar instance.
        """
        if star_name not in BABYLONIAN_STAR_CATALOG:
            raise ValueError(f"Star '{star_name}' not found in Babylonian catalog.")

        data = BABYLONIAN_STAR_CATALOG[star_name]

        # Unpack the data and instantiate dynamically
        return cls(
            name=star_name,
            ra_j2000=Angle(*data["ra0"], ra=True),
            dec_j2000=Angle(*data["dec0"]),
            pm_ra_arcsec=data["pm_ra"],
            pm_dec_arcsec=data["pm_dec"],
            arc_of_vision=data["arc_of_vision"],
            V=data["V"],
            B_V=data["(B-V)"]
        )

    @classmethod
    def stars(cls, screen: int = 1, filter_type: str | None = None):
        """Prints a clean ASCII table of the internal Babylonian Star Catalog for auditing.

        Args:
            filter_type (str | None, optional): Type of star to list (normal_star, mul_apin, both). Defaults to None.
            screen (int, optional): Page # to print. Defaults to 1.

        """

        def sep_cun(string, sep):
            return sep.join(list(string))

        screen_dict = {
            1: "Astronomical data.",
            2: "Angle of vision and transliterations.",
            3: "Name meaning and cuneiform glyphs.",
            4: "Photometry.",
            5: "Astrophysics and modern comments."
        }

        if screen not in screen_dict:
            print(
                f"You asked for screen: {screen}, but it has not (yet) been implemented."
            )
            print("Currently available screens are:")
            for scr, cont in screen_dict.items():
                print(f"    Screen {scr}: {cont}")
            return

        if screen == 1:
            print("\n" + "-" * 76)
            print(
                "| Star Name       |    RA(J2000) |   DEC(J2000) |   pm_ra |  pm_dec | Type |"
            )
            print(
                "|-----------------|--------------|--------------|---------|---------|------|"
            )

            type_mapping = {"normal_star": "N", "mul_apin": "M", "both": "B"}

            for star_name, data in BABYLONIAN_STAR_CATALOG.items():
                if filter_type and data.get("type") != filter_type:
                    continue

                ra_str = Angle(*data["ra0"], ra=True).ra_str(fancy=False, n_dec=2)
                dec_str = Angle(*data["dec0"]).dms_str(fancy=False, n_dec=2)
                t_code = type_mapping.get(data.get("type"), "-")

                print(
                    f"| {star_name:<15} | "
                    f"{ra_str:>12} | "
                    f"{dec_str:>12} | "
                    f"{data['pm_ra']:>7.3f} | "
                    f"{data['pm_dec']:>7.3f} | "
                    f"  {t_code:<2} |"
                )

            print("=" * 76)
            print(
                "* pm_ra, pm_dec in mas/yr | Types -> N: Normal Star | M: MUL.APIN | B: Both"
            )

        elif screen == 2:
            print("\n" + "-" * 79)
            print(
                "| Star Name       |  AoV | Cuneiform Name (mul.+)  | Akkadian Name            |"
            )
            print(
                "|-----------------|------|-------------------------|--------------------------|"
            )

            for star_name, data in BABYLONIAN_STAR_CATALOG.items():
                if filter_type and data.get("type") != filter_type:
                    continue

                aov = data["arc_of_vision"]
                cun = data["cuneiform_name"]
                akk = data["transliteration"]

                print(f"| {star_name:<15} | {aov:>4} | {cun[4:27]:<23} | {akk:<24} |")

            print("=" * 79)

        elif screen == 3:
            print("\n" + "-" * 79)
            print(
                "| Star name      | Meaning                                 | Cuneiform Glyphs"
            )
            print(
                "|----------------|-----------------------------------------|-------------------"
            )

            for star_name, data in BABYLONIAN_STAR_CATALOG.items():
                if filter_type and data.get("type") != filter_type:
                    continue

                cun = sep_cun(data["cuneiform_unicode"], " ")
                mea = data["meaning"]

                print(f"| {star_name:<14} | {mea:<40}| {cun}")

            print("=" * 79)

        elif screen == 4:
            print("\n" + "-" * 79)
            print(
                "| Star name      | Arc Vision | V magnitude | (B-V) Color Index |"
            )
            print(
                "|----------------|------------|-------------|-------------------|"
            )

            for star_name, data in BABYLONIAN_STAR_CATALOG.items():
                if filter_type and data.get("type") != filter_type:
                    continue

                arc = data.get("arc_of_vision", 0.0)
                v_mag = data.get("V", 0.0)
                bv = data.get("(B-V)", 0.0)

                arc_str = f"{arc:.1f}°"
                v_str = f"{v_mag:+.2f}"
                bv_str = f"{bv:+.2f}"

                # Estructura totalmente simétrica y cerrada
                print(f"| {star_name:<14} | {arc_str:<10} | {v_str:<11} | {bv_str:<17} |")

            print("=" * 79)

        elif screen == 5:
            print("\n" + "-" * 79)
            print(
                "| Star name      | Historical & Astrophysical Comments"
            )
            print(
                "|----------------|------------------------------------------------------------"
            )

            for star_name, data in BABYLONIAN_STAR_CATALOG.items():
                if filter_type and data.get("type") != filter_type:
                    continue

                comm = data.get("comment", "")
                
                # Al estar abierta a la derecha, los comentarios largos pueden fluir 
                # libremente en la terminal sin romper las columnas principales
                print(f"| {star_name:<14} | {comm}")

            print("=" * 79)

    catalog = stars

    def get_geocentric_position(self, epoch: Epoch) -> tuple[Angle, Angle, None]:
        """Calculates the star equatorial coordinates (RA, Dec) for a given epoch including precession and proper motion.

        Args:
            epoch (Epoch): Epoch to evaluate coordinates.

        Returns:
            tuple[Angle, Angle, None]: Right Ascension and Declination (equinox of the epoch), None.
        """
        # PyMeeus requires pm_ra and pm_dec in arcseconds
        alpha, delta_out = Coordinates.precession_equatorial(
            JDE2000, epoch, self.ra0, self.dec0, self.pm_ra, self.pm_dec
        )
        # The following is due to a bug in pymeeus 0.5.12
        if self.dec0() > 85.0:
            delta = Angle(90.0) - delta_out
        else:
            delta = delta_out

        return alpha, delta, None

    def get_rising_angle(self, epoch: Epoch, latitude: Angle) -> Angle:
        """Angle of the diurnal path at star rise/set time relative to the horizon.

        Args:
            epoch (Epoch): Epoch to evaluate coordinates.
            latitude (Angle): Latitude of the observation site.

        Raises:
            ValueError: If the star is circumpolar or perpetually invisible 
                at the given latitude (never crosses the horizon).

        Returns:
            Angle: Angle of the diurnal path relative to the horizon.
        """
        # 1. Obtener la declinación (delta) de la estrella para la época dada
        _, delta, _ = self.get_geocentric_position(epoch)
        
        # 2. Extraer los valores numéricos en grados para la validación geométrica
        lat_deg = abs(latitude())
        dec_deg = abs(delta())
        
        # 3. Blindaje geográfico contra estrellas que no tocan el horizonte
        co_latitude = 90.0 - lat_deg
        
        if dec_deg >= co_latitude:
            # Determinamos cuál es el caso específico para dar un mensaje de error útil
            if delta() * latitude() > 0:
                condition = "CIRCUMPOLAR (always above horizon)"
            else:
                condition = "PERPETUALLY INVISIBLE (always below horizon)"
                
            raise ValueError(
                f"[{self.name}] Cannot calculate rising angle: Object is {condition} "
                f"at latitude {latitude():.4f}° (Declination: {delta():.4f}°)."
            )

        # 4. Si pasa el filtro, el cálculo de PyMeeus es 100% seguro
        return Coordinates.diurnal_path_horizon(delta, latitude)


    def get_equatorial(self, epoch: Epoch) -> tuple[Angle, Angle]:
        """Calculates the star equatorial coordinates (RA, Dec) for a given epoch.

        Args:
            epoch (Epoch): Date to evaluate coordinates.

        Returns:
            tuple[Angle, Angle]: Right Ascension and Declination (equinox of the epoch).
        """
        return self.get_geocentric_position(epoch)[:2]

    def get_ecliptical(self, epoch: Epoch) -> tuple[Angle, Angle]:
        """Calculates the star ecliptical coordinates (lon, lat) for a given epoch.

        Args:
            epoch (Epoch): Date to evaluate coordinates.

        Returns:
            tuple[Angle, Angle]: Longitude and Latitude (equinox of the epoch).
        """
        ra, dec = self.get_geocentric_position(epoch)[:2]
        true_obliquity = Coordinates.true_obliquity(epoch)
        lon, lat = Coordinates.equatorial2ecliptical(ra, dec, true_obliquity)

        return lon, lat

    def heliacal_rising(
        self,
        epoch: Epoch,
        city: str | dict = "Babylon",
        ziggurat: float = 0.0,
        max_days: int = 60,
    ) -> Epoch:
        """Search for an heliacal rising of the star in the max_days following the epoch.

        Args:
            epoch (Epoch): Start epoch for the search.
            city (str | dict, optional): Observatory/City name. Defaults to "Babylon".
            ziggurat (float, optional): Height of the observer above terrain in meters. Defaults to 0.0.
            max_days (int, optional): Explore max_days days following the epoch. Defaults to 60.

        Returns:
            Epoch: Epoch of the heliacal rising.
        """
        return find_heliacal_event(
            self,
            epoch,
            horizon="sunrise",
            search_type="appearance",
            city=city,
            ziggurat=ziggurat,
            max_days=max_days,
        )

    def acronychal_rising(
        self,
        epoch: Epoch,
        city: str | dict = "Babylon",
        ziggurat: float = 0.0,
        max_days: int = 60,
    ) -> Epoch:
        """Search for an acronychal rising of the star in the max_days following the epoch.

        Args:
            epoch (Epoch): Start epoch for the search.
            city (str | dict, optional): Observatory/City name. Defaults to "Babylon".
            ziggurat (float, optional): Height of the observer above terrain in meters. Defaults to 0.0.
            max_days (int, optional): Explore max_days days following the epoch. Defaults to 60.

        Returns:
            Epoch: Epoch of the acronychal rising.
        """
        return find_heliacal_event(
            self,
            epoch,
            horizon="sunset",
            search_type="appearance",
            city=city,
            ziggurat=ziggurat,
            max_days=max_days,
        )

    def search_phenomena(
        self,
        year: int,
        phenomenon: str = "heliacal",
        city: str | dict = "Babylon",
        ziggurat: float = 0.0,
        with_return: bool = False,
        verbose: bool = True
    ):
        """Search for the star Heliacal/Acronychal Rising along the year.

        Args:
            year (int): Year to explore.
            phenomenon (str, optional): Either "heliacal" or "acronychal". Defaults to "heliacal".
            city (str | dict, optional): Observatory/City name. Defaults to "Babylon".
            ziggurat (float, optional): Height of the observer above terrain in meters. Defaults to 0.0.
            with_return (bool, optional): If it's true, it returns the epoch of the phenomenon. Defaults to False.
            verbose (bool, optional): Prints results to screen if True. Default to True.

        Raises:
            ValueError: if phenomenon is not "heliacal" or "acronychal".
        
        Returns:
            Epoch: Epoch of the phenomenon.
        """
        # Look for a specific starting month in catalog to avoid "ALREADY VISIBLE" blocks
        # if not defined, default to 1 (January)
        #start_month = BABYLONIAN_STAR_CATALOG[self.name].get("start_month", 1)
        start_month = BABYLONIAN_STAR_CATALOG.get(self.name, {}).get("start_month", 1)
        epoch = Epoch(year, int(start_month), 1)
        latitude = Angle(resolve_city_coordinates(city)["latitude"])


        e = None  # Scope safety assignment

        if phenomenon == "heliacal":
            if verbose:
                print(
                    f"\nSearch for {self.name} Heliacal Appearance in the East before sunrise:"
                )
                print("=" * 70)
                y, m, d = epoch.get_date()
                s = f" {y:04d}-{m:02d}-{round(d, 0)}"
                print(f"Search starting at {resolve_city_name(city)}: {s}")

            try:
                # First attempt using optimal or standard baseline
                e = self.heliacal_rising(
                    epoch, city=city, ziggurat=ziggurat, max_days=366
                )
            except Exception:
                # If it fails (ValueError or RuntimeError), try shifting 6 months later
                try:
                    retry_month = (
                        7 if start_month == 1 else ((start_month + 5) % 12) + 1
                    )
                    epoch_2 = Epoch(year, retry_month, 1)
                    e = self.heliacal_rising(
                        epoch_2, city=city, ziggurat=ziggurat, max_days=366
                    )
                except Exception as retry_err:
                    print(
                        f"[ERROR] Could not resolve Heliacal for {self.name}: {retry_err}"
                    )

            if verbose:
                if e is not None:
                    y, m, d = e.get_date()
                    s = f" {y:04d}-{m:02d}-{round(d, 2):05.2f}"
                    print(f"   First sight found at: {s} (JD={e():15.6f})")
                    ang = self.get_rising_angle(epoch, latitude)
                    print(f"           Rising angle:  {round(ang(),3)}d")
                print("-" * 70)
            if with_return:
                return e

        elif phenomenon == "acronychal":
            if verbose:
                print(
                    f"\nSearch for {self.name} Acronychal Appearance in the East before sunset:"
                )
                print("=" * 70)
                y, m, d = epoch.get_date()
                s = f" {y:04d}-{m:02d}-{round(d, 0)}"
                print(f"  Search starting at {resolve_city_name(city)}:{s}")

            try:
                e = self.acronychal_rising(
                    epoch, city=city, ziggurat=ziggurat, max_days=366
                )
            except Exception:
                try:
                    retry_month = (
                        7 if start_month == 1 else ((start_month + 5) % 12) + 1
                    )
                    epoch_2 = Epoch(year, retry_month, 1)
                    e = self.acronychal_rising(
                        epoch_2, city=city, ziggurat=ziggurat, max_days=366
                    )
                except Exception as retry_err:
                    print(
                        f"[ERROR] Could not resolve Acronychal for {self.name}: {retry_err}"
                    )

            if verbose:
                if e is not None:
                    y, m, d = e.get_date()
                    s = f" {y:04d}-{m:02d}-{round(d, 2):05.2f}"
                    print(f"Acronychal sight found at:{s} (JD={e():15.6f})")
                    ang = self.get_rising_angle(epoch, latitude)
                    print(f"             Rising angle: {round(ang(),3)}d")
                print("-" * 70)
            if with_return:
                return e

        else:
            raise ValueError(f"Unknown phenomenon: {phenomenon}")

    def twilight_tomography(
        self,
        year: int,
        phenomena: str = "heliacal",
        city: str = "Babylon",
        ziggurat: float = 0.0,
        minutes: int = 6,
        ramp_model: bool = False,
        air_mass_func: Callable[[Angle, float], Tuple[float, float, float]] | None = None,
        k: float = 0.20,
        day_offset: Iterable[int] = (0, 1, 2, 3),
        verbose: bool = True,
    ) -> None:
        """Executes a multi-day twilight visibility scan sequence for this star instance.

        Acts as an instance wrapper over `scan_twilight_visibility`. It iterates over 
        a collection of day offsets relative to the star's calculated phenomenon epoch, 
        printing consecutive time-series reports. To avoid terminal noise, it automatically 
        silences the underlying geometric finder data (`verbose=False`) for all iterations 
        except the first day of the sequence.

        Args:
            year (int): Historical BCE/CE year to evaluate (e.g., -378).
            phenomena (str, optional): Type of phenomenon to seek. Defaults to "heliacal".
            city (str, optional): Target archaeological site or city. Defaults to "Babylon".
            ziggurat (float, optional): Elevation override in meters to simulate observations
                from high platforms. Defaults to 0.0.
            minutes (int, optional): Step interval in sidereal minutes for the time loop. Defaults to 6.
            ramp_model (bool, optional): Use standard zenith-based ramp model instead of a 3D 
                scattering model if True. Defaults to False.
            air_mass_func (Callable[[Angle, float], tuple[float, float, float]], optional):
                Air-mass function to use. If None, falls back to air_mass_pickering. Defaults to None.
            k (float, optional): Atmospheric extinction coefficient. Defaults to 0.20.
            day_offset (Iterable[int], optional): Sequence of integer day offsets to simulate. 
                Defaults to (0, 1, 2, 3, 4).
            verbose (bool, optional): If True, allows the initial geometric search report to 
                print. Defaults to True.

        Raises:
            ValueError: If the star instance lacks valid V photometric magnitude data.
        """
        from mesotimes.astronomy.visibility import scan_twilight_visibility, air_mass_pickering

        if self.V is None:
            raise ValueError("Star has no valid magnitude.")

        for offset in day_offset:
            # The first iteration honors the global verbose flag; subsequent ones are silenced
            is_first = (offset == list(day_offset)[0]) if isinstance(day_offset, (list, tuple)) else True
            
            scan_twilight_visibility(
                year,
                self,
                phenomena=phenomena,
                city=city,
                ziggurat=ziggurat,
                minutes=minutes,
                ramp_model=ramp_model,
                air_mass_func=air_mass_pickering if air_mass_func is None else air_mass_func,
                k=k,
                day_offset=offset,
                verbose=verbose if is_first else False,
            )


    def __repr__(self) -> str:
        return f"{self.name} as Babylonian star"
