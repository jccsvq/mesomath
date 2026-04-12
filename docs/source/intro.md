
# Introduction to MesoMath

**MesoMath** is not just a calculator; it is a digital bridge to the mathematical mind of the ancient Mesopotamian scribe. While modern mathematics relies on abstract decimal notation, the Old Babylonian period (c. 1900–1600 BCE) developed a sophisticated sexagesimal (base-60) system that combined floating-point arithmetic with a complex web of metrological units.

## Core Concepts

### 1. Sexagesimal Arithmetic (`babn.py`)

Unlike modern calculators, MesoMath treats numbers in their "floating" aspect. In the Babylonian context, the absolute value of a number often depended on its metrological context rather than a fixed decimal point. The `BabN` class implements this logic, allowing for:

* **Reciprocal-based division**: Traditional Babylonian division was performed by multiplying by the reciprocal of "regular" numbers.
* **Hamming Numbers**: Integration with a SQLite database to handle regular numbers up to 20 sexagesimal digits.

### 2. Metrological Systems (`npvs.py`)

The project manages physical quantities through a hierarchy of Non-Place-Value Systems (NPVS).

* **Inheritance**: All metrological classes (length, area, volume, capacity, weight, and bricks) inherit from a generic `MesoM` class.
* **Interoperability**: You can convert between systems—such as finding the capacity of a grain pile from its measured volume—using historically accurate factors.


## Why version {{ release }}?

Version 2.0.0 represents a complete architectural overhaul of the project. While previous versions focused on standalone calculations, this release transforms MesoMath into a **unified metrological ecosystem**.

Key advancements in this version include:

* **Dimensional Intelligence**: The system now understands geometric relationships. It can perform dimensional descent (e.g., dividing a Volume by a Surface to find Height) while automatically managing the complex historical ratios (like the implicit *1-kuš₃* thickness in volume calculations).
* **Epigraphic Authenticity**: A new dedicated engine renders results in professional Old Babylonian transliteration and Unicode Cuneiform, respecting the specific sign variations for different metrological contexts.
* **Bidirectional Modern Integration**: The `@classmethod .from_si()` allows researchers to bridge the gap between 21st-century field measurements (meters, kilograms) and ancient units with a single command.
* **Analytical Inference**: The new `.lookup()` method acts as a "metrological detective," allowing users to identify physical magnitudes from isolated abstract numbers found on broken tablets.

---

## Project Structure

The MesoMath ecosystem is now organized into a streamlined, object-oriented hierarchy that prioritizes the researcher's workflow:

### 1. The Core Engine
* **`babn.py`**: The arithmetic heart. Handles sexagesimal logic, floating-point ambiguity, and advanced reciprocal algorithms.
* **`npvs.py`**: The metrological skeleton. Contains the `MesoM` base class and all dimensional subclasses (`Blen`, `Bsur`, `Bvol`, `Bcap`, `Bwei`, `Bbri`).
* **`hamming.py`**: A high-performance database interface for managing "Regular Numbers" (Hamming numbers) used in scribal division.

### 2. The Unified CLI (`babcalc`)
Following the philosophy of "everything inside the class," the legacy standalone utilities (`mtlookup`, `bmultable`, `metrotable`) have been integrated directly into the core library as methods. 
* **`babcalc`** remains the primary entry point—a specialized REPL environment for interactive math and metrology.
* **Legacy utilities** are currently maintained as a compatibility layer but are officially deprecated in favor of internal methods like `Blen.lookup()` or `BabN.multable()`.

### 3. The Visual & Export Layer
* **`glyphs.py`**: Manages the mapping of substance symbols and cuneiform characters.
* **Export Methods**: Native support for generating professional research tables in **Markdown**, **HTML**, and **LaTeX** directly from metrological objects.

### 4. Interactive & Educational Labs
* **Jupyter Notebooks**: Exploratory environments available via Binder for visual learning and complex data analysis. [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)

## About the Author

**MesoMath** is developed by a retired Professor of Astrophysics from the University of Seville (Spain), with over four decades of experience in theoretical mechanics, numerical analysis, and geostatistics. 

A lifelong enthusiast of historical computing methods —from slide rules and logarithmic tables to a deep study of the Oriental abacus— the author created MesoMath to fill a gap in digital Assyriology: the need for an agile, command-line-driven environment for sexagesimal and metrological computation.

What began as a personal hobby to explore the fascinating "alternative path" of Mesopotamian mathematics has evolved into this framework. MesoMath is a tribute to the scribal tradition, built with the same precision used to model celestial orbits or geostatistical maps.