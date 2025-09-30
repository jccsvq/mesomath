# Installing MesoMath

## Using `pip` or `pipx`

Since version `v1.1.0` you can install `MesoMath` from [pypi.org](https://pypi.org/project/mesomath/) using [`pip`](https://pypi.org/project/pip/) or [`pipx`](https://pipx.pypa.io/stable/):

### `pip`

Start by creating a virtual environment anywhere convenient in your directory tree, call it whatever you like, for example: `myenv` and `cd` to that directory:

    $ python -m venv myenv
    $ cd myenv
    $ bin/python -m pip install mesomath

or perhaps:

    $ python -m venv myenv
    $ cd myenv
    $ bin/pip install mesomath

if your system intalls `pip` in the virtual environment.

This will install a repackaged version of `MesoMath` into your environment, containing the library and three commands that you can invoke as:



    $ bin/babcalc:     # the interactive calculator with all metrological classes.
    ...
    $ bin/metrotable   # for printing metrological tables
    ...
    $ bin/mtlookup     # for consulting values in metrological tables
    ...

The rest of the test scripts (test-babn.py, test-npvs.py,...) are accessible as:

    $ bin/python -m mesomath.test.test-babn
    ...
    $ bin/python -m mesomath.test.test-npvs
    ...

etc.

You can [activate/deactivate](https://docs.python.org/3/tutorial/venv.html) your virtual environment.

Consult: [Installing python packages guide](https://packaging.python.org/en/latest/tutorials/installing-packages/)

### `pipx`

If your system has `pipx` installed you don't have to worry about creating a virtual environment, `pipx` will do it and manage it for you, simply:

    $ pipx install mesomath


This will install a repackaged version of `MesoMath` in a hidden virtual environment, containing the library and three commands:

    $ babcalc:     # the interactive calculator with all metrological classes.
    ...
    $ metrotable   # for printing metrological tables
    ...
    $ mtlookup     # for consulting values in metrological tables
    ...

that should work directly, if it is not the case, try:

    $ pipx ensurepath

to expose them in your PATH.

Consult: [Getting started with `pipx`](https://pipx.pypa.io/stable/getting-started/)


## From sources

If you don't have `pip` or `pipx` on your system or don't want to bother with virtual environments, you can install `MesoMath` directly from the source and get everything working without disturbing the rest of your system. 

 1. Start by downloading the source package from its [GitHub repository](https://github.com/jccsvq/mesomath/releases/tag/v1.1.0)
 2. Unzip/Untar it to a directory of your choice
 3. cd to that directory
 4. Start reading the [tutorial](https://mesomath.readthedocs.io/tutorial.html#installation)