# Release Notes

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