import pytest
from mesomath.babn import BabN as bn

def test_arithmetic_and_representation():
    """Pruebas de aritmética básica y representación."""
    a = bn(405)
    b = bn("1:12:23")
    
    # Representación y Conversión
    assert str(a) == "6:45"
    assert b.dec == 4343
    assert int(b) == 4343
    
    # Aritmética (incluyendo conmutatividad)
    assert (a + b) == bn("1:19:8")
    assert (b - a) == bn("1:5:38") # Valor absoluto implícito
    assert (a * b) == bn("8:8:35:15")

def test_regularity_and_factors():
    """Pruebas de lógica de números regulares y factores."""
    a = bn(405)
    # Hamming #79405: El límite de 20 dígitos
    h_max = bn('59:55:19:56:29:53:35:26:59:56:27:48:02:50:23:52:37:01:52:30')
    
    assert a.isreg is True
    assert a.factors == (0, 4, 1, 1)
    assert h_max.isreg is True
    assert h_max.factors[3] == 1 # Residuo debe ser 1

def test_normalization_and_protection():
    """Pruebas de las nuevas protecciones del constructor."""
    # Habilidad: Normalización de listas (Carry-over)
    assert bn([1, 125]).list == [3, 5]
    
    # Blindaje: Bloqueo de tipos no permitidos
    class FakeUnit:
        def __int__(self): return 10
    
    with pytest.raises(TypeError):
        bn([1, FakeUnit()])

def test_metrological_blocking():
    """Verifica que las unidades metrológicas no se cuelen en BabN."""
    # Importación diferida para evitar dependencias circulares si las hubiera
    from mesomath.npvs import Blen as bl
    
    # Bloqueo automático
    with pytest.raises(TypeError):
        bn([1, bl(10)])
        
    # Conversión explícita permitida
    a = bn([1, int(bl(10))])
    assert isinstance(a, bn)