
# 🏺 MesoMath v2.1.0
**The Mesopotamian Computational Engine for Python.**

![PyPI - Version](https://img.shields.io/pypi/v/mesomath)
![PyPI - Status](https://img.shields.io/pypi/status/mesomath)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Hatch project](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pypa/hatch/master/docs/assets/badge/v0.json)](https://github.com/pypa/hatch)
[![Documentation Status](https://readthedocs.org/projects/mesomath/badge/?version=latest)](https://mesomath.readthedocs.io)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)

MesoMath is a high-precision computational framework engineered for the rigorous study of ancient Mesopotamian mathematics, metrology, chronology, timekeeping, and archaeoastronomy. It provides native command-line environments (CLI), Jupyter integration, and authentic epigraphic support (Old Babylonian transliteration and Unicode cuneiform rendering).

---

## ✨ What's New in v2.1.0?

MesoMath has evolved into a unified metapackage, structurally decoupling core arithmetic from chronological anchoring systems:

* **`mesomath` Core**: Introduces the **`BabF`** class for native sexagesimal (base-60) fractional arithmetic without floating-point rounding artifacts.
* **`mesotimes` Subsystem**: A dedicated historical engine driving:
    * **Empirical & Proleptic Chronology**: Seamless alignment with historical cuneiform registers.
    * **Elastic Timekeeping**: Shifting horizon-based day boundaries (Sunset-to-Sunset) and dynamic nocturnal watches (*maṣṣarātu*).
    * **Archaeoastronomy**: High-fidelity celestial positioning and eclipse matrices.

---

## 🚀 Quick Start

### Installation

Install the complete environment globally using `pipx` (recommended for CLI apps):

```bash
$ pipx install mesomath

```

### The Scribal Console

Launch the pre-configured advanced interactive environment:

```bash
$ ibabcalc

```

### 1. Dimensional Arithmetic & Fractions

MesoMath manages geometric dimensions and base-60 rational numbers natively:

```python
from mesomath import Blen, Bsur

# Objects understand localized metrological ratios
width = Blen('3 ninda')
area = Bsur('1 sar')

# Dimensional descent via division engine
length = area / width
print(length.prtf())  # Output: '1/3 ninda'

```

### 2. Epigraphic Authenticity

Export mathematical computations directly into cuneiform strings or scholarly transliterations:

```python
from mesomath import Bcap

vol = Bcap('3 bariga 2 ban')
print(vol.translit)   # Output: '3(barig) 2(ban2) še'
print(vol.cuneiform)  # Output: 𒑗 𒑐 𒊺

```

### 3. Chronology & Archaeoastronomy

Translate continuous timeline anchors into historical calendars and calculate complex planetary visibilities:

```python
from mesomath import ChronDate

# Instantiate a target Julian date
date = ChronDate.from_julian(-378, 5, 17)
print(date.babylonian)
# Output: 'Year 26 of Artaxerxes II, month: 2 (Aiaru), day: 14'

```

```python
# Generate localized micro-historical data grids
date.day_ephemeris(city='Susa')

```

```text
=================================================================
               MESOPOTAMIAN DAILY EPHEMERIS: SUSA                
=================================================================
  Julian Day:  1583129.5       | Civil Calendar: Julian (-378/5/17)
  Chronology:  Year 26 of Artaxerxes II, month: 2 (Aiaru), day: 14
-----------------------------------------------------------------
  SOLAR CONTEXT:
    Sunrise : 01:46 UT | Sunset : 15:32 UT
    Transit : 08:39 UT | Season : Day: 52 of spring
-----------------------------------------------------------------
  LUNAR INTERVALS (Phenomena in current lunation):
    [Neomenia] NA Interval: -68.35 min (Time from Sunset to Moonset)
    [Mid-Month] MI-MUSH:    19.77 min (Simultaneous visibility)
    [End-Month] KUR:        -894.34 min (Dawn crescent disappearance)
-----------------------------------------------------------------
  PLANETARY VISIBILITY ( Twilight vs. Arc of Vision ):
    * Mercury    -> Invisible / Glare                   (Required Av: 12.0°)
    * Venus      -> VISIBLE (Morning Star)     (Required Av: 6.0°)
    * Mars       -> VISIBLE (Morning Star)     (Required Av: 14.0°)
    * Jupiter    -> VISIBLE (Evening Star)     (Required Av: 9.0°)
    * Saturn     -> VISIBLE (Evening Star)     (Required Av: 11.0°)
=================================================================


```

```python
# Visualize the sky timeline across ancient nocturnal watches
date.night_at_a_glance(city='Susa')

```

```text
===================================================================
          NIGHT AT A GLANCE: SUSA (-378-05-17)
===================================================================
UT Hours:  09  11  13  15  17  19  21  23  01  03  05  07  09  
Local H.:  12  14  16  18  20  22  00  02  04  06  08  10  12  
-------------------------------------------------------------------
 Sky/Sun :  #############::.               .::###############
-------------------------------------------------------------------
 Moon    :              =====================                
-------------------------------------------------------------------
 Mercury :  ----------                      -----------------
 Venus   :  ------------                     ----------------
 Mars    :  -                          --------------------- 
 Jupiter :          -----------------------                  
 Saturn  :  ------------------------                    -----
===================================================================
Legend:  # Day  : Civ/Nav Twilight  . Ast Twilight    Night
         - Planet above horizon     = Moon above horizon


```

---

## 📚 Documentation

The complete user manual, tutorials, and mathematical references are available at [mesomath.readthedocs.io](https://mesomath.readthedocs.io).

---

## 🏛️ Acknowledgments & Sources

* **Mathematical Metrology**: Structured upon the breakthrough historical analyses of **Christine Proust** (*Tablettes mathématiques de Nippur*, 2007) and canonical scribal lexical lists.
* **Archaeoastronomy & Eclipses**: Driven by the raw ephemeris computational methods and historical eclipse logs compiled in NASA's *Five Millennium Canon of Eclipses* by **Fred Espenak and Jean Meeus**.
* **Chronological Registers**: Grounded on the empirical data frameworks from *Babylonian Chronology: 626 B.C. – A.D. 75*, by **Richard A. Parker and Waldo H. Dubberstein** (2nd edition, Brown University Press, 1971).

---

**Developed by [jccsvq](https://github.com/jccsvq?tab=repositories)**

