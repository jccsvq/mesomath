
## [2.0.0] - 2026-04-20

### Added
* **New Interactive Environments**: 
    * **`ibabcalc`**: Advanced **IPython 9** based interactive shell for power users, featuring a clean "Scribal Console" with pre-configured metrological namespaces.
    * **Jupyter Support**: New `nb_utils` module and special rendering methods (`BabN.multable_nb` and `MesoM.metronotebook`) for high-fidelity research in notebooks.
* **Cloud Experience**: Official **Binder** integration with live, zero-install notebooks for *Plimpton 322* and *Surface of Squares*.
* **Dimensional Arithmetic**: Full support for geometric division between magnitudes (e.g., `Bsur / Blen -> Blen`).
* **Interoperability**: Added `.from_si()` methods for all metrological classes, allowing instant conversion from metric units to Babylonian systems.
* **Unified API**: 
    * `.lookup()`: New reverse metrological search engine (replaces `mtlookup.py`).
    * `.multable()`: New scribal multiplication table generator (replaces `bmultable.py`).
* **Epigraphic Engine**: Native support for **Old Babylonian Transliteration** and **Unicode Cuneiform** across all core classes.
* **New Systems**: 
    * Implementation of **Proust Series** presets for standard Nippur metrology.
    * `BsyK`: New class for the **Sumerian King List** counting system.
    * `Bbri`: Enhanced support for **Brick Metrology** and logistics.
* **Export Options**: Added `.metrohtml()` and `.metrolatex()` for professional table generation.

### Changed
* **Architectural Refactor**: 
    * `.metrolist()` and `.scheme()` promoted to **class methods** for better performance and consistency.
    * All console output and tables now default to **Markdown format** for better legibility.
* **Documentation**: Major restructuring of the Tutorial and Reference sections to include `ibabcalc` and Jupyter workflows.
* **Dependencies**: Minimum requirements updated to `ipython>=9.0.0`, `traitlets>=5.0.0`, and `wcwidth` (for character alignment).

### Fixed
* **.metrolist()**: Fixed a bug where substances were not rendered with cuneiform glyphs when `cuneiform=True`.
* **Visual Alignment**: Improved Cuneiform character spacing in CLI environments via `wcwidth`.
* Several minor bugfixes identified during the RC cycle (v2.0.0rc0 - v2.0.0rc2).

### Removed
* **Legacy Apps**: The standalone scripts `metrotable.py`, `mtlookup.py`, and `bmultable.py` have been removed. Their functionality is now integrated into the core class methods.

---

### *Historical Note (Release Candidates)*
* **v2.0.0rc2** (2026-04-12): Fixes to metrological glyph rendering.
* **v2.0.0rc1** (2026-04-10): Alignment fixes for terminal output.
* **v2.0.0rc0** (2026-04-08): Initial architectural refactor and new API.

---

## [2.0.0rc2] - 2026-04-12

### Fixed
* **.metrolist() bug**: Now the substance is written with the appropriate glyphs if `cuneiform=True`.
* **Some Minor Fixes**

---

## [2.0.0rc1] - 2026-04-10

### Fixed
* **Dependencies**: Added missing `wcwidth` dependency to ensure correct visual alignment of cuneiform characters in CLI environments.

---

## [2.0.0rc0] - 2026-04-08

### Added
* **Dimensional Arithmetic**: Full support for geometric division between magnitudes (e.g., `Bsur / Blen -> Blen`).
* **Interoperability**: New `@classmethod .from_si()` for all metrological classes, allowing instant conversion from modern metric units to Babylonian objects.
* **Unified API**: 
    * `.lookup()`: New reverse metrological search engine (replaces `mtlookup.py`).
    * `.multable()`: New scribal multiplication table generator (replaces `bmultable.py`).
* **Epigraphic Engine**: Native support for **Old Babylonian Transliteration** and **Unicode Cuneiform** across all core classes.
* **Historical Series**: Implementation of the **Proust Series** presets for standard Nippur metrology.
* **New Metrologies**: 
    * `BsyK`: New class for the **Sumerian King List** counting system (years).
    * `Bbri`: Enhanced support for **Brick Metrology** and logistics.
* **Export Options**: New `.metrohtml()` and `.metrolatex()` methods for generating professional tables with full cuneiform support.

### Changed
* **Architectural Refactor**: 
    * `.metrolist()` and `.scheme()` are now **class methods**, optimized for better performance and consistency.
    * Source code reorganized for a more logical developer experience.
* **Output Format**: All console listings and tables now default to **Markdown format** for better readability and easier copy-pasting into research documents.

### Deprecated
* **Legacy Apps**: `metrotable.py`, `mtlookup.py` and `bmultable.py` are now considered **obsolete**. They are maintained in this Release Candidate for backward compatibility but **will be removed** in the final v2.0.0 stable release. Use the internal class methods instead.

---


## [1.4.0] - 2026-03-08

### Added

* **Formal Grammar Engine**: Integrated `parsimonious` (v0.11.0) to handle metrological string parsing via the new `MesoInterpreter` class.
* **New Test File**: `test_parser.py` checks that the 75 different metrological expression types generated by MesoMath are readable as valid inputs.

