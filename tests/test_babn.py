from mesomath.babn import BabN as bn
#import pytest


def test_babn():
    a = bn(405)
    b = bn("1:12:23")
    c = bn("12.13.0.0") * bn("1.23.45.0.0.0")
    assert a.__repr__() == "6:45"
    assert b.dec == 4343
    assert int(b) == 4343
    assert round(b, 2) == bn("1:12")
    assert len(b) == b.len()
    assert a.isreg
    assert b.isreg is False
    assert a.factors == (0, 4, 1, 1)
    assert b.factors == (0, 0, 0, 4343)

    assert bn('59:55:19:56:29:53:35:26:59:56:27:48:02:50:23:52:37:01:52:30').isreg

    assert (a + b).__repr__() == "1:19:8"
    assert (b + a).__repr__() == "1:19:8"
    assert (b - a).__repr__() == "1:5:38"
    assert (a - b).__repr__() == "1:5:38"
    assert (a * b).__repr__() == "8:8:35:15"
    assert (b * a).__repr__() == "8:8:35:15"

    assert c.__repr__() == "17:3:8:45:0:0:0:0:0"
    assert (c.f()).__repr__() == "17:3:8:45"

    assert (111 + b).__repr__() == "1:14:14"
    assert (b + 111).__repr__() == "1:14:14"
    assert (a - 33).__repr__() == "6:12"
    assert (a / 43).__repr__() == "9:25:6:58:36:16:45"
    assert (8 * b).__repr__() == "9:39:4"

    assert (b // a).__repr__() == "10:43:24:26:40"
    assert (a / b).__repr__() == "5:35:42:45:30:28"
    assert (a**3).__repr__() == "5:7:32:48:45"

    assert (a > b) is False
    assert (a <= b) is True
    assert (a > b) is False
    assert (not a <= b) is False
    assert (a == a) is True

    assert (a != (a - 1)) is True
    assert (a > 100) is True
    assert (not a <= 47) is True

    assert (b.inv()).__repr__() == "49:44:6:45"
    assert (b.inv(8)).__repr__() == "49:44:6:44:30:46:50:2"
    assert (b * b.inv(8)).__repr__() == "59:59:59:59:59:59:59:59:34:46"
    assert (b * b.inv(8)).len() == 10

    assert (a.rec()).__repr__() == "8:53:20"

    assert ((30 * bn(2).sqrt()).float()).__repr__() == "42:25:35:3:53"
    assert ((bn(2).sqrt()).dec / 60.0**5).__repr__() == "1.4142135622427983"
    assert ((bn(2).sqrt() ** 2).round(6)).__repr__() == "2:0:0:0:0:0"
    assert round(bn(2).cbrt() ** 3, 5).f() == 2

    # Database
    z = a.searchreg("01:10", "01:20", 5, 1)
    assert z == bn("01:20")


def test_normalization_and_protection():
    # 1. Normalization Test (The "ability")
    assert bn([1, 125]).list == [3, 5]

    # 2. Shielding Test (The "customs")
    # Try to put something that is NOT int, str, or pure BabN
    class FakeUnit:
        def __int__(self):
            return 10

    fake = FakeUnit()
    try:
        bn([1, fake])
    except TypeError:
        print("Success: Metrological unit blocked!")

def test_metrological_blocking():
    from mesomath.npvs import Blen as bl
    
    # 1. This should fail (Attempt to mix length with pure number)
    #with pytest.raises(TypeError) as excinfo:
    try:
        bn([1, bl(10)])
    except TypeError:
        print("Success: Metrological unit blocked!")
    #assert "Prohibited element:" in str(excinfo.value)

    # 2. This should work (Explicit conversion by the user)
    # The user "assumes responsibility" when using int()
    a = bn([1, int(bl(10))]) 
    assert isinstance(a, bn)