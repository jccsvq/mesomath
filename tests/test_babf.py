"""Unit tests for the BabF class (Sexagesimal Fractions)."""

import pytest
from mesomath import BabN, BabF


def test_babf_construction_and_properties():
    """Test the multiple ways to instantiate a BabF object."""
    # Case 1: Numerator and Denominator as loose integers
    f1 = BabF(74, 28)
    assert f1.p.dec == 74
    assert f1.q.dec == 28
    assert f1.as_dec_fraction == "74/28"

    # Case 2: Structural separation with '/'
    f2 = BabF("74/28")
    assert f2 == f1

    # Case 3: Positional notation with '@' (implicit denominator 60^n)
    f3 = BabF("29@31:50:8:48")  # Ptolemy's synodic month
    assert f3.q.dec == 60**4
    assert f3.p.dec == 29 * (60**4) + 31 * (60**3) + 50 * (60**2) + 8 * 60 + 48

    # Case 4: Single argument without separators (treated as n/1)
    f4 = BabF("14:33")
    assert f4.p == BabN("14:33")
    assert f4.q.dec == 1


def test_babf_simplification_and_expansion():
    """Test fraction reduction and sexagesimal string expansion."""
    f = BabF(74, 28)  # 74/28 -> 37/14
    f_sim = f.simplified
    assert f_sim.p.dec == 37
    assert f_sim.q.dec == 14

    # Test periodic expansion
    # 74/28 = 2.64285714... -> 2 + 38/60 + 34/3600 + 17/216000 ...
    assert f.expand(3) == "2@38:34:17"
    assert f.expand(6) == "2@38:34:17:8:34:17"


def test_babf_repeated_method():
    """Test conversion of repeating sexagesimal digits into an exact fraction."""
    # 1/7 in sexagesimal repeats '8:34:17' infinitely
    h = BabF.repeated("8:34:17")
    assert h.q.dec == (60**3) - 1
    assert h.simplified == BabF(1, 7)


def test_babf_arithmetic_operations():
    """Test basic arithmetic, powers, and reciprocals."""
    f = BabF(74, 28)  # 37/14
    g = BabF(5, 8)

    # Addition: (74*8 + 5*28) / (28*8) = 732 / 224
    res_add = f + g
    assert res_add.p.dec == 732
    assert res_add.q.dec == 224

    # Subtraction: (74*8 - 5*28) / (28*8) = 452 / 224
    res_sub = f - g
    assert res_sub.p.dec == 452
    assert res_sub.q.dec == 224

    # Multiplication: (74*5) / (28*8) = 370 / 224
    res_mul = f * g
    assert res_mul.p.dec == 370
    assert res_mul.q.dec == 224

    # Division: (74*8) / (28*5) = 592 / 140
    res_div = f / g
    assert res_div.p.dec == 592
    assert res_div.q.dec == 140

    # Power
    res_pow = g**2
    assert res_pow.p.dec == 25
    assert res_pow.q.dec == 64

    # Reciprocal
    assert g.rec == BabF(8, 5)


def test_babf_mixed_types_operations():
    """Test arithmetic operations with alternative native types (int, BabN)."""
    f = BabF(5, 8)
    
    # Interoperability with int
    res_int = f + 2  # 5/8 + 16/8 = 21/8
    assert res_int.simplified == BabF(21, 8)
    assert 2 + f == res_int

    # Interoperability with BabN
    n = BabN("2")
    res_babn = f * n
    assert res_babn.simplified == BabF(10, 8)


def test_babf_comparisons():
    """Test total ordering operations via cross product."""
    f = BabF(74, 28)  # ~2.64
    g = BabF(5, 8)    # 0.625

    assert f > g
    assert g < f
    assert f != g
    assert f == BabF(37, 14)


def test_babf_precision_guardrails():
    """Ensure that mixing floats raises a TypeError to protect precision."""
    f = BabF(5, 8)

    with pytest.raises(TypeError, match="MesoMath does not allow mixed operations with float"):
        _ = f + 0.5

    with pytest.raises(TypeError, match="MesoMath does not allow mixed operations with float"):
        _ = f * 1.2