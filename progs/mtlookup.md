# `mtlookup` tutorial

Jesús Cabrera ([jccsvq](https://jccsvq.github.io/))(*), 2025.

>(*) At gmail.com

## Introduction

Python3 command line application based on [MesoMath](https://github.com/jccsvq/mesomath) to search for the abstract number that corresponds to a measure or to list measures that correspond to a given abstract number (option: `-r`).

## Installation

Please refer to the installation of [`metrotable`](https://jccsvq.github.io/mesomath/progs/metrotable.html) and follow the same steps.

## How to use

### Options:

    $ mtlookup -h

or

    $ mtlookup --help

list the program options:

    usage: mtlookup [-h] [-t {L,Lh,S,V,C,W,SysG,SysS}] [-r] [-f FORCE] [-v] VALUE

    Prints abstract number corresponding to a meassure or lists measures having an
    abstract number.

    positional arguments:
      VALUE                 Value

    options:
      -h, --help            show this help message and exit
      -t {L,Lh,S,V,C,W,SysG,SysS}, --type {L,Lh,S,V,C,W,SysG,SysS}
                            Metrology to use (default: None)
      -r, --reverse         Reverse lookup ,lists measures having an abstract
                            number (default: False)
      -f FORCE, --force FORCE
                            Force base unit to number FORCE (default: -1)
      -v, --verbose         Prints more information (default: False)

    jccsvq fecit, 2025. Public domain.

### Metrologies

Metrologis selected with the options `-t` or `--type`:

* L:   length meassurements
* Lh:   length meassurements (Heights)
* S:   surface meassurements
* V:   volume meassurements
* C:   capacity meassurements
* W:   weight meassurements
* SysS:   System S to count objects
* SysG:   System G to count objects

### Direct search

Returns the abstract value corresponding to a measurement in a given metrology.

    $ mtlookup -t L '1 us 30 ninda' 

returns:

    1 us 30 ninda  ->  1:30

You can use the verbose options `-v` or `--verbose`:

    $ mtlookup -t L '1 us 30 ninda' --verbose

    Abstract number for  Babylonian length meassurement
        Base unit:  ninda
    ========================================================
    1 us 30 ninda  ->  1:30 Reciprocal:  40


### Reverse search

With the `-r` or `--reverse` options you get a list of measures that match the given abstract number:

    $ mtlookup -t L 1.30 -r 

    Looking for  Babylonian length meassurements with abstract =  1.30
        Base unit:  ninda
    ========================================================
    10800 danna  <-  1:30
    180 danna  <-  1:30
    3 danna  <-  1:30
    1 us 30 ninda  <-  1:30
    1 ninda 6 kus  <-  1:30
    9 susi  <-  1:30

    $ mtlookup -t L 1.30 -r -v

    Looking for  Babylonian length meassurements with abstract =  1.30
        Base unit:  ninda
    ========================================================
    10800 danna 
        Equiv.:  116640000.0 meters 
        Abstract:  1:30
    180 danna 
        Equiv.:  1944000.0 meters 
        Abstract:  1:30
    3 danna 
        Equiv.:  32400.0 meters 
        Abstract:  1:30
    1 us 30 ninda 
        Equiv.:  540.0 meters 
        Abstract:  1:30
    1 ninda 6 kus 
        Equiv.:  9.0 meters 
        Abstract:  1:30
    9 susi 
        Equiv.:  0.15 meters 
        Abstract:  1:30

In some cases, due to the discrete nature of the measurements and rounding, the last rows of the list only show approximate values:

    $ mtlookup -r -t L 6.40.38 

    Looking for  Babylonian length meassurements with abstract =  6.40.38
        Base unit:  ninda
    ========================================================
    2884560 danna  <-  6:40:38
    48076 danna  <-  6:40:38
    801 danna 8 us  <-  6:40:38
    13 danna 10 us 38 ninda  <-  6:40:38
    6 us 40 ninda 7 kus 18 susi  <-  6:40:38
    6 ninda 8 kus 3 susi  <-  6:40:30
    1 kus 10 susi  <-  6:40
