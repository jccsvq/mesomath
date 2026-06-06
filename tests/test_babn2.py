import pytest
from mesomath.babn import BabN as bn

def test_arithmetic_and_representation():
    """Basic arithmetic tests and representation."""
    a = bn(405)
    b = bn("1:12:23")
    
    # Representation and Conversion
    assert str(a) == "6:45"
    assert b.dec == 4343
    assert int(b) == 4343
    
    # Arithmetic (including commutativity)
    assert (a + b) == bn("1:19:8")
    assert (b - a) == bn("1:5:38") # Implicit absolute value
    assert (a * b) == bn("8:8:35:15")

def test_regularity_and_factors():
    """Tests of logic of regular numbers and factors."""
    a = bn(405)
    # Hamming #79405: The 20-digit limit
    h_max = bn('59:55:19:56:29:53:35:26:59:56:27:48:02:50:23:52:37:01:52:30')
    
    assert a.isreg is True
    assert a.factors == (0, 4, 1, 1)
    assert h_max.isreg is True
    assert h_max.factors[3] == 1 # Remainder must be 1

def test_normalization_and_protection():
    """Tests of the constructor's new protections."""
    # Skill: List normalization (Carry-over)
    assert bn([1, 125]).list == [3, 5]
    
    # Shielding: Blocking of not allowed types
    class FakeUnit:
        def __int__(self): return 10
    
    with pytest.raises(TypeError):
        bn([1, FakeUnit()])

def test_metrological_blocking():
    """Check that the metrological units do not sneak into BabN."""
    # Deferred import to avoid circular dependencies if there are any
    from mesomath.npvs import Blen as bl
    
    # Automatic lock
    with pytest.raises(TypeError):
        bn([1, bl(10)])
        
    # Explicit conversion allowed
    a = bn([1, int(bl(10))])
    assert isinstance(a, bn)