"""This package is designed for the study of metrology and arithmetic of 
natural sexagesimal numbers used by Babylonian scribes and their apprentices 
in antiquity.

Inspired by the arithmetic and metrological parts of Baptiste Mélès' MesoCalc, 
it aims to bring this type of calculation to Python programming and to the 
command line as a calculator.
"""

from .__about__ import __version__
from .babn import BabN
from .babf import BabF
from .npvs import (
    Bbri,
    Bcap,
    Blen,
    Bsur,
    BsyC,
    BsyG,
    BsyK,
    BsyS,
    Bvol,
    Bwei,
)

# Overriding module metadata for a seamless top-level API experience
BabN.__module__ = "mesomath"
BabF.__module__ = "mesomath"
Blen.__module__ = "mesomath"
Bsur.__module__ = "mesomath"
Bvol.__module__ = "mesomath"
Bcap.__module__ = "mesomath"
Bwei.__module__ = "mesomath"
BsyG.__module__ = "mesomath"
BsyS.__module__ = "mesomath"
BsyC.__module__ = "mesomath"
BsyK.__module__ = "mesomath"
Bbri.__module__ = "mesomath"

# Base contract of core mathematical components
__all__ = [
    "__version__",
    "BabN",
    "BabF",
    "Blen",
    "Bsur",
    "Bvol",
    "Bcap",
    "Bwei",
    "BsyG",
    "BsyS",
    "BsyC",
    "BsyK",
    "Bbri",
]

# =========================================================================
# DYNAMIC INTER-PACKAGE BRIDGE: OPTIONAL MESOTIMES EXTENSION
# =========================================================================
try:
    import mesotimes
    
    ChronDate = mesotimes.ChronDate
    ChronDate.__module__ = "mesomath"
    
    __all__.append("ChronDate")
    
except ImportError:
    pass
