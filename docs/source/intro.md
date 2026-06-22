
# Introduction to MesoMath ({{ release }})

**MesoMath** is more than just a calculator; it is a digital bridge to the mathematical and astronomical mind of the ancient Mesopotamian scribe. While modern mathematics relies on abstract decimal notation, the Old Babylonian period (c. 1900–1600 BCE) developed a sophisticated sexagesimal (base-60) system that combined floating-point arithmetic with a complex web of metrological units and elastic, horizon-based timekeeping frameworks.

## The MesoMath Ecosystem

MesoMath 2.1.0 expands its unified workflow by transitioning into a comprehensive metapackage. It couples core scribal mathematics with advanced historical chronology and archaeoastronomy, tailored to the needs of researchers from quick terminal calculations to reproducible academic analysis:

### 1. Command-Line Environments (CLI)

* **`babcalc`**: The standard toolkit. A lightweight, dedicated REPL (Read–Eval–Print Loop) environment. It is architected for speed and efficiency, making it the ideal choice for rapid calculations and script automation without complex dependency overhead.
* **`ibabcalc`**: The "Scribal Console." Built upon **IPython 9**, this advanced environment is designed for power users. It offers a refined, distraction-free workspace featuring object introspection, robust command history, and a pre-configured metrological namespace.

### 2. Research & Educational Environments (Jupyter & Cloud)

* **Jupyter Notebooks**: The gold standard for reproducible research. MesoMath includes specialized utilities (`nb_utils`) that allow for high-fidelity rendering of cuneiform tables, statistical analysis, and rigorous documentation of the calculation process.
* **Zero-Install Experience (Binder)**: Launch a fully functional MesoMath instance directly in your browser. Our Binder integration provides immediate access to interactive tutorials, curated case studies (such as the *Plimpton 322* analysis), and live terminal sessions.

[](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)

-----

## Core Concepts

### Sexagesimal Arithmetic and Metrology (`mesomath`)

* **Dimensional Intelligence**: MesoMath understands geometric relationships. It performs "dimensional descent"—such as dividing volume by area to derive height—by automatically managing historical metrological ratios.
* **Fractional Precision**: With the introduction of the `BabF` engine, the framework natively handles sexagesimal fraction arithmetic, ensuring strict base-60 mathematical representation without floating-point rounding artifacts.
* **Bidirectional Conversion**: Utilizing the `@classmethod .from_si()`, researchers can bridge the gap between 21st-century metrics (meters, kilograms) and Babylonian units instantly.
* **Analytical Inference**: The `.lookup()` engine serves as a metrological detective, helping to identify physical magnitudes even from fragmented numerical data found on damaged tablets.

### Epigraphic Authenticity

The MesoMath engine does not merely compute; it documents. All results can be exported into **Old Babylonian Transliteration** or **Unicode Cuneiform**, respecting the variations of sign usage inherent to different metrological contexts.

### Historical Chronology & Timekeeping (`mesotimes`)

* **Elastic Day Metrics (`BabylonianDay`)**: Rather than relying on rigid modern 24-hour grids, MesoMath simulates localized Mesopotamian timekeeping. It models shifting sunset-to-sunset day boundaries, spatial time degrees (`UŠ`), double-hours (`bēru`), and dynamic nocturnal watches (*maṣṣarātu*).
* **Internal Database of Historical Registers**: Based on **Parker, R. and Dubberstein, W.** (1971). *Babylonian Chronology: 626 B.C.–A.D. 75 (2nd Edition)*. Providence: Brown University Press.
* **Calendrical Matrix Dispatcher**: The `bab_year_calendar()` engine dynamically routes timeline queries. It builds structural annual tables matching empirical cuneiform records (`kingdates`), continuous Seleucid Era structures, or idealized proleptic mathematical lunations when handling chronological record gaps.

### Archaeoastronomy

* **Precise Event Ephemeris**: Calculated directly with the [`pymeeus` library](https://github.com/architest/pymeeus) (VSOP87, ELP85) up to the current limit of knowledge of the parameter `Delta T`.
* **Internal Database of Historical Eclipses**: Solar and Lunar eclipses visible at Kish (total and partial) based on the [*Five Millennium Canon of Eclipses* by Fred Espenak and Jean Meeus](https://eclipse.gsfc.nasa.gov/SEpubs/5MCSE.html).
* **Search of Heliacal and Acronychal Rising of Stars**: Precise dating and dissection/tomography of the twilight lights to reveal the temporal evolution of the star/twilight-background contrast.

-----

## Project Architecture

MesoMath has shifted into a structural metapackage architecture, decoupling core scribal metrologies and arithmetic (`mesomath`) from chronological timelines and ephemeris tracking subsystems (`mesotimes`):

1. **The `mesomath` Package Core Engine**:
   * `babn.py`: Arithmetic foundation (sexagesimal integer logic, reciprocal algorithms).
   * `babf.py`: Sexagesimal fraction arithmetic and base-60 rational representations.
   * `npvs.py`: Metrological backbone (`MesoM` base class and magnitude-specific subclasses).
   * `hamming.py`: High-performance interface for regular numbers.

2. **The `mesotimes` Package Core Engine**:
   * `date.py`: Chronological, calendrical, and astronomical dispatchers (`ChronDate`).
   * `stars.py` and `visibility.py`: Search and analysis of heliacal/acronychal star phenomena.

3. **Unified API**: Legacy standalone utilities (formerly `mtlookup`, `bmultable`) are integrated directly into the core classes, streamlining the developer experience. Methods like `Blen.lookup()` or `BabN.multable()` are now standard.

4. **Export Layer**: Native support for professional-grade tables in **Markdown**, **HTML**, and **LaTeX**.

-----

## About the Author

**MesoMath** is developed by a retired Professor of Astrophysics from the University of Seville, with over four decades of experience in theoretical mechanics, numerical analysis, and geostatistics.

A lifelong enthusiast of historical computing methods—from slide rules and logarithmic tables to the study of the Oriental abacus—the author created MesoMath to fill a gap in digital Assyriology: the need for an agile, command-line-driven environment for sexagesimal and metrological computation.

What began as a personal hobby to explore the "alternative path" of Mesopotamian mathematics has evolved into this framework. MesoMath is a tribute to the scribal tradition, built with the same precision used to model celestial orbits.

