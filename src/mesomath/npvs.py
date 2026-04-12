"""This module implements classes for Non-Place-Value numeration system and
related arithmetic. Intended for Mesopotamian metrological systems,
but class Npvs is of general use.

* class  Npvs: Generic class inspired in Imperial Units System lengths

    * class _MesoM: Specializes the Npvs class to handle Mesopotamian counting systems.

        * class  BsyC: Babylonian System C
        * class  BsyG: Babylonian System G
        * class  BsyS: Babylonian System S
        * class  BsyK: Babylonian System K

        * class MesoM: Specializes the Npvs class to handle Mesopotamian measurements.

            * class  Blen: Babylonian length system
            * class  Bsur: Babylonian surface system
            * class  Bvol: Babylonian volume system
            * class  Bcap: Babylonian capacity system
            * class  Bwei: Babylonian weight system
            * class  Bbri: Babylonian brick counting system

"""

import sys
from re import sub
from typing import Final

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self
from parsimonious.exceptions import IncompleteParseError, ParseError, VisitationError

from mesomath.babn import BabN

# Data
#: Dictionary of principal fractions withouth 1/6
fdic0: Final[dict] = {
    3: (["2/3", "1/3"], [2, 1]),
    5: ([""], []),
    10: (["1/2"], [5]),
    6: (["5/6", "2/3", "1/2", "1/3"], [5, 4, 3, 2]),
    12: (["5/6", "2/3", "1/2", "1/3"], [10, 8, 6, 4]),
    30: (["5/6", "2/3", "1/2", "1/3"], [25, 20, 15, 10]),
    60: (["5/6", "2/3", "1/2", "1/3"], [50, 40, 30, 20]),
    100: (["1/2"], [50]),
    180: (["5/6", "2/3", "1/2", "1/3"], [150, 120, 90, 60]),
}

#: Dictionary of principal fractions including 1/6
fdic1: Final[dict] = {
    3: (["2/3", "1/3"], [2, 1]),
    5: ([""], []),
    10: (["1/2"], [5]),
    6: (["5/6", "2/3", "1/2", "1/3", "1/6"], [5, 4, 3, 2, 1]),
    12: (["5/6", "2/3", "1/2", "1/3", "1/6"], [10, 8, 6, 4, 2]),
    30: (["5/6", "2/3", "1/2", "1/3", "1/6"], [25, 20, 15, 10, 5]),
    60: (["5/6", "2/3", "1/2", "1/3", "1/6"], [50, 40, 30, 20, 10]),
    100: (["1/2"], [50]),
    180: (["5/6", "2/3", "1/2", "1/3", "1/6"], [150, 120, 90, 60, 30]),
}


# Functions
def cmul(x: list[int]) -> list[int]:
    """Utility function. Returns list of cumulative products of the factor list x

    Example: cmul([4,3,3,22,10,8,3]) returns:
         [1, 4, 12, 36, 792, 7920, 63360, 190080]

    :param x: list of factors
    :type x: list[int]
    :raises TypeError: if x is not a list
    :return: list of cumulative products of the factor list x
    :rtype: list[int]
    """
    if isinstance(x, list):
        prod = 1
        prodl = [1]
        for i in x:
            prod *= i
            prodl.append(prod)
        return prodl
    else:
        raise TypeError


def normalize(st: str) -> str:
    """Converts `aname`'s to unit names and standardizes fractions.

    :param st: input strig to be normalized
    :type st: str
    :return: normalized string
    :rtype: str
    """
    # Consolidate character and word replacements
    replacements = {
        r"[šŠ]": "s",
        r"([a-zA-Z])(['23\-]+)": r"\g<1>",
        r"GAN": "gan",
        r"U": "u",
    }

    # Pre-compile patterns for efficiency
    for pattern, repl in replacements.items():
        st = sub(pattern, repl, st)

    # Normalizing fractions
    st = sub(r"1/6|1/3|1/2|2/3|5/6", r"+\g<0>", st)
    st = sub(r" *\+ *", "+", st)
    st = sub(r"[a-z]\+", r"\g<0>+", st)
    st = sub(r" *\++", "+", st)
    st = sub(r"([a-z])(\+)", r"\g<1> 0+", st)

    # Clean up spacing
    st = sub(r"\s+", " ", st).strip()

    # Handle leading fractions
    if st.startswith("+"):
        st = "0" + st

    return st


