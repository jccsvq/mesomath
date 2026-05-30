"""This module implements class BabF for sexagesimal representation of non-negative rational
fractions and their basic arithmetic operations."""

from functools import total_ordering
from math import gcd

from mesomath import BabN


@total_ordering
class BabF:
    """Class for sexagesimal representation of fractions and their basic arithmetic operations."""

    #: Sexagesimal separator
    SEP = "@"

    @classmethod
    def repeated(
        cls, repeat: int | str | list[int] | tuple[int, int, int, int]
    ) -> object:
        """Converts repeating digits in sexagesimal notation to fraction.

        :param repeat: sexagesimal repeating digits
        :type repeat: int | str | list[int] | tuple[int, int, int, int]
        :return: BabF object with the repeating digits
        :rtype: object
        """
        p = BabN(repeat)
        n = len(p)

        return BabF(p, 60**n - 1)

    def __init__(
        self,
        p: int | str | list[int] | tuple[int, int, int, int],
        q: int | str | list[int] | tuple[int, int, int, int] = None,
    ):
        """Class constructor

        :param p: Numerator of the fraction
        :type p: int | str | list[int] | tuple[int, int, int, int]
        :param q: Denominator of the fraction, defaults to None
        :type q: int | str | list[int] | tuple[int, int, int, int], optional
        """
        # Case 1: Two arguments (BabN, BabN, int, or str)
        if q is not None:
            self.__p = BabN(p)
            self.__q = BabN(q)

        # Case 2: A single argument
        else:
            if isinstance(p, str):
                if "/" in p:
                    # Structural separation: '/'
                    num, den = p.split("/", 1)
                    self.__p, self.__q = BabN(num), BabN(den)
                elif "@" in p:
                    # Structural separation: '@'
                    # We delegate the parsing of the parts to BabN
                    int_str, frac_str = p.split("@", 1)

                    tmp = BabN(frac_str)
                    n = tmp.len()

                    # We convert to integer: integer_value * 60^n + fractional_value
                    # BabN(frac_str) here helps us convert "14:33" -> 873
                    val_frac = tmp.dec

                    self.__p = BabN(BabN(int_str).dec * (60**n) + val_frac)
                    self.__q = BabN(60**n)
                else:
                    # It is a simple number (e.g., "14:33"), we treat it as n/1
                    self.__p = BabN(p)
                    self.__q = BabN(1)

            else:
                # Case p is a BabN object or loose int
                self.__p = BabN(p)
                self.__q = BabN(1)

    @property
    def p(self) -> object:
        """Getter

        :return: Numerator of the fraction
        :rtype: BabN object
        """
        return self.__p

    @property
    def q(self) -> object:
        """Getter

        :return: Denominator of the fraction
        :rtype: BabN object
        """
        return self.__q

    @property
    def as_float(self) -> float:
        """Returns the decimal value of the fraction as a float.

        :return: Decimal value of the fraction
        :rtype: float
        """
        return self.__float__()

    @property
    def as_dec_fraction(self) -> str:
        """Returns the object as fraction of decimal integers

        :return: String with the fraction of decimal integers
        :rtype: str
        """
        return f"{self.p.dec}/{self.q.dec}"

    @property
    def rec(self) -> object:
        """Returns BabF object with the reciprocal of self

        :return: BabF object with the reciprocal of self
        :rtype: BabF object
        """
        """Returns the reciprocal of self"""
        return self.__class__(self.q, self.p)

    @property
    def simplified(self) -> object:
        """Return BabF object with the fraction in lowest terms.

        :return: BabF object with the simplified fraction.
        :rtype: BabF object
        """
        g = gcd(self.p.dec, self.q.dec)

        return BabF(self.p.dec // g, self.q.dec // g)

    def expand(self, max_digits: int = 6) -> str:
        """Return the sexagesimal expansion of the fraction using max_digits and ``cls.SEP``
        as "sexagesimal point" (default ``@``).

        :param max_digits: Number of sexagesimal digits to use, defaults to 6
        :type max_digits: int, optional
        :return: String with the sexagesimal expansion of the fraction
        :rtype: str
        """
        integer_part = self.p.dec // self.q.dec
        remainder = self.p.dec % self.q.dec

        digits = []
        for _ in range(max_digits):
            remainder *= 60
            digit, remainder = divmod(remainder, self.q.dec)
            digits.append(str(digit))
            if remainder == 0:
                break  # Terminamos si es exacto

        return f"{integer_part}{self.SEP}{':'.join(digits)}"

    def to_cunei(self, ndigits:int=6, alter: bool = False, stroke: bool = False) -> str:
        """Cuneiform version of sexagesimal number

        Requires Noto Sans Cuneiform font or similar to be present in your system.
        This method uses U+2009 Thin Space Unicode Characters

        :param ndigits: Number of sexagesimal digits to use, defaults to 6
        :type ndigits: int, optional
        :param obj: BabN object or string to be converted
        :type obj: Any
        :param alter: alternate version of some signs, defaults to False
        :type alter: bool, optional
        :param stroke: strike out empty space (sexagesimal digit zero), defaults to False
        :type stroke: bool, optional
        :return: cuneiform string
        :rtype: str
        """
        line = self.expand(ndigits)
        line = line.replace(self.SEP, ":")
        babn = BabN(line)
        return babn.to_cunei(alter=alter, stroke=stroke)
        

    def __hash__(self):
        """Hash based on the internal state."""
        return hash((self.__p.dec, self.__q.dec))

    def __eq__(self, other) -> bool:
        """Exact comparison (a/b == c/d) by cross product."""
        # Usamos tu validador _check_operand (que nos devuelve un BabF o NotImplemented)
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # a * d == c * b
        return (self.p.dec * other.q.dec) == (other.p.dec * self.q.dec)

    def __lt__(self, other) -> bool:
        """Order comparison (a/b < c/d) by cross product."""
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # a * d < c * b
        return (self.p.dec * other.q.dec) < (other.p.dec * self.q.dec)

    def __float__(self):
        """Float representation of object

        :return: Decimal value of the fraction
        :rtype: float
        """
        return self.p.dec / self.q.dec

    def __int__(self):
        """Integer representation of object"""
        return int(self.__float__())

    def __add__(self, other):
        """Overloads ``+`` operator: returns object with the sum of operands"""
        # 0. Exclude floats
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # 1. If it's BabF, we do fraction mathematics
        if isinstance(other, BabF):
            # (a/b) + (c/d) = (ad + bc) / bd
            new_p = self.p.dec * other.q.dec + other.p.dec * self.q.dec
            new_q = self.q.dec * other.q.dec
            return BabF(new_p, new_q)

        # 2. If it is int or BabN, we treat it as a fraction n/1
        elif isinstance(other, (int, BabN)):
            other_f = BabF(other, 1)
            return self + other_f

    def __radd__(self, other):
        """Overloads ``+`` operator: returns object with the sum of operands"""
        # Python calls this if 'other' does not know how to add with BabF
        return self.__add__(other)

    def __sub__(self, other):
        """Overloads ``-`` operator: returns object with the difference of operands"""
        # 0. Exclude floats
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # 1. If it's BabF, we do fraction mathematics
        if isinstance(other, BabF):
            # (a/b) + (c/d) = (ad + bc) / bd
            new_p = self.p.dec * other.q.dec - other.p.dec * self.q.dec
            new_q = self.q.dec * other.q.dec
            return BabF(new_p, new_q)

        # 2. If it is int or BabN, we treat it as a fraction n/1
        elif isinstance(other, (int, BabN)):
            other_f = BabF(other, 1)
            return self - other_f

    def __rsub__(self, other):
        """Overloads ``-`` operator: returns object with the difference of operands"""
        # Python calls this if 'other' does not know how to subtract with BabF
        return self.__sub__(other)

    def __mul__(self, other):
        """Overloads ``+`` operator: returns object with the product of operands"""
        # 0. Exclude floats
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # 1. If it's BabF, we do fraction mathematics
        if isinstance(other, BabF):
            # (a/b) * (c/d) = (a * c) / (b * d)
            new_p = self.p.dec * other.p.dec
            new_q = self.q.dec * other.q.dec
            return BabF(new_p, new_q)

        # 2. If it is int or BabN, we treat it as a fraction n/1
        elif isinstance(other, (int, BabN)):
            other_f = BabF(other, 1)
            return self * other_f

    def __rmul__(self, other):
        """Overloads ``*`` operator: returns object with the product of operands"""
        # Python calls this if 'other' does not know how to multiply with BabF
        return self.__mul__(other)

    def __truediv__(self, other):
        """Overloads ``/`` operator: returns object with the quotient of operands"""
        # 0. Exclude floats
        other = self._check_operand(other)
        if other is NotImplemented:
            return NotImplemented

        # 1. If it's BabF, we do fraction mathematics
        if isinstance(other, BabF):
            # (a/b) / (c/d) = (a * d) / (b * c)
            new_p = self.p.dec * other.q.dec
            new_q = self.q.dec * other.p.dec
            return BabF(new_p, new_q)

        # 2. If it is int or BabN, we treat it as a fraction n/1
        elif isinstance(other, (int, BabN)):
            other_f = BabF(other, 1)
            return self / other_f

    def __rtruediv__(self, other):
        """Overloads ``/`` operator: returns object with the quotient of operands"""
        # Python calls this if 'other' does not know how to divide with BabF
        return (self.__truediv__(other)).rec

    def __pow__(self, other):
        """Overloads ``**`` operator: returns object with the power of self"""
        if not isinstance(other, int) or other < 0:
            raise ValueError("Exponent must be a positive integer")
        return BabF(self.p.dec ** other, self.q.dec ** other)

    def __repr__(self):
        """String representation of object"""
        return f"{self.p}/{self.q}"

    def _check_operand(self, other):
        """Validate that the operand is not a float before operating."""
        if isinstance(other, float):
            raise TypeError(
                "MesoMath does not allow mixed operations with float to preserve precision.\n"
                "Use explicit conversion to BabF or use .as_float"
            )
        # If it is a compatible type (BabF, BabN, int), we convert it to BabF to operate
        if isinstance(other, (int, BabN)):
            return BabF(other, 1)
        if isinstance(other, BabF):
            return other
        return NotImplemented


if __name__ == "__main__":
    a = BabF("14:33", "44:14")
    print(a)
    print(a.as_float)
    b = BabF("14:33/44:14")
    print(b)
    print(b.as_float)
    c = BabF(14, 44)
    print(c)
    print(c.as_float)
    d = c.simplified
    print(d)
    print(d.as_float)
    e = BabF("3@14:33")
    print(e)
    print(e.as_float)
    f = BabF("16@30:56:47:14")
    print(f)
    print(f.expand())
    g = BabF([1, 2], (1, 5, 4, 7))
    print(g)
    print(g.as_float)
