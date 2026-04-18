"""This module implements class Babn for sexagesimal representation of the natural numbers
and their basic arithmetic operations, especially in their "floating" version,
as performed by Babylonian scribes. Hence the name."""

import sys
from math import log, sqrt
from os.path import exists
from sqlite3 import connect

from typing import List

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class BabN:
    """This class implements a sexagesimal representation of the natural numbers
    and their basic arithmetic operations, especially in their "floating" version,
    as performed by Babylonian scribes. Hence the name.

    Class attributes:
    -----------------

    :title: Describe the type of object
    :type title: str
    :sep: separator for string representation (default: ":")
    :type sep: str, (default: ":")
    :fill: if True writes: "01.33.07" instead of "1.33.7"
    :type fill: bool,  (default: False)
    :rdigits: approximate number of sexagesimal digits for some results
    :type rdigits: int, (default: 6:)
    :floatmult: If True, multiplication result is floating
    :type floatmult: bool, (default: False)
    :database: path to SQLite3 database of regular numbers providing:

        | regular:    TEXT, regular number e.g. 01:18:43:55:12
        | len:     INTEGER, its length e.g. 5 for 01:18:43:55:12
        | see ``createDB.py`` or ``hamming.py`` for how to generate it

    :type database: str, (default: "regular.db3")

    Instance attributes:
    --------------------

    :dec: decimal versión of number (ex: 405 for sexagesimal "6:45")
    :type dec: int
    :list: list of sexagesimal digits of number (ex: [6, 45] for 405 or "6:45")
    :type list: list
    :isreg: True if number is regular (only contains 2, 3, 5 as divisors)
    :type isreg: bool
    :factors: tuple with the powers of 2, 3, 5 and the remainder
    :type factors: tuple

    jccsvq fecit, 2005. Public domain.

    Operators
    ---------

    This class overloads arithmetic and logical operators allowing arithmetic
    operations and comparisons to be performed between members of the class and
    externally with integers. Comparing with any other object type will raise
    ``NotImplementedError``.

    """

    title: str = "Sexagesimal number"
    sep: str = ":"
    fill: bool = False
    rdigits: int = 6
    floatmult: bool = False
    database: str = "regular.db3"

    def __init__(self, value: int | str | list[int] | tuple[int, int, int, int]):
        """
        Initialize a new Babylonian number (BabN).

        This constructor acts as a robust gateway for sexagesimal data. It normalizes
        input values, enforces the non-negative constraint of Babylonian mathematics,
        and protects against improper metrological mixing.

        :param value: The source data for the number. Supported formats:

            * **int | float**: Absolute integer value.
            * **str**: Sexagesimal digits separated by non-numeric characters (e.g., "1:20", "1.20").
            * **list**: Coefficients of the sexagesimal polynomial. Values > 59 are
              automatically normalized (carry-over).
            * **tuple**: A 4-element factor tuple (i, j, k, x) representing
              :math:`2^i \\cdot 3^j \\cdot 5^k \\cdot x`.

        :type value: int | str | list | tuple

        :raises ValueError: If the input string contains no digits, a tuple does not
            have 4 elements, or factors are invalid.
        :raises TypeError: If an unsupported type is passed, or if a metrological
            unit (e.g., Blen, Bwei) is found inside a list.

        .. note::
           **Normalization Logic**: If a list is provided as ``[1, 125]``, it is
           treated as :math:`1 \\cdot 60^1 + 125 \\cdot 60^0 = 185`, which
           normalizes to ``[3, 5]`` (3:05).

        .. warning::
           To maintain historical rigor, all negative inputs are converted to
           their absolute value.
        """
        self.__list: list[int] = []
        self.__dec: int = 0
        # CASE 1: Tuple (i, j, k, x)
        if isinstance(value, tuple):
            if len(value) != 4:
                raise ValueError(
                    "Factor tuple must have exactly 4 elements: (i, j, k, x)"
                )

            try:
                i, j, k, x = [int(v) for v in value]
                # Los exponentes i, j, k sí deberían ser positivos para ser Hamming
                if i < 0 or j < 0 or k < 0:
                    raise ValueError(
                        "Exponents i, j, k in factor tuple must be non-negative."
                    )
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid factor tuple: {value}") from e

            self.__dec = (2**i) * (3**j) * (5**k) * abs(x)
            self.__list = self._to_sexagesimal(self.__dec)
        # CASE 2: String (with regex for any separator)
        elif isinstance(value, str):
            import re

            parts = re.split(r"[:;.,\-\s]+", value.strip())
            self.__list = [int(p) for p in parts if p]
            if not parts:
                raise ValueError(f"Text string without valid numbers: '{value}'")
            ll = [int(p) for p in parts]
            self.__dec = self._to_decimal(ll)
            self.__list = self._to_sexagesimal(self.__dec)
        # CASE 3: List
        elif isinstance(value, list):
            ll = []
            for v in value:
                # WHITE LIST: We only allow the exact type BabN, int, or str.
                # Any other object (like bl, bs...) that has __int__ will be rejected.
                if type(v) in (int, str, BabN):
                    try:
                        ll.append(abs(int(v)))
                    except (ValueError, TypeError):
                        raise ValueError(f"Could not convert '{v}' to an integer.")
                else:
                    raise TypeError(
                        f"Prohibited element: {v} (type {type(v).__name__})."
                        "To use a metrological unit in a BabN list, "
                        "convert it explicitly to an integer with int()."
                    )

            self.__dec = self._to_decimal(ll)
            self.__list = self._to_sexagesimal(self.__dec)
        # CASE 4: Int or Float
        elif isinstance(value, (int, float, BabN)):
            self.__dec = abs(int(value))
            self.__list = self._to_sexagesimal(self.__dec)

        # Instance attributes (Lazy)
        self.__factors = None
        self.__isreg = None
        # self.__factors = self._calculate_factors(self.__dec)
        # self.__isreg = (self.factors[3] == 1)
        # print(f"{self.__dec=} -> {self.__list=} -> {self.__factors=} -> {self.__isreg=}")

    @staticmethod
    def genDB(dbname: str) -> None:
        """Generates a sqlite3 database of regular numbers up to 20 sexagesimal digits

        :dbname: database path and name
        :type dbname: str

        """
        sqlhead = """
        CREATE TABLE regulars (
        id INTEGER PRIMARY KEY,
        regular    TEXT,
        len     INTEGER
        );
        """
        from mesomath.hamming import hamming

        sqltail = """CREATE UNIQUE INDEX regs ON regulars (regular);
        """

        rlist = hamming(1, 79405)
        i = 0
        BabN.fill = True

        con = connect(dbname)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS regulars;")
        cur.execute(sqlhead)

        for x in rlist:
            if x % 60 != 0:
                i += 1
                n = BabN(x)
                nlen = n.len()
                cur.execute(f"INSERT INTO regulars VALUES({i},'{n}',{nlen});")
        cur.execute(sqltail)
        con.commit()
        con.close()
        print(f"""...(Database: {dbname} created!)...""")

    @staticmethod
    def _calculate_factors(n: int) -> tuple[int, int, int, int]:
        """Obtains :math:`i, j, k, x` such that
        :math:`2^i \\cdot 3^j \\cdot 5^k \\cdot x = n`

        :param n: decimal integer
        :type n: int
        :return: tuple (i, j, k, x)
        :rtype: tuple[int, int, int, int]
        """
        if n <= 0:
            return (0, 0, 0, n)

        d = n
        # Factor 2 with bit_length and bitwise (very fast)
        # We count how many zeros are on the right in binary
        i = (d & -d).bit_length() - 1 if d > 0 else 0
        d >>= i

        # Factors 3 and 5 with walrus operator
        j = 0
        while d > 0 and (m := divmod(d, 3))[1] == 0:
            j += 1
            d = m[0]

        k = 0
        while d > 0 and (m := divmod(d, 5))[1] == 0:
            k += 1
            d = m[0]

        return (i, j, k, d)

    @staticmethod
    def _to_decimal(s_list: list[int]) -> int:
        """Convert a sexagesimal list to a decimal integer (BigInt).

        :param s_list: list of sexagesimal digits
        :type s_list: list[int]
        :return: equivalent decimal integer
        :rtype: int
        """
        res = 0
        for digit in s_list:
            res = res * 60 + digit
        return res

    @staticmethod
    def _to_sexagesimal(n: int) -> list[int]:
        """Convert a decimal integer to its sexagesimal list representation.

        :param n: decimal integer to convert
        :type n: int
        :return: resulting sexagesimal list
        :rtype: list[int]
        """
        if n == 0:
            return [0]
        digits = []
        temp = abs(n)
        while temp > 0:
            temp, rem = divmod(temp, 60)
            digits.append(rem)
        return digits[
            ::-1
        ]  # Invertimos para que el más significativo esté al principio

    @classmethod
    def create_new(
        cls, data: int | str | list[int] | tuple[int, int, int, int]
    ) -> "BabN":
        """Class method that returns a new instance.

        :param data: _description_
        :type data: _type_
        :return: resultant object
        :rtype: "BabN"
        """
        return cls(data)

    @property
    def dec(self):
        """Getter"""
        return self.__dec

    @property
    def list(self):
        """Getter"""
        return self.__list

    @property
    def factors(self) -> tuple[int, int, int, int]:
        """Getter. Calculate the factors only when requested (Lazy).

        :return: i, j, k, x such that self.dec = 2^i * 3^j * 5^k * x
        :rtype: tuple[int, int, int, int]
        """
        if self.__factors is None:
            self.__factors = self._calculate_factors(self.__dec)
        return self.__factors

    @property
    def isreg(self) -> bool:
        """Getter (Lazy)"""
        return self.factors[3] == 1

    def inv(self, digits: int = 4) -> Self | None:
        """Returns BabN object with approximate inverse of the number,
        i.e., a * a.inv() is approximately a power of 60

        :param digits: the intended number of digits to return, defaults to 4
        :type digits: int, optional
        :return: _description_
        :rtype: "BabN" | None
        """
        x = self.dec
        if x == 0:
            print("This number has no inverse!")
            return None
        nsd = int(log(x) / log(60))
        inv = (pow(60, nsd + digits)) / x
        inv = int(round(inv, 0))
        while inv % 60 == 0:
            inv //= 60
        return self.create_new(inv)

    def f(self) -> Self:
        """Returns BabN object with the floating part of the number (mantissa),
        i.e., removes any trailing sexagesimal zero, ex.: 4:42:0:0 -> 4:42"""
        temp_list = self.__list[:]
        while len(temp_list) > 1 and temp_list[-1] == 0:
            temp_list.pop()
        return self.create_new(temp_list)

    float = f

    def len(self) -> int:
        """Returns the number of sexagesimal digits of the number as int

        :return: number of sexagesimal digits of the number as int
        :rtype: int
        """
        """Returns the number of sexagesimal digits of the number as int"""
        return len(self.list)

    def head(self, d: int = 1) -> "BabN":
        """Returns the BabN object with the first d digits at most from self

        :param d: Number of digits to return, defaults to 1
        :type d: int, optional
        :return: d most significant sexagesimal digits of self
        :rtype: BabN
        """
        lm = min(abs(d), len(self.list))
        return self.create_new(self.list[:lm])

    def tail(self, d: int = 1) -> "BabN":
        """Returns the BabN object with the last d digits of itself at most

        :param d: Number of digits to return, defaults to 1
        :type d: int, optional
        :return: d less significant sexagesimal digits of self
        :rtype: BabN
        """
        ll = min(abs(d), len(self.list))
        return self.create_new(self.list[-ll:])

    def trim(self, d: int) -> "BabN":
        """Returns BabN object corresponding to the first d sexagesimal digits

        :param d: Number of digits to retain
        :type d: int
        :return: _description_
        :rtype: BabN
        """
        if d <= self.len():
            return self.create_new(self.list[:d])
        else:
            return self

    def round(self, d: int) -> "BabN":
        """Returns BabN object rounded to d sexagesimal digits

        :param d: Number of digits to return
        :type d: int
        :return: number rounded to d sexagesimal digits
        :rtype: BabN
        """
        if d < self.len():
            ll = self.list
            if ll[d] >= 30:
                return self.create_new(ll[:d]) + self.create_new(1)
            else:
                return self.create_new(ll[:d])
        else:
            return self

    def rec(self) -> Self | None:
        """Returns the reciprocal of the BabN object using the factorization method."""
        if not self.isreg:
            print("Not regular, (igi nu)!")
            return None

        # If we've already calculated it before, we return it (Lazy pattern manual)
        if hasattr(self, "_cached_rec"):
            return self._cached_rec

        i, j, k, _ = self.factors

        # The goal is to find i', j', k' such that:
        # (2^i * 3^j * 5^k) * (2^i' * 3^j' * 5^k') = 60^m = 2^(2m) * 3^m * 5^m
        # Therefore: m >= j, m >= k, 2m >= i
        m = max(j, k, (i + 1) // 2)

        i_prime = 2 * m - i
        j_prime = m - j
        k_prime = m - k

        # We calculate the decimal value of the reciprocal
        # We use bit shifts for the factor of 2 (very fast)
        res_dec = (1 << i_prime) * (3**j_prime) * (5**k_prime)

        self._cached_rec = self.create_new(res_dec)
        return self._cached_rec

    def sqrt(self) -> "BabN":
        """Returns BabN object with approximate floating square root

        :return: approximate floating square root
        :rtype: BabN
        """
        digits = BabN.rdigits - 1
        x = self.dec
        sqr = (pow(60, digits)) * sqrt(x)
        sqr = int(round(sqr, 0))
        while sqr % 60 == 0:
            sqr //= 60
        return self.create_new(sqr)

    def cbrt(self) -> "BabN":
        """Returns BabN object with approximate floating cube root

        :return: approximate floating cube root
        :rtype: BabN
        """
        digits = BabN.rdigits - 1
        x = self.dec
        cbr = (pow(60, digits)) * x ** (1.0 / 3)
        cbr = int(round(cbr, 0))
        while cbr % 60 == 0:
            cbr //= 60
        return self.create_new(cbr)

    def dist(self, n: str | int | type(Self)) -> int:
        """Estimates a certain "pseudo-distance" between two sexagesimal numbers.

        The objective is, given a non-regular number, to select the regular
        number that is closest to it from a list. Since these are floating-point
        numbers, this pseudo-distance must be based on the similarity of the most
        significant sexagesimal digits, so that 7 is "close" to 6:59:54:14:24
        (decimals 7 and 90699264).

        :param n: may be an integer, formated string (ex: "1:2:3"), a list (ex., [1, 12, 23]) or another BabN object.
        :type n: str | int | type
        :return: pseudo-distance
        :rtype: int
        """
        list1 = [] + self.list
        len1 = self.len()
        if type(n) is BabN:
            list2 = [] + n.list
            len2 = n.len()
            print(self.dec, n.dec)
        else:
            new_object = self.create_new(n)
            list2 = new_object.list
            len2 = len(list2)
        if len1 > len2:
            list2 += [0 for i in range(len1 - len2)]
        elif len2 > len1:
            nextd = list2[len1]
            list2 = list2[:len1]
            if nextd > 30:
                list2[-1] += 1
        return (BabN(list1) - BabN(list2)).dec

    def searchreg(
        self,
        minn: str | int,
        maxn: str | int,
        limdigits: int = 6,
        prt: bool = False,
    ) -> "BabN":
        """Search database for regulars between sexagesimals minn y maxn.
        Returns BabN object with the closest regular found.

        :param minn: and maxn: must be sexagesimal strings using ":" separator
        :type minn: str | int
        :param maxn: and maxn: must be sexagesimal strings using ":" separator
        :type maxn: str | int
        :param limdigits:  max regular digits number, defaults to 6
        :type limdigits: int, optional
        :param prt: print list of found regulars, defaults to False
        :type prt: bool, optional
        :return: closest regular found as BabN object
        :rtype: BabN
        """
        if not exists(BabN.database):
            __class__.genDB(BabN.database)

        conn = connect(BabN.database)
        cursor = conn.cursor()
        sql_line = """
SELECT regular
  FROM regulars
 WHERE len <= ? AND 
       regular BETWEEN ? AND ?
 ORDER BY regular
;
"""
        cursor.execute(sql_line, (limdigits, minn, maxn))
        rl = cursor.fetchall()
        conn.commit()
        conn.close()

        tmplist = [] + self.__list
        if len(tmplist) < limdigits:
            tmplist = tmplist + [0 for i in range(limdigits - len(tmplist))]

        a = __class__.create_new(tmplist)
        mind = a.dist(rl[0][0])
        minr = rl[0][0]
        for i in rl:
            if prt:
                print(f" {a.dist(i[0]):12d} {i[0]}")
            ndis = a.dist(i[0])
            if ndis < mind:
                mind = ndis
                minr = i[0]
        if prt:
            print(f"Minimal distance: {mind}, closest regular is: {minr}")
        return self.create_new(minr)

    def explain(self) -> None:
        """Explains number; print out basic information about the object."""
        print(f"|  Sexagesimal number: {self.list} is the decimal number: {self.dec}.")
        (i, j, k, x) = self.factors
        print(f"|    It may be written as (2^{i} * 3^{j} * 5^{k} * {x}),")
        if self.isreg:
            print(f"|    so, it is a regular number with reciprocal: {self.rec()}")
        else:
            print("|    so, it is NOT a regular number and has NO reciprocal.")
            print(f"|    but an approximate inverse is: {self.inv()}")
            cr = self.searchreg("01:0", "59:59", 5, 0)
            if cr is not None:
                print(f"|    and a close regular is: {cr}")
                print(f"|    whose reciprocal is: {cr.rec()}")

    def to_cunei(self, alter: bool = False, stroke: bool = False) -> str:
        """Cuneiform version of sexagesimal number

        Requires Noto Sans Cuneiform font or similar to be present in your system.
        This method uses U+2009 Thin Space Unicode Characters

        :param obj: BabN object or string to be converted
        :type obj: Any
        :param alter: alternate version of some signs, defaults to False
        :type alter: bool, optional
        :param stroke: strike out empty space (sexagesimal digit zero), defaults to False
        :type stroke: bool, optional
        :return: cuneiform string
        :rtype: str
        """
        #: cuneiform unit dicttionary
        l1 = [" ", "𒐕", "𒐖", "𒐗", "𒐘", "𒐙", "𒐚", "𒑂", "𒑄", "𒑆"]
        #: cuneiform tens dictionaries
        l10a = [" ", "𒌋", "𒎙", "𒌍", "𒑩", "𒑪"]  # alternate signs
        l10b = [" ", "𒌋", "𒎙", "𒌍", "𒐏", "𒐐"]

        l10 = l10a if alter else l10b
        ln = (self.list).copy()

        out = ""
        for i in ln:
            if i == 0:
                if stroke:
                    out += "𒃵 "  # 𒍻
                else:
                    out += " "
            else:
                tens, unit = divmod(i, 10)
                out += l10[tens]
                out += l1[unit] + " "
        # print(obj, out)
        return out

    cuneiform = to_cunei

    def multable(
        self,
        pral: bool = True,
        sep: str = ":",
        fill: bool = False,
        cuneiform: bool = False,
        stroke: bool = False,
        floating: bool = False,
        indices: List[int] = None,
        echo: bool = True,
    ) -> List[str] | None:
        """
        Displays the multiplication table for the current number.
        
        Following Babylonian tradition, the table includes the 'principal' 
        multipliers (1 to 20, then 30, 40, 50) or the full range (1 to 59).

        :param pral: If True, prints principal numbers (1-20, 30, 40, 50). 
                     If False, prints 1 to 59. Defaults to True.
        :type pral: bool
        :param sep: Separator for sexagesimal digits. Defaults to ":".
        :type sep: str
        :param fill: If True, adds leading zeros to sexagesimal digits <= 9.
        :type fill: bool
        :param cuneiform: If True, outputs the table in Unicode Cuneiform.
        :type cuneiform: bool
        :param stroke: If True, strikes out empty spaces (zeroes) in cuneiform.
        :type stroke: bool
        :param floating: If True, results are treated as sexagesimal floating point.
        :type floating: bool
        :param indices: print table only for these values. Defaults to None.
        :type indices: list[ints]
        :param echo: if False return list of marldown lines instead of printing them. Defaults to True.
        :type echo: bool
        :returns: List of strings with markdown table
        :rtype: List[str] | None
        """
        from mesomath.glyphs import TIMES_LABEL as TIMES
        from mesomath.utils import cunei_rjust
        
        outlist=[]

        def print_to(text):
            if echo:
                print(text)
            else:
                outlist.append(text)


        # Internal value for calculations
        nn = self.dec

        # Context manager style: Backup and restore BabN's global state
        oldsep, oldfill = BabN.sep, BabN.fill
        BabN.sep, BabN.fill = sep, fill

        try:
            # Traditional Babylonian multipliers
            if indices is None:
                pnum = [i + 1 for i in range(20)] + [30, 40, 50] if pral else range(1, 60)
            else:
                pnum = indices

            if cuneiform:
                val = self.to_cunei(stroke=stroke, alter=True)
                # Header formatting for cuneiform
                hh = cunei_rjust(f" {val} {TIMES}  𒐕  ", 15)
                lh = len(hh)
                hh2 = cunei_rjust(f"{val}", len(val) + 4)
                lh2 = len(hh2)
                header = f"\n|{hh}|{hh2}|"
                print_to(header)
                print_to("|" + "-" * lh + "|" + "-" * (lh2-1) + ":|")
            else:
                # Header formatting for ASCII
                label_n = str(self)
                ll = f" i * {label_n}"
                lh = len(ll)
                header = f"\n|  i  |{ll.center(lh)}|"
                print_to(header)
                print_to("|-----|" + "-" * (lh-1) + ":|")

            for i in pnum:
                # Calculate the result
                # Note: using 'floating' avoids issues with integer overflow in sexagesimal context
                res = (BabN(nn * i)).f() if floating else BabN(nn * i)
                
                if cuneiform:
                    # Cuneiform row rendering
                    if i > 1:
                        a1 = BabN(i).to_cunei(stroke=stroke, alter=True)
                        a2 = res.to_cunei(stroke=True, alter=True)
                        b1 = cunei_rjust(TIMES + "  " + a1, lh)
                        b2 = cunei_rjust(a2, lh2)
                        print_to(f"|{b1}|{b2}|")
                    else:
                        # Row for i=1 is often implicit or the header itself in some tablets
                        pass
                else:
                    # ASCII row rendering
                    print_to(f"| {i:2d}  | {str(res).rjust(lh - 2)} |")
                    
        finally:
            # Ensure state is restored even if an error occurs
            BabN.sep, BabN.fill = oldsep, oldfill
            
            if not echo: 
                return outlist

    def multable_nb(self, *arg, **kwargs):
        """
        Displays the multiplication table in a Jupyter Notebook using Markdown.

        :param arg: Positional arguments for multable.
        :param kwargs: Keyword arguments for multable.
        """
        from IPython.display import display_markdown

        kwargs["echo"] = False
        lines = self.multable(*arg, **kwargs)
        md = "\n".join(lines)
        display_markdown(md, raw=True)


    def __add__(self, other: object) -> "BabN":
        """Overloads `+` operator: returns BabN object with the sum of operands

        :param other: May be another BabN object or a positive int.
        :type other: object
        :return: result BabN object
        :rtype: BabN
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.create_new(self.dec + other_obj.dec)

    def __radd__(self, other: object) -> "BabN":
        """Overloads `+` operator: returns BabN object with the sum of operands

        :param other: May be another BabN object or a positive int.
        :type other: object
        :return: result BabN object
        :rtype: BabN
        """
        return self.__add__(other)

    def __sub__(self, other: object) -> "BabN":
        """Overloads `-` operator: returns BabN object with the absolute value
        of the operands difference

        Babylonian mathematics did not use negative numbers. To maintain
        consistency with historical practice, this operator always returns
        the absolute value of the subtraction (|a - b|), i.e: this subtraction is conmutative!

        :other: May be another BabN object or a positive int.
        :type other: object
        :return: result BabN object
        :rtype: BabN
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        # return self.create_new(abs(self.dec - other_obj.dec))
        return self.create_new(abs(self.dec - other_obj.dec))

    def __rsub__(self, other: object) -> "BabN":
        """Overloads `-` operator: returns BabN object with the absolute value
        of the operands difference

        :other: May be another BabN object or a positive int.
        :type other: object
        :return: result BabN object
        :rtype: BabN
        """
        return self.__sub__(other)

    def __mul__(self, other: object) -> "BabN":
        """Overloads `*` operator: returns BabN object with the operands product

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """

        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented

        res = self.dec * other_obj.dec
        if self.floatmult:
            return self.create_new(res).f()
        return self.create_new(res)

    def __rmul__(self, other: object) -> "BabN":
        """Overloads `*` operator: returns BabN object with the operands product

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """
        return self.__mul__(other)

    def __truediv__(self, other: object) -> "BabN":
        """Overloads `/` operator:  Returns BabN object with the floating
        approximate division of operands

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """
        a = self.dec
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        b = other_obj.dec
        try:
            q = a / b
        except ZeroDivisionError:
            print("Oops!  Cannot divide by zero")
            return None
        nsd = int(log(q) / log(60))
        inv = pow(60, BabN.rdigits - nsd) * q
        inv = int(round(inv, 0))
        while inv % 60 == 0:
            inv //= 60
        return self.create_new(inv)

    def __rtruediv__(self, other: object) -> "BabN":
        """Overloads `/` operator:  Returns BabN object with the floating
        approximate division of operands

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        # return (self.create_new(other_obj)) / (self)
        return other_obj.__truediv__(self)

    def __floordiv__(self, other: object) -> "BabN":
        """Overloads `//` operator: Returns BabN object with the result of
        "Babylonian división" of operands, i.e., if b is regular then a//b
        returns a times the reciprocal of b. Result is floating. Returns None
        if b is not regular.

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented

        if not other_obj.isreg:
            print("Divisor is not a regular number (igi nu)!")
            return None

        return (self * other_obj.rec()).f()

    def __rfloordiv__(self, other: object) -> "BabN":
        """Overloads `//` operator: Returns BabN object with the result of
        "Babylonian división" of operands, i.e., if b is regular then a//b
        returns a times the reciprocal of b. Returns None if b is not regular.

        :param other: operand
        :type other: object
        :return: result as BabN object
        :rtype: BabN
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented

        return other_obj.__floordiv__(self)

    def __pow__(self, x: int) -> "BabN":
        """Overloads `**` operator: Returns BabN object with the number raised
        to the power x where x is a natural integer

        :param x: power, positive int.
        :type x: int
        :return: result as BabN object
        :rtype: BabN
        """
        try:
            assert isinstance(x, int) and x >= 0
        except AssertionError:
            print("Exponent must be a positive integer")
            return None
        return self.create_new(pow(self.dec, x))

    def __lt__(self, other: object) -> bool:
        """Overloads < operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec < other_obj.dec

    def __le__(self, other: object) -> bool:
        """Overloads <= operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec <= other_obj.dec

    def __eq__(self, other: object) -> bool:
        """Overloads == operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec == other_obj.dec

    def __ne__(self, other: object) -> bool:
        """Overloads != operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec != other_obj.dec

    def __gt__(self, other: object) -> bool:
        """Overloads > operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec > other_obj.dec

    def __ge__(self, other: object) -> bool:
        """Overloads >= operator

        :param other: operand
        :type other: object
        :return: result of comparison
        :rtype: bool
        """
        other_obj = self._ensure_babn(other)
        if other_obj is NotImplemented:
            return NotImplemented
        return self.dec >= other_obj.dec

    def __repr__(self) -> str:
        """Returns string representation of sexagesimal number.

        :return: representation
        :rtype: str
        """
        rlist = self.list
        if self.fill:
            tt = list(map(str, rlist))
            for i in range(len(tt)):
                if len(tt[i]) == 1:
                    tt[i] = "0" + tt[i]
            return BabN.sep.join(tt)
        else:
            return BabN.sep.join(map(str, rlist))

    def __hash__(self) -> int:
        """Returns hash value of the instance"""
        return hash((type(self), self.__dec))

    def __int__(self) -> int:
        """Converts instance to int"""
        return self.__dec

    __len__ = len
    __round__ = round

    def _ensure_babn(self, other: object) -> "BabN":
        """Internal helper to normalize types before operating.

        :param other: operand
        :type other: object
        :return: BabN object
        :rtype: BabN
        """
        if isinstance(other, BabN):
            return other
        if isinstance(other, (int, float)):
            # Here we centralize the parsing of simple numbers
            return BabN(int(other))
        return NotImplemented