# Classes
class Npvs:
    """This class implement Non-Place-Value System arithmetic
           Example is taken from Imperial length units:

           **league <-3- mile <-8- furlong <-10- chain <-22- yard <-3- foot
           <-3- hand <-4- inch**

    Class Atributes:
    ----------------

    :title: Definition of the object
    :uname: Unit names
    :ufact: Factor between units
    :aname: Actual or academic unit names
    :cfact: Factor with the smallest unit
    :siv: S.I. value of the smallest unit
    :siu: S.I. unit name
    :prtsex: Printing measurements in sexagesimal (default: False)


    Instance Attributes:
    --------------------

    :dec: Decimal value of measurement in terms of the smallest unit
    :list: List of values per unit

    Operators
    ---------

    This class overloads arithmetic and logical operators allowing arithmetic
    operations and comparisons to be performed between members of the class.
    Comparison with other objects raises ``NotImplementedError``.

    jccsvq fecit, 2005. Public domain.

    """

    title: str = "Imperial length measurement"
    uname: list[str] = "in hh ft yd ch fur mi lea".split()  # Unit names
    aname: list[str] = (
        "inch hand foot yard chain furlong mile league".split()
    )  # Actual unit names
    ufact: list[int] = [4, 3, 3, 22, 10, 8, 3]  # Factor between units
    cfact: list[int] = [
        1,
        4,
        12,
        36,
        792,
        7920,
        63360,
        190080,
    ]  # Factor with the smallest unit
    siv: float = 0.0254  # meters per inch
    siu: str = "meters"  # S.I. unit name

    @classmethod
    def scheme(cls, actual: bool = False) -> list:
        """Returns list with the unit names separated by the corresponding factors

        :param actual: Uses actual or academic unit names if True, defaults to False
        :type actual: bool, optional
        :return: list with the unit names separated by the corresponding factors
        :rtype: list

        Example:

            >>> print(*Npvs.scheme(Npvs))
            lea <-3- mi <-8- fur <-10- ch <-22- yd <-3- ft <-3- hh <-4- in

            >>> print(*Npvs.scheme(Npvs,actual=1))
            league <-3- mile <-8- furlong <-10- chain <-22- yard <-3- foot <-3- hand <-4- inch

        """
        ll = []
        if actual:
            for i in range(len(cls.ufact)):
                ll.append(cls.aname[i])
                ll.append("⟵" + str(cls.ufact[i]) + "-")
            ll.append(cls.aname[-1])
        else:
            for i in range(len(cls.ufact)):
                ll.append(cls.uname[i])
                ll.append("⟵" + str(cls.ufact[i]) + "-")
            ll.append(cls.uname[-1])
        ll.reverse()
        return ll

    def dec2un(self, x: int) -> list:
        """Converts the decimal integer n to a list of integers, such that, for
        example, 1001 (inches) becomes ``[1, 1, 2, 5, 1, 0, 0, 0]``, which means
        that 1001 inches equals: 1 chain 5 yards 2 feet 1 hand 1 inch.

        :param x: input decimal integer
        :type x: int
        :return: list of unit coefficients
        :rtype: list
        """
        result = []
        for i in self.ufact:
            result.append(x % i)
            x //= i
        result.append(x)
        return result

    @classmethod
    def from_si(cls, val: float)-> object:
        """Converts SI measure into object.

        :param val: SI value
        :type val: float
        :return: Object with corresponding SI value
        :rtype: object
        """        
        return cls(int(round(val/cls.siv)))


    def __init__(self, x: int | str) -> None:
        """Class constructor

        :param x: The parameter n can be an integer (sign is ignored) or a properly
         formatted string representing the value. See the tutorial
        :type x: int | str
        """
        if type(x) is int:
            x = abs(x)
            dec = x
            lista = self.dec2un(x)
        elif type(x) is str:
            if x.find("(") >= 0:
                xx = x.split("(")[1:]
                xnew = ""
                for i in xx:
                    xy = i.split(")")
                    coef = self.sexsys(xy[0])
                    xnew += str(coef.dec) + " "
                    xnew += xy[1] + " "
                #                print(xnew)
                x = xnew
            ll = x.split()
            l1 = ll[::2]
            l2 = ll[1::2]
            t = 0
            for _ in range(len(l2)):
                j = self.uname.index(l2[_])
                t += int(l1[_]) * self.cfact[j]
            dec = t
            lista = self.dec2un(t)
        self.__dec: Final[int] = dec
        self.__list: Final[list[int]] = lista

    @property
    def dec(self):
        """Getter"""
        return self.__dec

    @property
    def list(self):
        """Getter"""
        return self.__list

    def si(self) -> float:
        """Returns the numeric equivalent in SI units

        :return: numeric equivalent in SI units
        :rtype: float
        """
        return self.dec * self.siv

    def SI(self) -> str:
        """Returns formated string with the equivalent in SI units

        :return: formated string with the equivalent in SI units
        :rtype: str
        """
        return f"{self.dec * self.siv} {self.siu}"

    def __add__(self, other: Self) -> Self:
        """Overloads ``+`` operator: returns object with the sum of operands

        :param other: operand
        :type other: Self
        :return: object with the sum of operands
        :rtype: Self
        """
        if isinstance(other, Npvs):
            return self.__class__(self.dec + other.dec)
        return NotImplemented

    def __sub__(self, other: Self) -> Self:
        """Overloads ``-`` operator: returns object with the absolute difference
        of operands

        :param other: operand
        :type other: Self
        :return: object with the absolute difference of operands
        :rtype: Self
        """
        if isinstance(other, Npvs):
            return self.__class__(abs(self.dec - other.dec))
        return NotImplemented

    def __mul__(self, other: int | float) -> Self:
        """Overloads ``*`` operator: returns object with the operands product

        :param other: operand
        :type other: int | float
        :return: object with the operands product
        :rtype: Self
        """
        t = self.dec * other
        return self.__class__(int(round(t, 0)))

    def __rmul__(self, other: int) -> Self:
        """Overloads ``*`` operator: returns object with the operands product

        :param other: operand
        :type other: int | float
        :return: object with the operands product
        :rtype: Self
        """
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> Self:
        """Overloads ``/`` operator: returns object with the operands quotient

        :param other: operand
        :type other: int | float
        :return: object with the operands quotient
        :rtype: Self
        """
        return self.__class__(int(round(self.dec / other, 0)))

    def __lt__(self, other: Self) -> bool:
        """Overloads ``<`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec <= other.dec
        else:
            raise NotImplementedError

    def __le__(self, other: Self) -> bool:
        """Overloads ``<=`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec <= other.dec
        else:
            raise NotImplementedError

    def __eq__(self, other: Self) -> bool:
        """Overloads ``==`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec == other.dec
        else:
            raise NotImplementedError

    def __ne__(self, other: Self) -> bool:
        """Overloads ``!=`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec != other.dec
        else:
            raise NotImplementedError

    def __gt__(self, other: Self) -> bool:
        """Overloads ``>`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec > other.dec
        else:
            raise NotImplementedError

    def __ge__(self, other: Self) -> bool:
        """Overloads ``>=`` operator

        :param other: another Npvs object
        :type other: Self
        :raises NotImplementedError: if not Self object
        :return: comparison result
        :rtype: bool
        """
        if isinstance(other, type(self)):
            return self.dec >= other.dec
        else:
            raise NotImplementedError

    def __repr__(self) -> str:
        """Returns string representation of object"""
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                ss.append(str(self.list[i]))
                ss.append(self.uname[i])
        return " ".join(ss)

    def __hash__(self):
        """Returns hash value of the instance"""
        return hash((type(self), self.dec))

    def __int__(self):
        """Converts instance to int"""
        return self.dec


class _MesoM(Npvs):
    """
    Specializes the Npvs class to handle Mesopotamian measurements.

    Introduces the .sex(), .metval() and .explain() methods and the .prtsex attribute.
    Modifies __repr__()

    :meta public:
    """

    title: str = "Sexagesimal sistem"
    uname: list[str] = "sa sb sc sd".split()  # Unit names
    aname: list[str] = "Ša Šb Šc Šd".split()  # Unit names
    ufact: list[int] = [60, 60, 60]  # Factor between units
    cfact: list[int] = [1, 60, 3600, 216000]  # Factor with the smallest unit
    siv: float = 1.0  #
    siu: str = "counts"  # S.I. unit name
    prtsex: bool = False  # Printing measurements in sexagesimal
    ubase: int = 0  # Base unit for metrological tables

    def __init__(self, x: int | str | float) -> None:
        """Class constructor

        :param x: The parameter n can be an integer (sign is ignored) or a properly
             formatted string representing the value. See the tutorial
        :type x: int | float | str
        """
        # CASE 1: Numeric input (Integer)
        # Directly represents the value in the smallest unit of the system.
        if type(x) is int:
            x = abs(x)
            dec = x
            lista = self.dec2un(x)

        # CASE 2: Numeric input (Float)
        # Rounded to the nearest integer to maintain discrete metrological consistency.
        elif type(x) is float:
            dec = int(round(abs(x), 0))
            lista = self.dec2un(dec)

        # CASE 3: String input (The "Cuneiform" parser)
        # Handles complex strings like "1(u) 2(dis) nindan" or fractions.
        elif isinstance(x, str):
            from mesomath.parser import MesoInterpreter

            target_sexsys = getattr(self, "sexsys", None)

            try:
                # Create the interpreter with the current class context
                parser = MesoInterpreter(self.__class__, target_sexsys)

                # Parse the string into a decimal value
                dec = parser.parse(x)

                # Convert decimal value to the internal unit list representation
                # This uses your existing dec2un method
                lista = self.dec2un(dec)

            except (ParseError, IncompleteParseError, VisitationError, ValueError):
                # Handles "unrecognized" characters or grammar violations
                raise ValueError(
                    "Incorrect input string: check format or units."
                ) from None

        # Internal state storage (Immutable/Final)
        self.__dec: Final[int] = dec  # Total value in smallest units
        self.__list: Final[list[int]] = lista  # Value broken down by unit

    @classmethod
    def cname(cls) -> list:
        """Return list of unit cuneiform glyphs

        :return: list of unit cuneiform glyphs
        :rtype: list
        """
        from .glyphs import MAP_UNIT_LOGOGRAMS

        return [MAP_UNIT_LOGOGRAMS.get(_, _) for _ in cls.uname]

    @classmethod
    def scheme(cls, actual: bool = False, cuneiform: bool = False) -> list:
        """Factor diagram for MesoMath.

        :param actual: uses actual or academic unit names if True, defaults to False
        :type actual: bool, optional
        :param cuneiform: write cuneiform glyphs if True, defaults to False
        :type cuneiform: bool, optional
        :return: list with the unit names separated by the corresponding factors
        :rtype: list
        """
        ll = []
        # Select the list of base names
        if cuneiform:
            names = cls.cname()
        elif actual:
            names = cls.aname
        else:
            names = cls.uname

        for i in range(len(cls.ufact)):
            unit_name = names[i]

            ll.append(unit_name)
            if cuneiform:
                ll.append(f"  ╼{cls.ufact[i]}╾ ")
            else:
                ll.append(f"<-{cls.ufact[i]}-")

        # Append last unit
        last_unit = names[-1]
        ll.append(last_unit)

        ll.reverse()
        return ll


    @property
    def dec(self):
        """Getter"""
        return self.__dec

    @property
    def list(self):
        """Getter"""
        return self.__list

    @property
    def acad(self):
        return self.__repr__(actual=True)

    def sex(self, r: int = 0) -> BabN | None:
        """Return sexagesimal floating value of object

        :param r: index of reference unit in uname, defaults to 0
        :type r: int, optional
        :return: sexagesimal floating value of object
        :rtype: BabN | None
        """
        return BabN(self.dec) // self.cfact[r]

    def abstract(self, r: int = None) -> BabN | None:
        """Return sexagesimal floating value of object

        :param r: index of reference unit in uname, defaults to 0
        :type r: int, optional
        :return: sexagesimal floating value of object
        :rtype: BabN | None
        """
        r = r or self.ubase
        return BabN(self.dec) // self.cfact[r]

    def metval(self) -> BabN | None:
        """Returns metrological value of object

        :return: metrological value of object
        :rtype: BabN | None
        """
        return self.sex(r=self.ubase)

    def explain(self) -> None:
        """Print some information about the object"""
        print(f"This is a {self.title}: {self}")
        print("    Metrology: ", *self.scheme())
        print(f"    Factor with unit '{self.uname[0]}': ", *self.cfact)
        print(
            f"Measurement in terms of the smallest unit: {self.dec} ({self.uname[0]})"
        )
        print(f"Sexagesimal floating value of the above: {self.sex(0)}")
        print(f"Approximate SI value: {self.SI()}")

    def pure_sex(self) -> str:
        """Returns the pure numerical representation without unit names.

        :return: pure numerical representation without unit names
        :rtype: str
        """
        # For BsyG this would return "9:1:5" instead of "9 bur 1 ese 5 iku"
        return ":".join(str(v) for v in reversed(self.list)).strip("0:") or "0"

    def prtf(self, onesixth: bool = False, actual: bool = False) -> str:
        """Alternative to __repr__() to use the fractions 1/3, 1/2, 2/3, 5/6 of
        the units in the output. Modified version for v1.4.0: Integrates with
        MesoInterpreter's scholastic systems (C and S)

        :onesixth: Adds 1/6 to the previous set of fractions if True
        :type onesixth: bool, (default = False)
        :actual: if True, uses academic unit names on output
        :type actual: bool, (default: False)
        """
        length = len(self.list)
        # ll = self.list.copy()
        # ff = ["" for i in range(length)]

        # 1. Fraction detection logic
        ll, ff, _ = self._get_decomposed_data(onesixth)

        # 2. Construction of value strings
        threshold = getattr(self, "sex_threshold", 0)

        for i in range(length):
            value_str = ""
            if ll[i] != 0 or ff[i] != "":
                if ll[i] != 0:
                    # --- IMPROVEMENT: We respect prtsex and C/S Systems ---
                    if not self.prtsex:
                        value_str = str(ll[i])
                    else:
                        # If unit >= threshold or value >= 60 -> System S
                        if i >= threshold or ll[i] >= 60:
                            # Final recommended version for prtf and __repr__
                            if hasattr(self, "sexsys") and self.sexsys:
                                # We use the "place value" (BabN) representation for the inside
                                # of the parentheses, avoiding unit names that break the parser.
                                val_obj = self.sexsys(ll[i])
                                value_str = f"({val_obj.pure_sex()})"
                            else:
                                value_str = f"({BsyC(ll[i])})"

                # We combine the value (if it exists) with the fraction found
                if ff[i] != "":
                    ff[i] = (value_str + " " + ff[i]).strip()
                else:
                    ff[i] = value_str

        # 3. Final assembly
        ss = []
        names = self.aname if actual else self.uname
        for i in reversed(range(length)):
            if ff[i] != "":
                ss.append(f"{ff[i]} {names[i]}")

        return " ".join(ss)

    @staticmethod
    def _to_Cunei_base(val: int, system: str = "S") -> str:
        """MATHEMATICAL ENGINE: Converts an integer to hierarchical NPVN glyphs.
        Does not add unit logograms or determinatives.

        :param val: integer to convert
        :type val: int
        :param system: system to use C, S, G, K, defaults to "S"
        :type system: str, optional
        :return: cuneiform string representation of the integer
        :rtype: str
        """
        from .glyphs import (
            l_as,
            l_dis,
            l_u,
            l_ges,
            l_gesu,
            l_sar2,
            l_saru,
            l_sar2_gal,
            l_iku,
            l_ese3,
            l_buru,
        )

        if val == 0:
            return ""
        res = []
        rem = val

        # 1. ŠAR2-GAL (216,000 / 108,000)
        f_sgal = 216000 if system != "G" else 108000
        if rem >= f_sgal:
            n = rem // f_sgal
            res.append(l_sar2_gal[0] * n)
            rem %= f_sgal

        # 2. ŠAR'U (36,000 / 18,000)
        f_sharu = 36000 if system != "G" else 18000
        if rem >= f_sharu:
            n = rem // f_sharu
            if n <= 5:
                res.append(l_saru[n - 1])
            rem %= f_sharu

        # 3. ŠAR2 (3,600 / 1,800)
        f_sar2 = 3600 if system != "G" else 1800
        if rem >= f_sar2:
            n = rem // f_sar2
            if n <= 9:
                res.append(l_sar2[n - 1])
            rem %= f_sar2

        if system == "G":
            # BUR'U (180), BUR3 (18), EŠE3 (6), IKU (1)
            factors = [(180, l_buru, 5), (18, l_u, 9), (6, l_ese3, 2), (1, l_iku, 5)]
            for f, glyphs, limit in factors:
                if rem >= f:
                    n = rem // f
                    if n <= limit:
                        res.append(glyphs[n - 1])
                    rem %= f
        else:
            # GEŠ'U (600), GEŠ (60), U (10), Unidades (1)
            factors = [(600, l_gesu, 5), (60, l_ges, 9), (10, l_u, 9)]
            for f, glyphs, limit in factors:
                if rem >= f:
                    n = rem // f
                    if n <= limit:
                        res.append(glyphs[n - 1])
                    rem %= f
            if rem >= 1:
                u_list = l_as if system == "S" else l_dis
                if rem <= 9:
                    res.append(u_list[rem - 1])

        return " ".join(res)

    def to_cunei(self, **kwargs) -> str:
        """
        INTERFACE FOR NUMERIC CLASSES (BsyS, BsyK, BsyG, BsyC).
        Adds historical disambiguation and determinants.
        """
        from .glyphs import MAP_UNIT_LOGOGRAMS, subsdict

        out = []
        stroke = kwargs.get("stroke", False)
        subst = kwargs.get("subst", None)

        # self.list es la lista sexagesimal posicional
        for i in reversed(range(len(self.list))):
            val = self.list[i]
            unit_key = self.uname[i]
            if val > 0:
                block = self._to_Cunei_base(int(val), system=self.system_type)
                # D. Desambiguación Histórica: 60 su-si
                if (
                    unit_key == "ges"
                    and i + 1 < len(self.list)
                    and self.list[i - 1] == 0
                ):
                    out.append(f"{block} {MAP_UNIT_LOGOGRAMS['susi']}")
                else:
                    out.append(block)
            elif stroke:
                out.append("𒃵")

        res = " ".join(out)
        if subst:
            glyph = subsdict.get(subst.lower(), "")
            if glyph:
                res += f" {glyph}"
        return res.strip()

    def _get_decomposed_data(self, onesixth=False) -> tuple[list, list]:
        """Decompose the list of coefficients into two, one of them for fractional parts.

        :param onesixth: Adds 1/6 to the previous set of fractions if True, defaults to False
        :type onesixth: bool, optional
        :return: tuple of lists
        :rtype: tuple[list, list]
        """
        fdic = fdic1 if onesixth else fdic0
        length = len(self.list)
        ll = self.list.copy()
        ff = ["" for i in range(length)]
        is_numeric_system = self.__class__.__name__.startswith("Bsy")
        if is_numeric_system:
            return ll, ff, self.uname

        # 1. Fraction detection logic
        for i in range(length - 1):
            k = self.ufact[i]
            if k in fdic:  # We avoid errors if the factor is not in the dictionary
                zfrac, z = fdic[k]
                for j in range(len(z)):
                    if ll[i] >= z[j]:
                        ll[i] -= z[j]
                        ff[i + 1] = zfrac[j]
                        break
        return ll, ff, self.uname

    def __repr__(self, actual: bool = False) -> str:
        """Returns string representation of object.

        :param actual: use academic names if True, defaults to False
        :type actual: bool, optional
        :return: object representation
        :rtype: str
        """
        names = self.aname if actual else self.uname
        ss = []
        for i in reversed(range(len(names))):
            if self.list[i] != 0:
                if not self.prtsex:
                    ss.append(str(self.list[i]))
                    ss.append(names[i])
                else:
                    if self.list[i] >= 60:
                        ss.append(
                            str(self.list[i] // 60) + ":" + str(self.list[i] % 60)
                        )
                    else:
                        ss.append(str(self.list[i]))
                    ss.append(names[i])
        return " ".join(ss)


class BsyG(_MesoM):  # Babylonian System G numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-G (GAN2) numeration

        **šar2-gal <-6- šar'u <-10- šar2 <-6- bur'u <-10- bur3 <-3- eše3 <-6- iku**

    """

    title: str = "Babylonian System G to count objects"
    uname: list[str] = "iku ese bur buru sar saru sargal".split()
    aname: list[str] = "iku eše3 bur3 bur'u šar2 šar'u šar2-gal".split()
    ufact: list[int] = [6, 3, 10, 6, 10, 6]
    cfact: list[int] = [1, 6, 18, 180, 1080, 10800, 64800]
    siv: float = 1
    siu: str = "#"
    ubase: int = 0  # iku
    dic_cfact = {
        "iku": 1,
        "ese": 6,
        "bur": 18,
        "buru": 180,
        "sar": 1080,
        "saru": 10800,
        "sargal": 64800,
    }
    system_type: str = "G"


class BsyS(_MesoM):  # Babylonian System S numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-S (Sexagesimal) numeration

        **šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- aš**

    """

    title: str = "Babylonian System S to count objects"
    uname: list[str] = "as u ges gesu sar saru sargal".split()
    aname: list[str] = "aš u geš geš'u šar2 šar'u šar2-gal".split()
    ufact: list[int] = [10, 6, 10, 6, 10, 6]
    cfact: list[int] = [1, 10, 60, 600, 3600, 36000, 216000]
    siv: float = 1
    siu: str = "#"
    ubase: int = 0  # as
    dic_cfact = {
        "as": 1,
        "u": 10,
        "ges": 60,
        "gesu": 600,
        "sar": 3600,
        "saru": 36000,
        "sargal": 216000,
    }
    system_type: str = "S"


class BsyK(_MesoM):  # Babylonian System SKL numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-SKL (Sumerian King List) numeration

        **šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš**

    """

    title: str = "Babylonian System SKL to count years"
    uname: list[str] = "dis u ges gesu sar saru sargal".split()
    aname: list[str] = "diš u geš geš'u šar2 šar'u šar2-gal".split()
    ufact: list[int] = [10, 6, 10, 6, 10, 6]
    cfact: list[int] = [1, 10, 60, 600, 3600, 36000, 216000]
    siv: float = 1
    siu: str = "#"
    ubase: int = 0  # as
    dic_cfact = {
        "dis": 1,
        "u": 10,
        "ges": 60,
        "gesu": 600,
        "sar": 3600,
        "saru": 36000,
        "sargal": 216000,
    }
    system_type: str = "K"


class BsyC(_MesoM):  # Babylonian System C numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-C (Common) numeration

        **u <-10- diš**

    """

    title: str = "Babylonian System S to count objects"
    uname: list[str] = "dis u".split()
    aname: list[str] = "diš u".split()
    ufact: list[int] = [10]
    cfact: list[int] = [1, 10]
    siv: float = 1
    siu: str = "#"
    ubase: int = 0  # dis
    system_type: str = "C"


class MesoM(_MesoM):
    """This class complements the _MesoN class by allowing you to express unit
    coefficients in measurements using the S and G systems as appropriate. It
    introduces the sexsys attribute and enhances the __repr__ method."""

    sexsys: type[BsyS] | type[BsyG] = BsyS

    @classmethod
    def lookup(
        cls,
        value: str | int,
        ubase: int = None,
        strict: bool = False,
        width: int = 20,
        fractions: int = -1,
        academic: bool = False,
        verbose: bool = False,
        translit: bool = False,
        cuneiform: bool = False,
    ):
        """
        Performs a reverse metrological search. Given an abstract sexagesimal
        number, it lists all possible physical measurements within the class
        that correspond to that number at different orders of magnitude.

        :param value: The abstract sexagesimal value to look up (e.g., '20' or 20).
        :type value: str | int
        :param ubase: Index of the reference unit for the abstract value. Defaults to cls.ubase.
        :type ubase: int, optional
        :param strict: If True, only matches where the sexagesimal representation is identical.
        :type strict: bool, optional
        :param width: Character width for the measurement column in the output table.
        :type width: int, optional
        :param fractions: Number of fractional parts to show. -1 for default representation.
        :type fractions: int, optional
        :param academic: Use academic notation (e.g., using ';' for sexagesimal fractions).
        :type academic: bool, optional
        :param verbose: If True, provides detailed info including SI equivalents.
        :type verbose: bool, optional
        :param translit: If True, displays the measurement in Nippur-style transliteration.
        :type translit: bool, optional
        :param cuneiform: If True, displays both measurement and abstract value in Unicode cuneiform.
        :type cuneiform: bool, optional
        """
        from .utils import cunei_ljust as padc

        if ubase is None:
            ubase = cls.ubase

        # Convert search value to a Babylonian Number object for decimal access
        aa = BabN(value)
        # x is the target 'decimal footprint' in the smallest unit
        x = aa.dec * cls.cfact[ubase]

        line = f"\nLooking for {cls.title} with Abstract = {aa}"
        print(line)
        print(f"Base reference unit: {cls.uname[ubase]}")
        print("-" * len(line))

        # Iterating through 8 orders of magnitude (from 60^-3 to 60^4)
        for i in range(-3, 5):
            # Calculate potential decimal value for this magnitude
            val_dec = int(x // 60**i)
            if val_dec < 1:
                continue  # Skip magnitudes that result in zero

            obj = cls(val_dec)

            # Format the measurement string
            if translit:
                medida_str = obj.translit
            elif cuneiform:
                medida_str = obj.cuneiform
            else:
                medida_str = (
                    obj.prtf(fractions, academic) if fractions >= 0 else str(obj)
                )

            # Get the abstract sexagesimal representation for the found measurement
            abstracto = obj.sex(ubase)

            # Strict filter: ensures the string representation matches exactly
            if strict and str(aa) != str(abstracto):
                continue

            # Handle Cuneiform output for the abstract column
            if cuneiform:
                abstracto_print = abstracto.to_cunei(alter=True)
            else:
                abstracto_print = abstracto

            if verbose:
                print(f"Measure:   {medida_str}")
                print(f"Equiv.:    {obj.SI()}")
                print(f"Abstract:  {abstracto_print}\n")
            else:
                print(
                    f"{padc(medida_str, width) if cuneiform else medida_str.ljust(width)} <- {abstracto_print}"
                )

    @classmethod
    def metro_generator(
        cls,
        mmin: str | int,
        mmax: str | int | list,
        step: str | int | list,
        verbose: bool = False,
        ubase: int | None = None,
        width: int = 20,
        fractions: int = -1,
        actual: bool = False,
        translit: bool = False,
        cuneiform: bool = False,
        subst: str = "",
        incipit: bool = False,
        **kwargs,
    ):
        """
        Generator that yields formatted metrological strings line by line.


        :param mmin: Initial value (e.g., '1 ninda' or integer)
        :type mmin: str | int
        :param mmax: Final value
        :type mmax: str | int
        :param step: Increment
        :type step: str | int
        :param verbose: If it is True, it returns the floating metrological value, defaults to False
        :type verbose: bool, optional
        :param ubase: force ubase unit, defaults to None
        :type ubase: int, optional
        :param width: output width, defaults to 20
        :type width: int, optional
        :param fractions: Use fractions if 1 and add 1/6 if 2, defaults to -1 (no fractions)
        :type fractions: int, optional
        :param actual: use academic unit names
        :type actual: bool, optional
        :param echo: If True, prints the table to stdout. If False, only returns the list.
        :type echo: bool, optional
        :param translit: If True, prints the table in transliteration.
        :type translit: bool, optional
        :param cuneiform: If True, prints the table in cuneiform.
        :type cuneiform: bool, optional
        :param subst: add substance glyph to line
        :type subst: str, optional
        :param incipit: write subst on first line only, defaults to False
        :type incipit: bool, optional
        :yields: str (Each row of the table)
        """
        from .glyphs import IGI_NU
        from .glyphs import subsdict
        from .utils import cunei_ljust as padc
        from .utils import gen_multi_range

        # 1. Setup sequence (using the gen_multi_range generator)
        decimal_sequence = gen_multi_range(cls, mmin, mmax, step)

        if ubase is None:
            ubase = cls.ubase
        # First row
        fr = True

        # --- Main Generator Loop ---
        for dec_val, linenumber, subtotal, is_new_section in decimal_sequence:
            obj = cls(int(round(dec_val)))
            use_fracs = fractions >= 1
            use_onesixth = fractions == 2

            # Column 1
            if cuneiform:
                if subst:
                    subst= subsdict.get(subst, subst)

                if incipit:
                    val1 = (
                        obj.cuneiform + f" {subst}" if is_new_section else obj.cuneiform
                    )
                else:
                    val1 = obj.cuneiform + f" {subst}"
                col1 = f"|{padc(val1, width - 1)} "
            elif translit:
                if incipit:
                    val1 = (
                        obj.translit + f" {subst}" if is_new_section else obj.translit
                    )
                else:
                    val1 = obj.translit + f" {subst}"
                col1 = f"|{padc(val1, width - 1)} "
            else:
                val1 = (
                    obj.prtf(onesixth=use_onesixth, actual=actual)
                    if use_fracs
                    else obj.__repr__(actual=actual)
                )
                if incipit:
                    val1 += (
                        f" {'' if subst is None else subst}" if is_new_section else ""
                    )
                else:
                    val1 += f" {'' if subst is None else subst}" if fr else ""
                col1 = f"|{val1.ljust(width - 1)} "

            # Additional Columns
            if verbose:
                sex_obj = obj.sex(r=ubase)
                if cuneiform:
                    val2 = f"| {padc(sex_obj.to_cunei(alter=True), 15)} "
                    recip_val = (
                        sex_obj.rec().to_cunei(alter=True, stroke=True)
                        if sex_obj.isreg
                        else IGI_NU  # "𒅆𒉡" i.e. "--igi nu--"
                    )
                    col3 = f"| {padc(recip_val, 11)} "
                else:
                    val2 = f"| {str(sex_obj).ljust(15)} "
                    recip_val = str(sex_obj.rec()) if sex_obj.isreg else "--igi nu--"
                    col3 = f"| {recip_val.ljust(11)} "
                line = col1 + val2 + col3 + "|"
            else:
                line = col1 + "|"

            fr = False
            yield (line, linenumber, subtotal, is_new_section)

    @classmethod
    def metrolist(cls, *args, **kwargs):
        """Generate a list of metrological values for the current class.
        Now supports multi-range sections by passing lists to mmax and step.
        Accepts the same arguments as `metro_generator` and some that are specific to it.

        """
        from .glyphs import MAP_UNIT_LOGOGRAMS

        metrolist = cls.metro_generator(*args, **kwargs)

        width = kwargs.get("width", 20)
        actual = kwargs.get("actual", False)
        cuneiform = kwargs.get("cuneiform", False)
        verbose = kwargs.get("verbose", False)

        ubase = cls.ubase if kwargs.get("ubase") is None else kwargs["ubase"]

        # --- Header Management ---
        print("\n" + cls.title)
        print(*cls.scheme(actual=actual, cuneiform=cuneiform))

        # Column 1: Measurement label
        h1 = f"|{'Measurement'.ljust(width - 1)} "

        if verbose:
            # Column 2: Sexagesimal representation
            if cuneiform:
                ubase_name = (
                    cls.cname()[ubase]
                    if hasattr(cls, "cname")
                    else MAP_UNIT_LOGOGRAMS.get(cls.uname[ubase], cls.uname[ubase])
                )
                h2 = f"| {f'Sexag. ({ubase_name} )'.ljust(15)} "
                h3 = f"| {'Reciprocal'.ljust(11)} "
            else:
                u_label = cls.aname[ubase] if actual else cls.uname[ubase]
                h2 = f"| {f'Sexag. ({u_label})'.ljust(15)} "
                h3 = f"| {'Reciprocal'.ljust(11)} "
            header_line = h1 + h2 + h3 + "|"
        else:
            header_line = h1 + "|"

        print(header_line)

        # Dynamic separator line
        sep = "|" + "-" * (len(h1) - 1) + "|"
        if verbose:
            sep += "-" * (len(h2) - 1) + "|" + "-" * (len(h3) - 1) + "|"
        print(sep)

        # --- Main Loop ---
        # Iterate through the sequence generated by gen_multi_range

        # for dec_val in decimal_sequence:
        for line, linecount, subtotal, is_new_section in metrolist:
            print(line)

        # Colophon:
        if kwargs.get("colophon"):
            print(cls._draw_colophon(subtotal, linecount, format="text", **kwargs))

    @classmethod
    def metrohtml(cls, *args, **kwargs):
        """Exports the results of `metrolist` to a basic HTML table.
        Accepts the same arguments as `metro_generator` and some that are specific to it.

        :param file: output filename base, optional
        :type file: str, optional
        :param caption: table caption, optional
        :type caption: str, optional
        :param full_page: write a complete test HTML page instead of just the table, defaults to False
        :type full_page: bool, optional
        :return: HTML output
        :rtype: str
        """
        from itertools import chain

        # kwargs["echo"] = False
        metrolist = cls.metro_generator(*args, **kwargs)
        caption = kwargs.get("caption")
        full_page = kwargs.get("full_page", False)
        verbose = kwargs.get("verbose", False)

        ubase = cls.ubase if kwargs.get("ubase") is None else kwargs["ubase"]
        if kwargs.get("cuneiform", False):
            ubase_glyph = cls.cname()[ubase]
        elif kwargs.get("actual", False):
            ubase_glyph = cls.aname[ubase]
        else:
            ubase_glyph = cls.uname[ubase]

        # first row
        # 1. Extraemos el primer elemento para calcular columnas
        try:
            fr_data = next(metrolist)  # Tupla: (row_str, ln, sub, is_new)
        except StopIteration:
            return ""

        # 2. Re-unimos la primera fila con el resto del generador
        # Usamos chain para no agotar la memoria convirtiendo a tuple
        # full_sequence = chain([fr_data], metrolist)

        first_row = fr_data[0].strip("|").split("|")
        num_cols = len(first_row)

        html = []

        if full_page:
            # html.append("<!DOCTYPE html>\n<html>\n<head>")
            html.append('<!DOCTYPE html>\n<html lang="x-cuneiform">\n<head>')
            html.append('  <meta charset="UTF-8">')
            html.append(
                '  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Cuneiform&display=swap" rel="stylesheet">'
            )
            html.append("  <style>")
            html.append(
                "    body { background-color: #f4f1ea; font-family: sans-serif; display: flex; justify-content: center; padding: 20px; }"
            )
            html.append(
                "    .tablet { background-color: #e2c08d; border-radius: 15px; padding: 25px; "
            )
            html.append(
                "              box-shadow: inset 2px 2px 5px #bc9a6c, 5px 5px 15px rgba(0,0,0,0.3);"
            )
            html.append(
                "              border: 1px solid #cdaa7d; max-width: fit-content; }"
            )
            html.append(
                "    table { border-collapse: collapse; background: rgba(255,255,255,0.1); }"
            )
            html.append(
                "    th, td { border: 1px solid rgba(0,0,0,0.1); padding: 8px 15px; text-align: left; }"
            )
            html.append(
                "    th { background: rgba(0,0,0,0.05); color: #5d4037; font-variant: small-caps; }"
            )
            html.append(
                '    td { font-family: "Noto Sans Cuneiform", sans-serif; font-size: 1.2rem; }'
            )
            html.append(
                "    caption { margin-bottom: 10px; font-weight: bold; color: #5d4037; }"
            )
            html.append("  </style>\n</head>\n<body>")

        if kwargs.get("cuneiform", False):
            html.append('<div class="tablet">')
            html.append('  <table class="table">')
            cuneiform = True
        else:
            html.append("  <table>")
            cuneiform = False

        # Add the caption if there is one
        if caption:
            html.append(f"  <caption>{caption}</caption>")

        # Header
        html.append("  <tr>")
        html.append("    <th>Measurement</th>")
        # Future
        if num_cols > 2:
            html.append(f"    <th>Sexag. ({ubase_glyph})</th>") if verbose else None
            html.append("    <th>Reciprocal</th>")
        html.append("  </tr>")

        # Rows
        # Add the first row that we extracted for the count
        rows_iterator = chain([fr_data], metrolist)
        # 3. El bucle es ahora sagrado y único
        for row_str, linecount, subtotal, is_new_section in rows_iterator:
            # Limpiamos la fila de los separadores de la consola
            cells = row_str.strip("|").split("|")

            # Si es nueva sección, podemos añadir un estilo visual
            # (ln es tu contador manual, linecount es el que viene del generador)
            tr_style = (
                ' style="border-top: 2px solid #5d4037;"'
                if is_new_section and linecount > 0
                else ""
            )

            html.append(f"  <tr{tr_style}>")
            for cell in cells:
                clean_cell = cell.strip().replace("\u2009", "&thinsp;")
                html.append(f"    <td>{clean_cell}</td>")
            html.append("  </tr>")

        # Colophon
        if kwargs.get("colophon"):
            html.append(
                cls._draw_colophon(
                    subtotal, linecount, format="html", num_cols=num_cols, **kwargs
                )
            )

        # Closing
        if cuneiform:
            html.extend(["</table>", "</div>"])
        else:
            html.append("</table>")

        if full_page:
            html.append("</body>\n</html>")

        final_html = "\n".join(html)

        # File writing
        if kwargs.get("file", False):
            file = kwargs["file"]
            if cuneiform:
                table_class = "tablet"
            else:
                table_class = "raw"

            with open(file + ".html", "w", encoding="utf-8") as f:
                f.write(final_html)
            print(
                f"--> Exported {linecount} rows to '{file + '.html'}' ({table_class} style)"
            )
        else:
            return final_html

    @classmethod
    def metrolatex(cls, *args, **kwargs):
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        from itertools import chain
        from .utils import to_latex_hex

        # 1. Obtenemos el generador
        metrolist = cls.metro_generator(*args, **kwargs)
        caption = kwargs.get("caption")
        full_page = kwargs.get("full_page", False)
        is_cuneiform = kwargs.get("cuneiform", False)

        # 2. Extraemos la primera fila para configurar la tabla
        try:
            fr_data = next(metrolist)  # (row_str, linenum, subtotal, is_new)
        except StopIteration:
            return ""

        row_str_0, ln_0, sub_0, new_0 = fr_data
        first_row_cells = row_str_0.strip("|").split("|")
        num_cols = len(first_row_cells)
        align = "l" * num_cols

        latex = []
        if full_page:
            latex.append(r"\documentclass{article}")
            latex.append(r"\usepackage{booktabs}")
            latex.append(r"\usepackage{fontspec}")
            latex.append(r"% Make sure to upload NotoSansCuneiform.ttf to Overleaf")
            latex.append(r"\newfontfamily\cuneifont{NotoSansCuneiform.ttf}[Path = .//]")
            latex.append(r"\begin{document}")

        latex.append(r"\begin{table}[h]")
        latex.append(r"  \centering")
        if caption:
            latex.append(f"  \\caption{{{caption}}}")

        latex.append(f"  \\begin{{tabular}}{{{align}}}")
        latex.append(r"    \toprule")

        # Headers
        ubase = cls.ubase if kwargs.get("ubase") is None else kwargs["ubase"]
        u_raw = cls.cname()[ubase] if is_cuneiform else cls.uname[ubase]
        u_glyph = to_latex_hex(u_raw)

        # Lógica de headers corregida para usar num_cols
        # 1. Definimos los textos base (sin fuentes todavía)
        headers = ["Measurement"]
        if num_cols == 2:
            # Separamos el texto de la unidad: solo la unidad irá en cuneiforme
            unit_part = (
                f" ({{\\cuneifont {u_glyph}}})" if is_cuneiform else f" ({u_glyph})"
            )
            headers.append(f"Sexag.{unit_part}")
        elif num_cols > 2:
            unit_part = (
                f" ({{\\cuneifont {u_glyph}}})" if is_cuneiform else f" ({u_glyph})"
            )
            headers.append(f"Sexag.{unit_part}")
            headers.append("Reciprocal")

        # 2. Aplicamos formato a los headers
        # Usamos \textsf o \textbf para que los encabezados tengan peso,
        # pero mantenemos la fuente del documento (Times/Computer Modern)
        # formatted_headers = [f"\\textsf{{{h}}}" for h in headers]

        # 3. Unimos para LaTeX
        # latex.append("    " + " & ".join(formatted_headers) + r" \\")

        latex.append("    " + " & ".join(headers) + r" \\")
        latex.append(r"    \midrule")

        # 3. Bucle de filas usando chain para evitar duplicados
        rows_iterator = chain([fr_data], metrolist)

        for row_str, linecount, subtotal, is_new_section in rows_iterator:
            # Si es una nueva sección y NO es la primera línea,
            # añadimos un pequeño separador visual en LaTeX
            if is_new_section and linecount > 0:
                latex.append(r"    \addlinespace[0.5em]")

            cells = [c.strip() for c in row_str.strip("|").split("|")]

            if is_cuneiform:
                # Convertimos y aplicamos la fuente a cada celda
                formatted_cells = [f"{{\\cuneifont {to_latex_hex(c)}}}" for c in cells]
            else:
                # En modo normal, escapamos caracteres de LaTeX si fuera necesario
                formatted_cells = [c.replace("_", r"\_") for c in cells]

            latex.append("    " + " & ".join(formatted_cells) + r" \\")

        latex.append(r"    \bottomrule")
        if kwargs.get("colophon"):
            latex.append(
                cls._draw_colophon(
                    subtotal, linecount, format="latex", num_cols=num_cols, **kwargs
                )
            )
        latex.append(r"  \end{tabular}")
        latex.append(r"\end{table}")

        if full_page:
            latex.append(r"\end{document}")

        final_latex = "\n".join(latex)

        if kwargs.get("file"):
            filename = kwargs["file"] + ".tex"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_latex)
            print(
                f"--> Exported {linecount} rows to '{filename}' (LaTeX HEX-Safe style)"
            )
        else:
            return final_latex

    @classmethod
    def metrocsv(cls, *args, **kwargs):
        """Exports the results of `metrolist` to a CSV file.
        Accepts the same arguments as `metro_generator` and some that are specific to it.

        :param file: output filename base, defaults to 'output'
        :type file: str, optional
        """
        from itertools import chain
        import csv

        file = kwargs.get("file", "output")

        # Generate table
        metrolist = cls.metro_generator(*args, **kwargs)

        # ubase_glyph for header
        ubase = cls.ubase if kwargs.get("ubase") is None else kwargs["ubase"]
        if kwargs.get("cuneiform", False):
            ubase_glyph = cls.cname()[ubase]
        elif kwargs.get("actual", False):
            ubase_glyph = cls.aname[ubase]
        else:
            ubase_glyph = cls.uname[ubase]

        # First row
        # We extract the first element to calculate columns
        try:
            fr_data = next(metrolist)  # Tuple: (row_str, ln, sub, is_new)
        except StopIteration:
            return ""
        first_row = fr_data[0].strip("|").split("|")
        num_cols = len(first_row)

        # 2. Join the first row with the rest of the generator
        # We use chain to avoid exhausting memory by converting to tuple
        # full_sequence = chain([fr_data], metrolist)
        rows_iterator = chain([fr_data], metrolist)

        filename = file + ".csv"
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Headers
            if num_cols == 1:
                writer.writerow(["Measurement"])
            else:
                writer.writerow(
                    ["Measurement", f"Sexag. ({ubase_glyph})", "Reciprocal"]
                )
            # Rows
            for row_str, linecount, subtotal, is_new_section in rows_iterator:
                # Row cleaning
                cells = [_.strip() for _ in row_str.strip("|").split("|")]
                writer.writerow(cells)
        print(f"--> Exported {linecount} rows to '{filename}'")

    def prtf(self, onesixth: bool = False, actual: bool = False) -> str:
        """
        Print metrological values using fractions
        Revised version for MesoMath v2.0.0

        :param onesixth: include 1/6 fractions, defaults to False
        :type onesixth: bool, optional
        :param actual: use academic unit names, defaults to False
        :type actual: bool, optional
        :return: output string
        :rtype: str
        """
        """
        Revised version for MesoMath v2.0.0: 
        """
        length = len(self.list)

        # 1. We obtain broken down data (values, fractions, and unit names)
        ll, ff, _ = self._get_decomposed_data(onesixth)

        # 2. Threshold for the Golden Rule
        threshold = getattr(self, "sex_threshold", 0)

        # 3. Construction of value strings
        for i in range(length):
            if ll[i] != 0 or ff[i] != "":
                # CASE A: Simple Decimal Representation
                if not self.prtsex:
                    value_str = str(ll[i]) if ll[i] != 0 else ""

                # CASE B: Sexagesimal Representation (in parentheses)
                else:
                    if ll[i] == 0:
                        value_str = ""
                    else:
                        # We determine which numeric class to use
                        if i < threshold and ll[i] < 60:
                            num_obj = BsyC(ll[i])
                        elif hasattr(self, "sexsys"):
                            num_obj = self.sexsys(ll[i])
                        else:
                            num_obj = self.__class__(ll[i])

                        # We call prtf(0, actual) of the numeric object
                        # so that it uses 'eše3' and 'diš' if actual=True
                        value_str = f"({num_obj.__repr__(actual)})"

                # Join the value (whether decimal or sexagesimal) with its fraction
                if ff[i] != "":
                    ff[i] = (value_str + " " + ff[i]).strip()
                else:
                    ff[i] = value_str

        # 4. Final assembly (from largest to smallest)
        ss = ""
        for i in reversed(range(length)):
            if ff[i] != "":
                # We select the name of the unit (Academic or Common)
                unit_label = self.aname[i] if actual else self.uname[i]
                ss += f"{ff[i]} {unit_label} "

        return ss.strip()

    def labor_cost(self, work_man: str | int) -> float:
        """Calculate the number of workdays or man-days required for the task.

        :param work_man: work done in a day by worker
        :type work_man: str | int
        :return: number of workdays or man-days
        :rtype: float
        """
        try:
            wm = self.__class__(work_man)
            return self.dec / wm.dec
        except (ValueError, ZeroDivisionError) as e:
            # More specific error handling
            raise ValueError(f"Error in cost calculation: {e}")

    def rations(self, work_man: str | int, wage: str | int) -> "Bcap":
        """Calculate the cost of the work when payment is in capacity units

        :param work_man: work done in a day by worker (magnitude of current class)
        :type work_man: str | int
        :param wage: dayly payment for worker (grain, beer, etc. in capacity units)
        :type wage: str | int
        :return: total amount to pay
        :rtype: Bcap
        """
        from mesomath.npvs import Bcap

        try:
            # 1. We convert inputs into metrological objects
            wm = self.__class__(work_man)
            wg = Bcap(wage)

            # 2. We calculate exact wages (float)
            # We do not round here to allow proportional payments
            workdays = self.dec / wm.dec

            # 3. Final calculation of the total grain
            # We multiply the float by the minimum unit of the salary
            # We round only at the end to get an integer of 'se'
            total_se = int(round(workdays * wg.dec))

            return Bcap(total_se)

        except (ValueError, ZeroDivisionError) as e:
            # More specific error handling
            raise ValueError(f"Error in rations calculation: {e}")

    def silver_payments(self, work_man: str | int, wage: str | int) -> "Bwei":
        """Calculate the cost of the work when payment is in silver (weight).

        :param work_man: work done in a day by worker (magnitude of current class)
        :type work_man: str | int
        :param wage: dayly payment for worker (in silver weight units, e.g., '8 se')
        :type wage: str | int
        :return: total amount of silver to pay
        :rtype: Bwei
        """
        from mesomath.npvs import Bwei

        try:
            # 1. We convert inputs into metrological objects
            wm = self.__class__(work_man)
            wg = Bwei(wage)

            # 2. We calculate exact wages (float)
            # We do not round here to allow proportional payments
            workdays = self.dec / wm.dec

            # 3. Final calculation of the total silver payment
            # We multiply the float by the minimum unit of the salary
            # We round only at the end to get an integer of 'se'
            total_se = int(round(workdays * wg.dec))

            return Bwei(total_se)

        except (ValueError, ZeroDivisionError) as e:
            # More specific error handling
            raise ValueError(f"Error in silver payment calculation: {e}")

    def to_cunei(self, **kwargs) -> str:
        """
        INTERFAZ PARA CLASES METROLÓGICAS (Bcap, Bsur, Bwei, etc.).
        Usa descomposición por unidades y fracciones.
        """
        from .glyphs import MAP_UNIT_LOGOGRAMS, MAP_FRACTIONS, subsdict

        # onesixth = self.__class__.__name__ in ["Bsur", "Bvol", "Bbri"]
        onesixth = kwargs.get("onesixth", False)
        ll, ff, uname = self._get_decomposed_data(onesixth=onesixth)
        subst = kwargs.get("subst", None)
        stroke = kwargs.get("stroke", False)
        out = []

        for i in reversed(range(len(ll))):
            val, frac_str, unit = ll[i], ff[i], uname[i]
            parts = []

            if val > 0:
                # Determinamos sistema para el coeficiente
                target = (
                    "G"
                    if unit == "gan"
                    else ("K" if self.__class__.__name__ == "BsyK" else "S")
                )
                parts.append(self._to_Cunei_base(int(val), system=target))

            if frac_str:
                parts.append(MAP_FRACTIONS.get(frac_str, frac_str))

            block = " ".join(parts)
            unit_glyph = MAP_UNIT_LOGOGRAMS.get(unit, unit)

            if block:
                out.append(f"{block} {unit_glyph}")
            elif stroke:
                out.append(f"𒃵 {unit_glyph}")

        res = " ".join(out)
        if subst:
            glyph = subsdict.get(subst.lower(), "")
            if glyph:
                res += f" {glyph}"
        return res.strip()

    @classmethod
    def _draw_colophon(cls, subtotal, linecount, **kwargs):
        """
        Internal helper to generate the administrative closing (Shu-nigin).
        """
        from datetime import datetime
        from .utils import to_latex_hex  # Aseguramos el acceso a la utilidad
        from .glyphs import MAP_ADMIN, subsdict
        from .__about__ import __version__ as VERSION

        # 1. Setup de datos básicos
        subst = kwargs.get("subst", "")
        is_cunei = kwargs.get("cuneiform", False)
        translit = kwargs.get("translit", False)
        fmt = kwargs.get("format", "text")
        year = datetime.now().year
        month = datetime.now().month
        version = f"MesoMath {VERSION}"
        num_cols = kwargs.get("num_cols", 2)

        # 2. Construcción de etiquetas y valores
        if is_cunei:
            # Nota: BsyS y BsyK asumen que están disponibles o importados
            total_str = f"{cls(int(subtotal)).to_cunei()} {subsdict.get(subst, '')}"
            lines_str = f"{BsyS(linecount).to_cunei()}"
            date_str = f"{MAP_ADMIN['iti']} {BsyS(month).to_cunei()} {BsyK(year).to_cunei()} {MAP_ADMIN.get('mu', '𒈬')}"
            scribe_label = MAP_ADMIN["dub-sar"]
            total_label = MAP_ADMIN["su_ningin_gal"]
            lines_label = MAP_ADMIN["mu_sid_bi"]
        else:
            total_str = f"{cls(int(subtotal)).translit if translit else cls(int(subtotal)).prtf()} {subst}"
            lines_str = str(linecount)
            date_str = datetime.now().strftime("%B %Y")
            scribe_label = "Scribe"
            total_label = "Grand Total"
            lines_label = "Number of lines"

        # 3. Renderizado según formato con protección para LaTeX
        res = []

        if fmt == "text":
            res.append("-" * 50)
            res.append(f"| {total_label}: {total_str}")
            res.append(f"| {lines_label}: {lines_str} | {scribe_label}: {version} |")
            res.append(f"| {date_str} |")
            res.append("-" * 50)

        elif fmt == "html":
            res.append(
                '  <tfoot style="border-top: 2px solid #5d4037; font-style: italic;">'
            )
            res.append(
                f'    <tr><td colspan="{num_cols}">{total_label}: {total_str}</td></tr>'
            )
            res.append(
                f'    <tr><td colspan="{num_cols - 1}">{lines_label}: {lines_str}</td><td>{scribe_label}: {version}</td></tr>'
            )
            res.append(f'    <tr><td colspan="{num_cols}">{date_str}</td></tr>')
            res.append("  </tfoot>")

        elif fmt == "latex":
            # Función auxiliar local para envolver en fuente si es cuneiforme
            def _wrap(text):
                if is_cunei:
                    # Pasamos por el conversor HEX para seguridad de Overleaf
                    return f"{{\\cuneifont {to_latex_hex(text)}}}"
                return text.replace("_", r"\_")

            # res.append(r"    \midrule")
            # Aplicamos el envoltorio a cada línea del colofón
            line1 = f"{_wrap(total_label)}: {_wrap(total_str)}"
            line2 = rf"{_wrap(lines_label)}: {_wrap(lines_str)} \hfill {_wrap(scribe_label)}: {version}"
            line3 = f"{_wrap(date_str)}"

            res.append(f"    \\multicolumn{{{num_cols}}}{{l}}{{\\small {line1}}} \\\\")
            res.append(f"    \\multicolumn{{{num_cols}}}{{l}}{{\\small {line2}}} \\\\")
            res.append(f"    \\multicolumn{{{num_cols}}}{{l}}{{\\small {line3}}} \\\\")
            res.append(r"    \midrule")

        return "\n".join(res)

    @property
    def translit(self):
        return self._transliterate(False)

    @property
    def cuneiform(self):
        return self._transliterate(True)

    def _transliterate(self, cuneiform: bool = False, postprocess: bool = True) -> str:
        """
        Return the metrological transliteration or cuneiform representation of the object.

        This method performs a greedy decomposition of 'self.dec' into values corresponding
        to graphemes present in the Old Babylonian metrological lists published by C. Proust (2009).
        The resulting tokens are concatenated and optionally re-analyzed to regroup identical
        units and recalculate coefficients, ensuring historical accuracy in the final string.

        :param cuneiform: If True, converts the transliterated tokens into their
                          corresponding cuneiform Unicode characters.
        :type cuneiform: bool, optional
        :param postprocess: If True, performs a secondary pass to aggregate repetitive
                            minor units (e.g., 'še' grains) into single blocks.
        :type postprocess: bool, optional
        :raises AttributeError: Raised if the object's 'trmodel' is not a valid
                                Proust-based metrological model (Blen, Bsur, Bwei, Bcap).
        :return: A string containing the historical transliteration or cuneiform signs.
        :rtype: str
        """
        from mesomath.utils import translit_to_cunei
        from mesomath.data.proust import get_map_for
        import re

        # 1. Configuration & Vocabularies
        # SAFE_VOCAB: Tokens that the MesoMath string constructor can safely parse.
        SAFE_VOCAB = {
            "diš",
            "u",
            "geš2",
            "gešu",
            "šar2",
            "šar’u",
            "1/2",
            "1/3",
            "2/3",
            "5/6",
            "n",
            "m",
            "var",
        }

        # PROUST_STRUCTURAL: Units that must remain atomic and should not be fragmented by post-processing.
        PROUST_STRUCTURAL = {
            "(eše3)",
            "(iku)",
            "(ubu)",
            "(šar2)",
            "(šar’u)",
            "1(šargal)gal",
            "(diš)gal2",
        }

        # METROLOGICAL UNITS: Used for splitting and cleaning repetitive unit markers.
        UNITS = {
            "danna",
            "gal2",
            "GAN2",
            "gin2",
            "gu2",
            "gur",
            "igi",
            "kuš3",
            "ma-na",
            "ninda",
            "sar",
            "še",
            "sila3",
            "šu-si",
            "UŠ",
        }

        def clean_transliteration(text: str) -> str:
            """Removes redundant unit markers by scanning from right to left."""
            words = text.split()
            if not words:
                return ""
            cleaned = []
            last_unit_seen = None
            for word in reversed(words):
                if word in UNITS:
                    if word == last_unit_seen:
                        continue
                    last_unit_seen = word
                cleaned.append(word)
            return " ".join(reversed(cleaned))

        # 2. Metrological Model Validation
        valid_models = {"Blen", "Bsur", "Bwei", "Bcap"}
        try:
            model = self.trmodel
            if model not in valid_models:
                raise AttributeError
        except AttributeError:
            # Fallback to standard algorithm if no Proust model is defined
            return self.to_cunei() if cuneiform else self.acad

        # 3. Greedy Decomposition Algorithm
        # Consumes the decimal value using the largest available pieces from the Proust map.
        remainder = self.dec
        tokens = []
        proust_map = get_map_for(model)

        for val in proust_map:
            if remainder <= 0:
                break
            while 0 < val <= remainder:
                tokens.append(proust_map[val])
                remainder -= val
                # print(f"DEBUG: {proust_map[val]} {val} {remainder}")

        if remainder > 0:
            tokens.append(f"REMANENTE({remainder})")

        # 4. Preliminary Cleaning
        raw_text = " ".join(tokens)
        clean_text = clean_transliteration(raw_text)

        # 5. Post-processing (Refinement)
        if not postprocess:
            return clean_text

        # Use word boundaries (\b) to prevent 'še' from matching inside 'eše3'
        pattern = f"\\b({'|'.join(UNITS)})\\b"
        parts = re.split(pattern, clean_text)

        final_blocks = []
        # If the split didn't find units as independent words, it returns [clean_text]
        if len(parts) > 1:
            for i in range(0, len(parts) - 1, 2):
                num_part = parts[i].strip()
                unit_part = parts[i + 1].strip()

                words_in_block = num_part.replace("(", " ").replace(")", " ").split()
                is_safe = all(w.isdigit() or w in SAFE_VOCAB for w in words_in_block)
                is_structural = any(s_unit in num_part for s_unit in PROUST_STRUCTURAL)
                has_repetition = num_part.count("u") > 1 or num_part.count("diš") > 1

                if is_safe and has_repetition and not is_structural:
                    normalized = num_part.replace("(", " ").replace(")", "")
                    try:
                        temp_val = f"({normalized}) {unit_part}"
                        temp_obj = self.__class__(temp_val)
                        # Get refined text without unit (to avoid 'še še')
                        refined = temp_obj._transliterate(postprocess=False)
                        final_blocks.append(refined)
                    except (ValueError, Exception):
                        final_blocks.append(f"{num_part} {unit_part}")
                else:
                    # Add a space only if num_part is not empty (handles leading units)
                    block = f"{num_part} {unit_part}" if num_part else unit_part
                    final_blocks.append(block)

            # Add any trailing text after the last unit
            if parts[-1].strip():
                final_blocks.append(parts[-1].strip())

            clean_text = " ".join(final_blocks)

        # Reconstruct the final string
        clean_text = " ".join(final_blocks)

        # 6. Final Output
        return translit_to_cunei(clean_text) if cuneiform else clean_text

    def __repr__(self, actual: bool = False) -> str:
        """
        Academic representation: System C for small units, System S for large
        units or overflow values (>60).

        :param actual: use academic names, defaults to False
        :type actual: bool, optional
        :return: object representation
        :rtype: str
        """
        names = self.aname if actual else self.uname

        if not self.list or all(v == 0 for v in self.list):
            return f"0 {self.uname[0]}"

        ss = []
        # We retrieve the threshold; if it does not exist, by default it is 0 (all sexagesimal)
        threshold = getattr(self, "sex_threshold", 0)

        for i in reversed(range(len(names))):
            val = self.list[i]
            if val != 0:
                if not self.prtsex:
                    # Standard output (pure decimal)
                    ss.append(str(val))
                else:
                    # Academic Output (Scholastic)
                    # If we are above the threshold OR the value is >= 60 (problem of 180)
                    if i >= threshold or val >= 60:
                        ss.append(f"({(self.sexsys(val)).__repr__(actual)})")
                    else:
                        ss.append(f"({(BsyC(val)).__repr__(actual)})")

                ss.append(names[i])

        return " ".join(ss)


class Blen(MesoM):  # Length
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period length units

        **danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si**

    """

    title: str = "Babylonian length measurement"
    uname: list[str] = "susi kus ninda us danna".split()
    aname: list[str] = "šu-si kuš3 ninda UŠ danna".split()
    ufact: list[int] = [30, 12, 60, 30]
    cfact: list[int] = [1, 30, 360, 21600, 648000]
    sex_threshold = 5
    siv: float = 0.5 / 30
    siu: str = "meters"
    ubase: int = 2  # ninda
    trmodel: str = "Blen"  # Transliteration model

    def __mul__(self, other: object) -> object:
        """Overloads ``*`` operator: returns object with the operands product

        :param other: operand
        :type other: "Blen" or "Bsur" or float
        :return: product
        :rtype: "Bsur" | "Bvol" | "Blen"
        """
        # 1. Case: Length * Length (or subclasses) -> Area
        if isinstance(other, Blen):
            t = int(round((self.dec * other.dec) / 12.0, 0))
            return Bsur(t)
        # 2. Case: Length * Surface (or subclasses) -> Volume
        elif isinstance(other, Bsur):
            t = int(round((self.dec * other.dec) / 30.0, 0))
            return Bvol(t)
        # 3. Case: Scale (number)
        elif isinstance(other, (int, float)):
            t = self.dec * other
            return self.__class__(int(round(t, 0)))
        return NotImplemented


class Bsur(MesoM):  # Surface
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period surface units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """

    title: str = "Babylonian surface measurement"
    uname: list[str] = "se gin sar gan".split()
    aname: list[str] = "še gin2 sar GAN2".split()
    ufact: list[int] = [180, 60, 100]
    cfact: list[int] = [1, 180, 10800, 1080000]
    sex_threshold = 3
    siv: float = 36.0 / 60 / 180
    siu: str = "square meters"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG
    trmodel: str = "Bsur"  # Transliteration model

    def __mul__(self, other: object) -> object:
        """Overloads ``*`` operator

        :param other: operand
        :type other: "Blen" or float
        :return: product
        :rtype: "Bvol" | "Bsur" | None
        """
        # 1. Case: Area * Length (or subclasses) -> Volume
        if isinstance(other, Blen):
            t = int(round((self.dec * other.dec) / 30.0, 0))
            return Bvol(t)
        # 2. Case: Scale (number)
        elif isinstance(other, (int, float)):
            t = self.dec * other
            return self.__class__(int(round(t, 0)))
        return NotImplemented

    def __truediv__(self, other: object) -> object:
        """Overloads ``/`` operator

        :param other: operand
        :type other: "Blen" or float
        :return: quotient
        :rtype: "Blen" | "Bsur" | None
        """
        # 1. Case: Area / Length (or subclasses) -> Length
        if isinstance(other, Blen):
            t = int(round((self.dec / other.dec) * 12.0, 0))
            return Blen(t)
        # 2. Case: Scale (number)
        elif isinstance(other, (int, float)):
            t = self.dec / other
            return self.__class__(int(round(t, 0)))
        return NotImplemented


class Bvol(MesoM):  # Volume
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period volume units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """

    title: str = "Babylonian volume measurement"
    uname: list[str] = "se gin sar gan".split()
    aname: list[str] = "še gin2 sar GAN2".split()
    ufact: list[int] = [180, 60, 100]
    cfact: list[int] = [1, 180, 10800, 1080000]
    sex_threshold = 3
    siv: float = 18.0 / 60 / 180
    siu: str = "cube meters"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG
    trmodel: str = "Bsur"  # Transliteration model

    def cap(self):  # noqa: F821
        """Convert volume to capacity measurement"""
        return Bcap(18000 * self.dec)

    def bricks(self, nalb: float = 1.0) -> "Bbri":
        """Returns the volume in number of bricks equivalent based on their
        "Nalbanum." 720 for 1 sar volume if nalb is 1.

        :param nalb: nalbanum in decimal e.g. 7.20 for type 2 bricks, defaults to 1.0
        :type nalb: float, optional
        :return: volume in bricks equivalent
        :rtype: "Bbri"

        ==========  ============  ============
        Brick type  Nalb. (dec.)  Nalb. (sex.)
        ==========  ============  ============
        1           9.00          9
        1a          8.33          8:20
        2           7.20          7:12
        3           5.40          5:24
        4           5.00          5
        5           4.80          4:48
        7           3.33          3:20
        8           2.70          2:42
        9           2.25          2:15
        10          1.875         1:52:30
        11          1.20          1:12
        12          1.00          1
        ==========  ============  ============

        """
        return Bbri(int(nalb * self.dec))

    def __truediv__(self, other: object) -> object:
        """overloads ``/`` operator

        :param other: operand
        :type other: "Blen" or float
        :return: quotient
        :rtype: "Blen" | "Bsur" | None
        """
        # 1. Case: Volume / Length (or subclasses) -> Surface
        if isinstance(other, Blen):
            t = int(round((self.dec / other.dec) * 30.0, 0))
            return Bsur(t)
        # 2. Case: VOlume / Surface -> length
        elif isinstance(other, Bsur):
            t = int(round((self.dec / other.dec) * 30.0, 0))
            return Blen(t)
        # 3. Case: Scale (number)
        elif isinstance(other, (int, float)):
            t = self.dec / other
            return self.__class__(int(round(t, 0)))
        return NotImplemented


class Bcap(MesoM):  # Capacity
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period capacity units:

        **gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še**

    """

    title: str = "Babylonian capacity measurement"
    uname: list[str] = "se gin sila ban bariga gur".split()
    aname: list[str] = "še gin2 sila3 ban2 bariga gur".split()
    ufact: list[int] = [180, 60, 10, 6, 5]
    cfact: list[int] = [1, 180, 10800, 108000, 648000, 3240000]
    sex_threshold = 4
    siv: float = 1.0 / 60 / 180   # For the "cubic sila"
    siu: str = "litres"
    ubase: int = 1  # gin
    trmodel: str = "Bcap"  # Transliteration model

    def vol(self) -> Bvol | None:
        """Convert capacity to volume measurement

        :return: volume measurement
        :rtype: "Bvol" | None
        """
        if self.dec >= 18000:
            return Bvol(self.dec // 18000)
        else:
            print("Volume too small!")
            return None


class Bwei(MesoM):  # Weight
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period weight units:

        **gu2 <-60- ma-na <-60- gin2 <-180- še**

    """

    title: str = "Babylonian weight measurement"
    uname: list[str] = "se gin mana gu".split()
    aname: list[str] = "še gin2 ma-na gu2".split()
    ufact: list[int] = [180, 60, 60]
    cfact: list[int] = [1, 180, 10800, 648000]
    sex_threshold = 3
    siv: float = 0.5 / 60 / 180
    siu: str = "kilograms"
    ubase: int = 1  # gin
    trmodel: str = "Bwei"  # Transliteration model


class Bbri(MesoM):  # Counting bricks
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period counting bricks in "sar-b" units (720 bricks):

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """

    title: str = "Babylonian brick count"
    uname: list[str] = "se gin sar gan".split()
    aname: list[str] = "še gin2 sar GAN2".split()
    ufact: list[int] = [180, 60, 100]
    cfact: list[int] = [1, 180, 10800, 1080000]
    sex_threshold = 3
    siv: float = 720.0 / 10800
    siu: str = "bricks"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG
    trmodel: str = "Bsur"  # Transliteration model

    def vol(self, nalb: float = 1.0) -> "Bvol":
        """Returns the volume corresponding to a number of bricks  based on their
        *Nalbanum*.  1 sar volume for 720 bricks if nalb is 1

        :param nalb: nalbanum in decimal e.g. 7.20 for type 2 bricks, defaults to 1.0
        :type nalb: float, optional
        :return: equivalent volume
        :rtype: Bvol

        ==========  ============  ============
        Brick type  Nalb. (dec.)  Nalb. (sex.)
        ==========  ============  ============
        1           9.00          9
        1a          8.33          8:20
        2           7.20          7:12
        3           5.40          5:24
        4           5.00          5
        5           4.80          4:48
        7           3.33          3:20
        8           2.70          2:42
        9           2.25          2:15
        10          1.875         1:52:30
        11          1.20          1:12
        12          1.00          1
        ==========  ============  ============

        """
        tt = int(round(self.dec / nalb, 0))
        return Bvol(tt)
