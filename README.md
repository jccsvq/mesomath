# 🏺 MesoMath v2.0.0rc1
**The Definitive Mesopotamian Metrology & Arithmetic Engine for Python.**

[![PyPI version](https://img.shields.io/pypi/v/mesomath/2.0.0rc1)](https://pypi.org/project/mesomath/2.0.0rc1/)
[![Documentation Status](https://readthedocs.org/projects/mesomath/badge/?version=develop)](https://mesomath.readthedocs.io/develop/?badge=develop)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)

MesoMath is a high-precision computational framework designed for epigraphists, historians, and mathematicians working with Sumerian and Babylonian sexagesimal systems. 

From the Old Babylonian period (Nippur) to Late Babylonian administrative records, MesoMath bridges the gap between ancient clay tablets and modern data science.

---

## ✨ What's New in v2.0.0?
This  update transforms MesoMath from a set of utilities into a fully integrated Metrological Ecosystem.

* **🧮 Dimensional Awareness:** Perform complex calculations like `Surface / Length = Length` or `Volume / Surface = Height` directly with metrological objects.
* **🛠️ Versatile Integrated Design of Metrological Lists and Tables:** from the simplest to the most complex compatible with the scribal tradition.
* **🔍 Integrated Lookup:** The new `MesoM.lookup()` method allows for reverse metrological searches—identify physical measures from abstract sexagesimal values.
* **🔄 Bidirectional Conversion** between SI values and OBP metrology.
* **📜 Epigraphic Engine:** Native support for professional transliteration and Unicode Cuneiform rendering.
* **🏗️ Construction Metrology:** Dedicated support for Brick Metrology (`Bbri`) and labor/ration logistics.
* **🛠️ Unified CLI:** Access all features from the enhanced `babcalc` REPL.

---

## 🚀 Quick Start

### Installation
```bash
pip install mesomath==2.0.0rc1
````

### Basic Interaction

```python
from mesomath.npvs import Blen, Bsur

# Dimensional arithmetic
width = Blen('3 ninda')
area = Bsur('1 sar')

# The new division engine
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


