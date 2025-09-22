# Release Notes

## v1.1.0

* Preparing documentation using [Sphinx](https://www.sphinx-doc.org/en/master/index.html)
* Bug fix: `mtlookup.py` now admit integer values e.g.: `$ mtlookup -t L 123`
* Code reformated with `Black`. [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
*  Added method `.metval()` to `_MesoM` class.
* Added basic support for actual or academic unit names in methods `.__init__()`, `.scheme()` and `.prtf()` so that strings of type: `(1 dis) 1/3 kuš3 (4 dis) šu-si` can be obtained in output and used in input.
* `metrotable` and `mtlookup` utilities adapted to use *academic* names.
*  Updated tuttorials.

## v1.0.0 Initial release 2025-09-16.

* The intended functionality of the package is complete and testing (intensive but not exhaustive) is satisfactory.