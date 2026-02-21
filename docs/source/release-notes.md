# Release Notes

## v1.3.0 (2026-03-  )

This version marks a milestone in the evolution of MesoMath, transforming it from a fixed-system calculator into an extensible metrology environment designed for Assyriological research and administrative calculations.

### Main New Features

#### 1. Extensible and Polymorphic Metrology

The core of `npvs.py` has been refactored to allow user classes to interact natively with the system:

* **Use of `isinstance()`: The system now recognizes custom subclasses (such as height measurements or regional variants) as valid types for complex operations (e.g., Area * Height = Volume).

* **Safe extraction of `.dec`: Arithmetic has been shielded to prevent rounding errors when operating between different metrology systems.

#### 2. Economic and Administrative Management

Cost calculation methods have been integrated directly into the base class `MesoM`, available for all units of measure:

* **`rations()`**: Calculates grain rations from work volumes or capacity.

* **`silver_payments()`**: Manages silver (weight) payments with decimal precision, rounding to the smallest unit (*s*) only in the final step to ensure historical accuracy.

#### 3. Dynamic Metrological Tables (`metrolist`)

Any metrological class (including user-created ones) can now generate its own reference tables using the new `metrolist()` class method:

* Allows for quick previewing of unit progression in the `babcalc` REPL.

* Supports the use of `**kwargs` for future format expansions.

### Documentation Improvements

* **Migration to Markdown**: The main index and manuals now use MyST Markdown for more agile and readable writing.

* **Version Automation**: A system has been implemented that automatically synchronizes the version across all documentation directly from the source code.

### Internal Changes (Refactoring)

* Removal of redundant methods in `Bvol` to unify the API under `MesoM`.

* Improved robustness of the magic methods `__add__`, `__sub__`, and `__mul__`.

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