"""This package is intended for the arithmetic of natural sexagesimal numbers,
mainly in their "floating" aspect (i.e., by removing all possible trailing
sexagesimal zeros from the right), as performed by the Babylonian scribes and
their apprentices in ancient times.

Inpired by the arithmetic part of Baptiste Mélès' MesoCalc, it aims to bring
this type of calculation to Python programming and to the command line as a
calculator."""

from .__about__ import __version__
from .babn import BabN
from .npvs import Blen
from .npvs import Bsur
from .npvs import Bvol
from .npvs import Bcap
from .npvs import Bwei
from .npvs import BsyG
from .npvs import BsyS
from .npvs import Bbri

BabN.__module__ = "mesomath"
Blen.__module__ = "mesomath"
Bsur.__module__ = "mesomath"
Bvol.__module__ = "mesomath"
Bcap.__module__ = "mesomath"
Bwei.__module__ = "mesomath"
BsyG.__module__ = "mesomath"
BsyS.__module__ = "mesomath"
Bbri.__module__ = "mesomath"


__all__ = [
    "BabN",
    "Blen",
    "Bsur",
    "Bvol",
    "Bcap",
    "Bwei",
    "BsyG",
    "BsyS",
    "Bbri",
    "__version__",
]
