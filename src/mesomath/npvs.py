"""This module implements classes for Non-Place-Value numeration system and
related arithmetic. Intended for Mesopotamian metrological systems,
but class Npvs is of general use.

* class  Npvs: Generic class inspired in Imperial Units System lengths

    * class _MesoM: Specializes the Npvs class to handle Mesopotamian counting.

        * class  BsyG: Babylonian System G
        * class  BsyS: Babylonian System S
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
    :prtsex: Printing meassurements in sexagesimal (default: False)


    Instance Attributes:
    --------------------

    :dec: Decimal value of meassurement in terms of the smallest unit
    :list: List of values per unit

    Operators
    ---------

    This class overloads arithmetic and logical operators allowing arithmetic
    operations and comparisons to be performed between members of the class.
    Comparison with other objects raises ``NotImplementedError``.

    jccsvq fecit, 2005. Public domain.

    """

    title: str = "Imperial length meassurement"
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

    def scheme(self, actual: bool = False) -> list:
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
            for i in range(len(self.ufact)):
                ll.append(self.aname[i])
                ll.append("<-" + str(self.ufact[i]) + "-")
            ll.append(self.aname[-1])
        else:
            for i in range(len(self.ufact)):
                ll.append(self.uname[i])
                ll.append("<-" + str(self.ufact[i]) + "-")
            ll.append(self.uname[-1])
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
    prtsex: bool = False  # Printing meassurements in sexagesimal
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

            # IMPORTANTE: No envíes la clase base BsyS.
            # Envía el sistema que esta clase específica (Bcap, Bwei, etc.) usa.
            # Si tu clase tiene un atributo 'sexsys' definido a nivel de clase:
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

    @property
    def dec(self):
        """Getter"""
        return self.__dec

    @property
    def list(self):
        """Getter"""
        return self.__list

    def sex(self, r: int = 0) -> BabN | None:
        """Return sexagesimal floating value of object

        :param r: index of reference unit in uname, defaults to 0
        :type r: int, optional
        :return: sexagesimal floating value of object
        :rtype: BabN | None
        """
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
            f"Meassurement in terms of the smallest unit: {self.dec} ({self.uname[0]})"
        )
        print(f"Sexagesimal floating value of the above: {self.sex(0)}")
        print(f"Approximate SI value: {self.SI()}")

    def prtf(self, onesixth: bool = False, actual: bool = False) -> str:
        """Alternative to __repr__() to use the fractions 1/3, 1/2, 2/3, 5/6 of
        the units in the output

        :onesixth: Adds 1/6 to the previous set of fractions if True
        :type onesixth: bool, (default = False)
        :actual: if True, uses academic unit names on output
        :type actual: bool, (default: False)
        """
        if onesixth:
            fdic = fdic1
        else:
            fdic = fdic0
        length = len(self.list)
        ll = self.list.copy()
        ff = ["" for i in range(length)]
        for i in range(length - 1):
            k = self.ufact[i]
            (zfrac, z) = fdic[k]
            for j in range(len(z)):
                if ll[i] >= z[j]:
                    ll[i] -= z[j]
                    ff[i + 1] = zfrac[j]
                    break
        for i in range(length):
            if ll[i] == 0 and ff[i] == "":
                pass
            else:
                if ff[i] == "":
                    ff[i] = str(ll[i])
                else:
                    if ll[i] != 0:
                        ff[i] = str(ll[i]) + " " + ff[i]
        ss = ""
        for i in reversed(range(length)):
            if ff[i] != "":
                if actual:
                    ss += ff[i] + " " + self.aname[i] + " "
                else:
                    ss += ff[i] + " " + self.uname[i] + " "
        return ss[:-1]

    def __repr__(self) -> str:
        """Returns string representation of object."""
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                if not self.prtsex:
                    ss.append(str(self.list[i]))
                    ss.append(self.uname[i])
                else:
                    if self.list[i] >= 60:
                        ss.append(
                            str(self.list[i] // 60) + ":" + str(self.list[i] % 60)
                        )
                    else:
                        ss.append(str(self.list[i]))
                    ss.append(self.uname[i])
        return " ".join(ss)


class BsyG(_MesoM):  # Babylonian System G numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-G numeration

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


class BsyS(_MesoM):  # Babylonian System S numeration
    """This class implement Non-Place-Value System arithmetic
    for Babylonian System-S numeration

        **šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš**

    """

    title: str = "Babylonian System S to count objects"
    uname: list[str] = "dis u ges gesu sar saru sargal".split()
    aname: list[str] = "diš u geš geš'u šar2 šar'u šar2-gal".split()
    ufact: list[int] = [10, 6, 10, 6, 10, 6]
    cfact: list[int] = [1, 10, 60, 600, 3600, 36000, 216000]
    siv: float = 1
    siu: str = "#"
    ubase: int = 0  # dis
    dic_cfact = {
        "dis": 1,
        "u": 10,
        "ges": 60,
        "gesu": 600,
        "sar": 3600,
        "saru": 36000,
        "sargal": 216000,
    }


class MesoM(_MesoM):
    """This class complements the _MesoN class by allowing you to express unit
    coefficients in measurements using the S and G systems as appropriate. It
    introduces the sexsys attribute and enhances the __repr__ method."""

    sexsys: type[BsyS] | type[BsyG] = BsyS

    def prtf(self, onesixth: bool = False, actual: bool = False) -> str:
        """Alternative to __repr__() to use the fractions 1/3, 1/2, 2/3, 5/6 of
        the units in the output

        :onesixth: Adds 1/6 to the previous set of fractions if True
        :type onesixth: bool, (default = False)
        :actual: use academic unit names if True
        :type actual: bool, (default = False)
        """
        if onesixth:
            fdic = fdic1
        else:
            fdic = fdic0
        length = len(self.list)
        ll = self.list.copy()
        ff = ["" for i in range(length)]
        for i in range(length - 1):
            k = self.ufact[i]
            (zfrac, z) = fdic[k]
            for j in range(len(z)):
                if ll[i] >= z[j]:
                    ll[i] -= z[j]
                    ff[i + 1] = zfrac[j]
                    break
        for i in range(length):
            if ll[i] == 0 and ff[i] == "":
                pass
            else:
                if self.prtsex:
                    if ff[i] == "":
                        ff[i] = "(" + str(self.sexsys(ll[i])) + ")"
                    #                        ff[i] = '('+(self.sexsys(ll[i])).prtf(onesixth)+')'
                    else:
                        if ll[i] != 0:
                            ff[i] = "(" + str(self.sexsys(ll[i])) + ")" + " " + ff[i]
                #                            ff[i] =  '('+(self.sexsys(ll[i])).prtf(onesixth)+')'+' '+ff[i]
                else:
                    if ff[i] == "":
                        ff[i] = str(ll[i])
                    else:
                        if ll[i] != 0:
                            ff[i] = str(ll[i]) + " " + ff[i]
        ss = ""
        for i in reversed(range(length)):
            if ff[i] != "":
                if actual:
                    ss += ff[i] + " " + self.aname[i] + " "
                else:
                    ss += ff[i] + " " + self.uname[i] + " "

        return ss[:-1]

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

    def __repr__(self) -> str:
        """Returns string representation of object."""
        ss = []
        for i in reversed(range(len(self.uname))):
            if self.list[i] != 0:
                if not self.prtsex:
                    ss.append(str(self.list[i]))
                else:
                    if i == len(self.uname) - 1:
                        ss.append("(" + str(self.sexsys(self.list[i])) + ")")
                    else:
                        ss.append("(" + str(BsyS(self.list[i])) + ")")
                ss.append(self.uname[i])
        return " ".join(ss)

    @classmethod
    def metrolist(
        cls,
        mmin: str | int,
        mmax: str | int,
        step: str | int,
        verbose: bool = False,
        ubase: int | None = None,
        width: int = 20,
        fractions: int = -1,
        actual: bool = False,
        echo: bool = True,  # Nuevo switch para control de salida
        **kwargs,
    ):
        """Generate a list of metrological values for the current class.

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
        :return: List of formatted strings
        :rtype: list
        """
        start_dec = cls(mmin).dec
        end_dec = cls(mmax).dec
        step_dec = cls(step).dec

        if ubase is None:
            ubase = cls.ubase

        results = []

        # Helper function to handle output according to the switch
        def handle_output(text):
            if echo:
                print(text)
            results.append(text)

        if verbose:
            handle_output(f"{'Measurement'.ljust(width)} | {'Sexag. (base)'}")
            handle_output("-" * (width + 18))

        current = start_dec
        while current <= end_dec + (step_dec / 10):
            obj = cls(int(round(current)))

            if fractions in {1, 2}:
                ln = obj.prtf(onesixth=fractions == 2, actual=actual)
            else:
                ln = str(obj)

            if verbose:
                line = f"{ln.ljust(width)} | {str(obj.sex(r=ubase)).ljust(15)}"
            else:
                line = ln.ljust(width)

            handle_output(line)
            current += step_dec

        # Only return the list if echo is False (prevents duplication in REPL)
        if not echo:
            return results


class Blen(MesoM):  # Length
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period length units

        **danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si**

    """

    title: str = "Babylonian length meassurement"
    uname: list[str] = "susi kus ninda us danna".split()
    aname: list[str] = "šu-si kuš3 ninda UŠ danna".split()
    ufact: list[int] = [30, 12, 60, 30]
    cfact: list[int] = [1, 30, 360, 21600, 648000]
    siv: float = 0.5 / 30
    siu: str = "meters"
    ubase: int = 2  # ninda

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

    title: str = "Babylonian surface meassurement"
    uname: list[str] = "se gin sar gan".split()
    aname: list[str] = "še gin2 sar GAN2".split()
    ufact: list[int] = [180, 60, 100]
    cfact: list[int] = [1, 180, 10800, 1080000]
    siv: float = 36.0 / 60 / 180
    siu: str = "square meters"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG

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


class Bvol(MesoM):  # Volume
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period volume units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """

    title: str = "Babylonian volume meassurement"
    uname: list[str] = "se gin sar gan".split()
    aname: list[str] = "še gin2 sar GAN2".split()
    ufact: list[int] = [180, 60, 100]
    cfact: list[int] = [1, 180, 10800, 1080000]
    siv: float = 18.0 / 60 / 180
    siu: str = "cube meters"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG

    def cap(self):  # noqa: F821
        """Convert volume to capacity meassurement"""
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


class Bcap(MesoM):  # Capacity
    """This class implement Non-Place-Value System arithmetic
    for Old Babylonian Period capacity units:

        **gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še**

    """

    title: str = "Babylonian capacity meassurement"
    uname: list[str] = "se gin sila ban bariga gur".split()
    aname: list[str] = "še gin2 sila3 ban2 bariga gur".split()
    ufact: list[int] = [180, 60, 10, 6, 5]
    cfact: list[int] = [1, 180, 10800, 108000, 648000, 3240000]
    siv: float = 1.0 / 60 / 180
    siu: str = "litres"
    ubase: int = 1  # gin

    def vol(self) -> Bvol | None:
        """Convert capacity to volume meassurement

        :return: volume meassurement
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

    title: str = "Babylonian weight meassurement"
    uname: list[str] = "se gin mana gu".split()
    aname: list[str] = "še gin2 ma-na gu2".split()
    ufact: list[int] = [180, 60, 60]
    cfact: list[int] = [1, 180, 10800, 648000]
    siv: float = 0.5 / 60 / 180
    siu: str = "kilograms"
    ubase: int = 1  # gin


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
    siv: float = 720.0 / 10800
    siu: str = "bricks"
    ubase: int = 1  # gin
    sexsys: type[BsyS] | type[BsyG] = BsyG

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