### Changed

* **Robust Error Handling**: Wrapped the `_MesoM.__init__` logic to intercept technical `ParseError`, `VisitationError` and `IncompleteParseError` exceptions, replacing them with user-friendly error messages.
* **Unit Normalization**: The interpreter now uses the global `normalize` function consistently across all input types to ensure unit names like `šar2-gal` map correctly to `sargal`.

### Fixed

* **Non-parseable expressions**: An issue was resolved where some metrological expressions generated by MesoMath could not be interpreted back as inputs.

### Dependencies

* Pinned `parsimonious==0.11.0` to ensure grammar stability and prevent breaking changes from future library updates.


## v1.3.0 (2026-02-28)

This version marks a milestone in the evolution of MesoMath, transforming it from a fixed-system calculator into an extensible metrology environment designed for Assyriological research and administrative calculations.

### 🚀 Main New Features

#### 1. `babcalc` Improvements

`babcalc`, the central engine of MesoMath, now has new features that make it more user-friendly and functional:

    * History is now saved between sessions.
    * Tab completion.
    * Ability to run and debug scripts in pure Python.

#### 2. Extensible and Polymorphic Metrology

The core of `npvs.py` has been refactored to allow user classes to interact natively with the system:

* **Use of `isinstance()`: The system now recognizes custom subclasses (such as height measurements or regional variants) as valid types for complex operations (e.g., Area * Height = Volume).

* **Safe extraction of `.dec`: Arithmetic has been shielded to prevent rounding errors when operating between different metrology systems.

#### 3. Economic and Administrative Management

Cost calculation methods have been integrated directly into the base class `MesoM`, available for all units of measure:

* **`.labor_cost(work_man)`**: Calculate the total number of workdays (man-days) required for a task based on standard Babylonian perfo

* **`rations()`**: Calculates grain rations from work volumes or capacity.

* **`silver_payments()`**: Manages silver (weight) payments with decimal precision, rounding to the smallest unit (*s*) only in the final step to ensure historical accuracy.

#### 4. Dynamic Metrological Tables (`metrolist`)

Any metrological class (including user-created ones) can now generate its own reference tables using the new `metrolist()` class method:

* Allows for quick previewing of unit progression in the `babcalc` REPL.

* Supports the use of `**kwargs` for future format expansions.

### 📖 Documentation Improvements

* **Smart Copy-Paste**: Code examples in the documentation now feature a "smart" copy button that automatically ignores prompts (`-->` or `$`), allowing you to paste code directly into your terminal or script.

* **Migration to Markdown**: The main index and manuals now use MyST Markdown for more agile and readable writing.

* **Version Automation**: A system has been implemented that automatically synchronizes the version across all documentation directly from the source code.

* **Standardization of the API docstrings**: The python help is more useful now.

### 🛠 Internal Changes (Refactoring)

* Significant AI-assisted refactoring

* Improved robustness of class constructors and magic methods `__add__`, `__sub__`, `__mul__`, etc.

## v1.2.4 (2025-11-24)

* Added `typing_extensions` to dependencies.

## v1.2.3 (2025-11-20)

* Fixed a bug in the `mesomath.mtlookup` module

## v1.2.2 (2025-11-18)

* Fixed a bug in the `mesomath.babn` module

## v1.2.1 (2025-11-18)

* Fixed a major bug in the `mesomath.npvs` module that caused errors in parsing string input for the `Bsur` and `Bvol` classes.
* Added Jupyter notebooks.
* Required Python version  downgraded to 3.10.

## v1.2.0 (2025-11-14)

* Important review of the code and package structure.
    - Comparing objects of the included classes with other objects that are not of their own class (or integers, in the case of `BabN` class) now raises `NotImplementedError`.
    - Classes are now hashable.
    - Method `__int__` added to all clases. Methods `__len__` and `__round__` added to `BabN` class.
    - New simple utility to print sexagesimal multiplication tables.
    - The package and repository now have a more standard structure.
    - Some test files for `pytest` added.
    - Obsolete `mesolib.py` and old test files removed.

## v1.1.1 (2025-11-05).

* Some bug fixes and other minor improvements.

## v1.1.0 (2025-09-23).

* Documentation prepared using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) now resides in  [https://mesomath.readthedocs.io/index.html](https://mesomath.readthedocs.io/index.html). It includes the tutorials.
* Bug fix: `mtlookup.py` now admit integer values e.g.: `$ mtlookup -t L 123`
* Code reformated with `Black`. [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
* Added method `.metval()` to `_MesoM` class.
* Added basic support for actual or academic unit names in methods `.__init__()`, `.scheme()` and `.prtf()` so that strings of type: `(1 dis) 1/3 kuš3 (4 dis) šu-si` can be obtained in output and used in input.
* `metrotable` and `mtlookup` utilities adapted to use *academic* names.
* Updated tutorials moved to [documentation](https://mesomath.readthedocs.io/index.html).
* Restructured and cleared repository.

## v1.0.0 Initial release 2025-09-16.

* The intended functionality of the package is complete and testing (intensive but not exhaustive) is satisfactory.