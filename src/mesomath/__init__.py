"""This package is designed for the study of metrology and arithmetic of 
natural sexagesimal numbers used by Babylonian scribes and their apprentices 
in antiquity.

Inpired by the arithmetic and metrological parts of Baptiste Mélès' MesoCalc, 
it aims to bring this type of calculation to Python programming and to the 
command line as a calculator."""

from .__about__ import __version__
from .babn import BabN
from .npvs import Blen
from .npvs import Bsur
from .npvs import Bvol
from .npvs import Bcap
from .npvs import Bwei
from .npvs import BsyG
from .npvs import BsyS
from .npvs import BsyC
from .npvs import BsyK
from .npvs import Bbri

BabN.__module__ = "mesomath"
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


__all__ = [
    "BabN",
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
    "__version__",
]
