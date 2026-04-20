# 🏺 MesoMath v2.0.0
**The Definitive Mesopotamian Metrology & Arithmetic Engine for Python.**

![PyPI - Version](https://img.shields.io/pypi/v/mesomath)
![PyPI - Status](https://img.shields.io/pypi/status/mesomath)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/mesomath/badge/?version=stable)](https://mesomath.readthedocs.io/stable/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)

MesoMath is a high-precision computational framework designed for epigraphists, historians, and mathematicians working with Sumerian and Babylonian sexagesimal systems. 

From the Old Babylonian period (Nippur) to Late Babylonian administrative records, MesoMath bridges the gap between ancient clay tablets and modern data science.

---

## ✨ What's New in v2.0.0?
This major release transforms MesoMath from a set of utilities into a fully integrated Metrological Ecosystem.

* **Enhanced `ibabcalc` Console:** New **IPython 9**-based interactive environment providing a clean, "Scribal Console" workspace for power users.
* **Jupyter Integration:** New `nb_utils` module for high-fidelity rendering of cuneiform tables and academic documentation within notebooks.
* **🧮 Dimensional Awareness:** Perform complex geometric calculations (e.g., `Volume / Surface = Height`) directly with metrological objects.
* **🔍 Integrated Lookup:** The new `MesoM.lookup()` engine allows for reverse metrological searches—identify physical measures from abstract sexagesimal values.
* **🔄 Bidirectional Conversion:** seamless translation between SI units and Old Babylonian metrology.
* **📜 Epigraphic Engine:** Native support for professional transliteration and Unicode Cuneiform rendering.
* **🏗️ Construction Metrology:** Dedicated support for Brick Metrology (`Bbri`) and logistics.


---

## 🚀 Quick Start

### Installation

```bash
$ pipx install mesomath
````
### The Scribal Console
Launch the advanced interactive environment:

```bash
$ ibabcalc
```

### Basic Interaction

```python
from mesomath.npvs import Blen, Bsur

# Dimensional arithmetic
width = Blen('3 ninda')
area = Bsur('1 sar')

# The division engine
length = area / width
print(length.prtf())  # Output: '1/3 ninda'
```

### Cuneiform & Transliteration

```python
from mesomath.npvs import Bcap

vol = Bcap('3 bariga 2 ban')
print(vol.translit)     # Output: '3(barig) 2(ban2) še'
print(vol.cuneiform())  # Output: 𒑗 𒑐 𒊺
```

-----

## 📚 Documentation & Research

The full documentation is available at [ReadTheDocs](https://mesomath.readthedocs.io/).

*Note: We are currently updating the documentation to reflect the 2.0.0 changes. If you find any discrepancies, please check our [Issue Tracker](https://www.google.com/search?q=https://github.com/youruser/mesomath/issues).*

-----

## 🏛️ Acknowledgments

MesoMath's metrological logic is based on the seminal work of **Christine Proust** (e.g., *Tablettes mathématiques de Nippur*, 2007) and the standard Babylonian metrological lists.

-----

**Developed with 🖋️ and 🏺 by [jccsvq](https://github.com/jccsvq?tab=repositories)**


