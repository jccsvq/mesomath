# 🏺 MesoMath v2.2
**The Mesopotamian Computational Engine for Python.**

[![PyPI - Version](https://img.shields.io/pypi/v/mesomath.svg)](https://pypi.org/project/mesomath/)
[![PyPI - Status](https://img.shields.io/pypi/status/mesomath.svg)](https://pypi.org/project/mesomath/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Hatch project](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pypa/hatch/master/docs/assets/badge/v0.json)](https://github.com/pypa/hatch)
[![Documentation Status](https://readthedocs.org/projects/mesomath/badge/?version=latest)](https://mesomath.readthedocs.io)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?labpath=notebooks%2Findex.ipynb)

MesoMath is a high-precision computational framework engineered for the rigorous study of ancient Mesopotamian:

* **Mathematics**
  * Sexagesimal integer arithmetic (absolute and floating)
  * Fraction arithmetic
* **Metrology**
  * Old Babylonian Period metrology (length, surface, volume, weight, capacity, and bricks)
  * User-extensible framework for other historical periods
  * NPVS Systems S, G, C, and K
  * Socio-economic applications
* **Chronology**
  * Based on Parker and Dubberstein (1971) for the period 626 B.C. – A.D. 75
  * *Proleptic* lunar calendar engine for other historical eras
* **Timekeeping & Archaeoastronomy**
  * Lunar and Planetary Ephemerides
  * Heliacal and Acronychal Rising of stars (Atmospheric 3D scattering models)
  * Built-in catalog of relevant Mesopotamian astronomical sites
  * Built-in catalog of critical historical stars
  * Custom user-defined sites and stars support

MesoMath provides:
* **Native Command-Line Environments (CLI)**: `babcalc` (basic) and `ibabcalc` (full-featured interactive shell).
* **Jupyter Notebook Integration** for reproducible research.
* **Authentic Epigraphic Support**: Old Babylonian transliteration standards and Unicode cuneiform rendering.

---

## ✨ What's New in v2.2.0?

MesoMath v2.2.0 introduces the `BabStar` class, enabling high-fidelity search, physical contrast tracking, and multi-day **Twilight Tomography** for Heliacal and Acronychal stellar phenomena.

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
print(vol.cuneiform)  # Output: itri  samot 𒊺

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
    * Mercury    -> Invisible / Glare          (Required Av: 12.0°)
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
    Night at a Glance: Susa (-378-05-17)
===================================================================
UT Hours:  09  11  13  15  17  19  21  23  01  03  05  07  09  
Local H.:  12  14  16  18  20  22  00  02  04  06  08  10  12  
-------------------------------------------------------------------
 Sky/Sun :  #############::.               .::###############
-------------------------------------------------------------------
 Moon    :               =====================                 
-------------------------------------------------------------------
 Mercury :  ----------                     -----------------
 Venus   :  ------------                   ----------------
 Mars    :  -                           --------------------- 
 Jupiter :            -----------------------                  
 Saturn  :  ------------------------                     -----
===================================================================
Legend:  # Day  : Civ/Nav Twilight  . Ast Twilight    Night
         - Planet above horizon     = Moon above horizon

```

```python
# Search for Sirius' Heliacal Rising in 378 BCE
from mesomath import BabStar

sirius = BabStar.from_catalog("Sirius")
sirius.search_phenomena(-378)

```

```text
Search for Sirius Heliacal Appearance in the East before sunrise:
======================================================================
Search starting at Babylon:  -378-01-1.0
   First sight found at:  -378-07-23.08 (JD= 1583196.582765)
           Rising angle:  55.912d
----------------------------------------------------------------------

```

```python
# Generates a 2-day contrast time-series report at 6-minute intervals
sirius.twilight_tomography(year=-378, phenomena="heliacal", city="Babylon", k=0.20, day_offset=(0, 1))

```

```text
Search for Sirius Heliacal Appearance in the East before sunrise:
======================================================================
Search starting at Babylon:  -378-01-1.0
   First sight found at:  -378-07-23.08 (JD= 1583196.582765)
           Rising angle:  55.912d
----------------------------------------------------------------------
Scanning Sirius visibility in Babylon ( -378-07-23.0)
at 6 sidereal minutes interval (backward)
Day Offset: 0
Current Extinction Coefficient value: k = 0.2
|sun_ele |star_ele |     phi |Vis. |m_real | m_lim | Contrast
|--------|---------|---------|-----|-------|-------|---------------------
| -0.041 |  10.885 |  54.736 | No  | -0.43 | -5.78 | 
| -2.014 |   9.766 |  54.943 | No  | -0.32 | -3.69 | 
| -3.131 |   8.641 |  54.949 | No  | -0.18 | -2.52 | 
| -4.239 |   7.510 |  54.956 | No  | -0.00 | -1.35 | 
| -5.338 |   6.376 |  54.965 | No  |  0.23 | -0.19 | 
| -6.428 |   5.242 |  54.975 | Yes |  0.54 |  0.96 | ###
| -7.507 |   4.112 |  54.988 | Yes |  0.99 |  2.08 | ########
| -8.576 |   2.995 |  55.006 | Yes |  1.65 |  3.15 | ############
| -9.635 |   1.910 |  55.033 | Yes |  2.68 |  4.14 | ###########
|-10.681 |   0.897 |  55.081 | Yes |  4.33 |  4.94 | ####
-------------------------------------------------------------------------
Scanning Sirius visibility in Babylon ( -378-07-22.0)
at 6 sidereal minutes interval (backward)
Day Offset: 1
Current Extinction Coefficient value: k = 0.2
|sun_ele |star_ele |     phi |Vis. |m_real | m_lim | Contrast
|--------|---------|---------|-----|-------|-------|---------------------
| -1.888 |   9.028 |  54.332 | No  | -0.23 | -3.84 | 
| -3.004 |   7.899 |  54.339 | No  | -0.07 | -2.66 | 
| -4.111 |   6.765 |  54.347 | No  |  0.14 | -1.49 | 
| -5.209 |   5.631 |  54.356 | No  |  0.42 | -0.33 | 
| -6.298 |   4.498 |  54.367 | No  |  0.81 |  0.81 | 
| -7.376 |   3.376 |  54.382 | Yes |  1.39 |  1.93 | ####
| -8.444 |   2.277 |  54.404 | Yes |  2.27 |  3.01 | #####
| -9.501 |   1.232 |  54.441 | Yes |  3.68 |  4.01 | ##
|-10.546 |   0.297 |  54.506 | No  |  5.89 |  4.85 | 
-------------------------------------------------------------------------

```

---

## 📚 Documentation

The complete user manual, tutorials, and mathematical references are available at [mesomath.readthedocs.io](https://mesomath.readthedocs.io).

---

## 🏛️ Acknowledgments & Sources

* **Mathematical Metrology**: Structured upon the breakthrough historical analyses of **Christine Proust** (*Tablettes mathématiques de Nippur*, 2007) and canonical scribal lexical lists.
* **Archaeoastronomy & Eclipses**: Driven by the raw ephemeris computational methods and historical eclipse logs compiled in NASA's *Five Millennium Canon of Eclipses* by **Fred Espenak and Jean Meeus**.
* **Chronological Registers**: Grounded on the empirical data frameworks from *Babylonian Chronology: 626 B.C. – A.D. 75*, by **Richard A. Parker and Waldo H. Dubberstein** (2nd edition, Brown University Press, 1971).
* **Ephemeris Validation**: Elwood C. Downey's **XEphem** has been continuously utilized during development as an independent computational baseline to audit the mathematical accuracy of the underlying engine.

---

**Developed by [jccsvq**](https://github.com/jccsvq?tab=repositories)
