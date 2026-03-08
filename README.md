[![Docs](https://app.readthedocs.org/projects/mesomath/badge/?version=latest)](https://mesomath.readthedocs.io/)
![PyPI - Version](https://img.shields.io/pypi/v/mesomath)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jccsvq/mesomath-nb/main?urlpath=%2Fdoc%2Ftree%2Fnotebooks%2Findex.ipynb)


![mesomath](docs/source/_static/mesomath.png) 

# MesoMath: Mesopotamian Calculator and Metrology Tools



## Overview

**MesoMath** is a complete ecosystem for the study of ancient **Mesopotamian Mathematics** written in pure `Python3`. In this sense, it incorporates:

* the arithmetic of natural **sexagesimal numbers**, mainly in their *floating* aspect, as performed by Babylonian scribes and their apprentices in ancient times. 
* the arithmetic of **physical quantities**, length, surface, etc. described using the metrology of the **Old Babylonian Period** (but also extensible to other periods).

For this purpose, MesoMath provides four command-line applications:

* `babcalc`: a custom `Python3` REPL, the **Babylonian Calculator**, with tab completion and history support for interactive use and fully scriptable for batch processing.
* `metrotable`: An utility to create custom metrological list and tables.
* `mtlookup`: An utility for direct/reverse lookup in metrological tables.
* `bmultable`: A simple utility to recreate the sexagesimal multiplication tables used by the Babylonian scribes.

It has been inspired by the arithmetic and metrological parts of [MesoCalc](https://github.com/BapMel/mesocalc) by Baptiste Mélès. 

The package includes:

* the `mesomath` module containing four main submodules:

    *  `babn.py`: Containing the class `BabN` for *Babylonian* (sexagesimal) *numbers*.
    *  `npvs.py`: Containing *metrological* classes for measurements of distance, area, volume, capacity, weight,...
    *  `hamming.py`: For generating lists of *regular numbers*, as well as the [`SQLite3`](https://www.sqlite.org/) database of these used by the `BabN` class.
    *  `parser.interpreter.py`: Formal grammar engine to handle metrological string parsing.


* four application submodules:

    * `babcalc.py` implementing the interactive *Babylonian calculator* `babcalc`.
    * `metrotable.py`: implementation of the metrological table printing application `metrotable`.
    * `mtlookup.py`: implementation of the metrological table search application `mtlookup`.
    * `multable.py`: implementation of the sexagesimal multiplication table printing utility `bmultable`.

* Test files for `pytest` in the `test` subdirectory.
* [`Sphinx`](https://www.sphinx-doc.org/en/master/) source files for the documentation in the `docs` subdirectory, including tutorials for the four applications: `babcalc`, `metrotable`, `mtlookup` and `bmultable`.

## A glimpse into interactive usage

```bash
$ babcalc


Welcome to Babylonian Calculator 1.3.0
    ...the calculator that every scribe should have!

Use: bn(number) for sexagesimal calculations
Metrological classes: bl, bs, bv, bc, bw, bG, bS and bb loaded.
Use exit() or Ctrl-D (i.e. EOF) to exit

jccsvq fecit, 2025.

--> a = bn(111)              # define a
--> a
1:51
--> b = bn('24:17')          # define b
--> b
24:17
--> a * b                    # product
44:55:27
--> 

--> bn(2).sqrt()             # approximate floating square root of 2
1:24:51:10:7:46              # compare to YBC 7289

--> cash=bw('1 mana')        # we have 1 mana of silver
--> quota=bl('2 ninda')      # a worker can excavate 2 ninda of channel length per day
--> wage=bw('10 se')         # the daily wage in silver
--> n=cash.dec/wage.dec      # number of wages we can afford
--> n
1080.0
--> length=bl(n*quota.dec)   # total length of canal we can afford to excavate
--> length
1 danna 6 us
--> length.explain()         # what kind of quantity is `length`?
This is a Babylonian length meassurement: 1 danna 6 us
    Metrology:  danna <-30- us <-60- ninda <-12- kus <-30- susi
    Factor with unit 'susi':  1 30 360 21600 648000
Meassurement in terms of the smallest unit: 777600 (susi)
Sexagesimal floating value of the above: 3:36
Approximate SI value: 12960.0 meters
--> length.                  # press <Tab> twice to see options
length.aname             length.prtf(             length.silver_payments( 
length.cfact             length.prtsex            length.siu              
length.dec               length.rations(          length.siv              
length.dec2un(           length.scheme(           length.title            
length.explain()         length.sex(              length.ubase            
length.labor_cost(       length.sexsys(           length.ufact            
length.list              length.SI()              length.uname            
length.metval()          length.si()             
--> length.

```

## Power Usage and Scripting

**MesoMath** is designed to be fully scriptable and integrable into automated workflows, whether you are on Linux, macOS, or Windows.

### Running Scripts
You can write your metrological logic in a file (e.g., `myscript.py`):

```python
from mesomath.npvs import Blen

a = Blen(111117)
print(32*'-')
a.explain()
```

And execute it through `babcalc`:

```bash
$ babcalc myscript.py

```

### Stream Processing (Pipes)

All utilities support standard input/output streams. You can chain MesoMath with other command-line tools to filter and process data:

```bash
$ cat myscript.py | babcalc | grep "surface" > output.txt

```
This makes MesoMath a powerful engine for large-scale archaeological or mathematical data processing.

### Extending metrology

MesoMath is designed to work with the metrology of the Old Babylonian period, but it can be extended to use the metrology of other periods. For example, for the Late Babylonian period, we can start by defining a class `LBcap` for the capacities in a file `lateb.py`:

```python
from mesomath.npvs import Bcap, Bvol


class LBcap(Bcap):  # Capacity
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period capacity units:

        **gur <-5- bariga <-6- ban2 <-10- sila3 <-10- GAR**

    """

    title: str = "Late Babylonian capacity meassurement"
    uname: list[str] = "gar sila ban bariga gur".split()
    aname: list[str] = "GAR sila3 ban2 bariga gur".split()
    ufact: list[int] = [10, 10, 6, 5]
    cfact: list[int] = [1, 10, 100, 600, 3000]
    siv: float = 0.1
    siu: str = "litres"
    ubase: int = 3  # bariga

    def vol(self) -> object:
        """Convert capacity to volume meassurement

        :return: volume meassurement
        :rtype: "Bvol"
        """
        return LBvol(int(round(self.dec/(100/6))))

class LBvol(Bvol):  # Volume
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period volume units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """
    title: str = "Late Babylonian volume meassurement"
    
    def cap(self) -> object:
        """Convert volume to capacity meassurement"""
        return LBcap(int(round(self.dec*(100/6))))
```

and then:

```python
$ babcalc -i lateb.py 
--> a = LBcap('1000 sila')
--> b = a.vol()
--> b
3 gin 60 se
--> b.explain() 
This is a Late Babylonian volume meassurement: 3 gin 60 se
    Metrology:  gan <-100- sar <-60- gin <-180- se
    Factor with unit 'se':  1 180 10800 1080000
Meassurement in terms of the smallest unit: 600 (se)
Sexagesimal floating value of the above: 10
Approximate SI value: 0.9999999999999999 cube meters
--> c=b.cap() 
--> c
3 gur 1 bariga 4 ban
--> c.SI() 
'1000.0 litres'
--> c.explain() 
This is a Late Babylonian capacity meassurement: 3 gur 1 bariga 4 ban
    Metrology:  gur <-5- bariga <-6- ban <-10- sila <-10- gar
    Factor with unit 'gar':  1 10 100 600 3000
Meassurement in terms of the smallest unit: 10000 (gar)
Sexagesimal floating value of the above: 2:46:40
Approximate SI value: 1000.0 litres
-->
--> LBcap.metrolist('1 bariga','3 bariga', '1 ban',1)
1 bariga             | 1              
1 bariga 1 ban       | 1:10           
1 bariga 2 ban       | 1:20           
1 bariga 3 ban       | 1:30           
1 bariga 4 ban       | 1:40           
1 bariga 5 ban       | 1:50           
2 bariga             | 2              
2 bariga 1 ban       | 2:10           
2 bariga 2 ban       | 2:20           
2 bariga 3 ban       | 2:30           
2 bariga 4 ban       | 2:40           
2 bariga 5 ban       | 2:50           
3 bariga             | 3              
--> 

```

etc. but we should also redefine the rest of the classes to ensure consistency in the operations with the new units.



## Download

From the [GitHub repository](https://github.com/jccsvq/mesomath). Read below about the [installation](installation).

## Documentation

Documentation for this package is in [Read the Docs](https://mesomath.readthedocs.io/index.html).

## Install

For instance:

```bash
    $ pip install mesomath
```

or

```bash
    $ pipx install mesomath
```

to install from [pypi.org](https://pypi.org/). But you can also install from the sources, read the [documentation](https://mesomath.readthedocs.io/install.html).

## Dependencies

Depending on the version of `Python 3` installed, you may need `typing-extensions>=4.0.0`, which was added as a dependency starting with version v1.2.4. Otherwise,MesoMath only uses  standard Python modules: `math`, `itertools`, `argparse`, `os`, `re`, `types`, `typing` and `sqlite3`. 

Since version `v1.4.0` MesoMath requires `parsimonious==0.11.0`.

The dependencies expressed in `requirements.txt` are for testing and documentation building.

Tested with Python 3.11.2 and 3.12.8 under Debian GNU/Linux 12 (bookworm), 3.11.2 in x86_64 under aarch64 (raspberrypi 5) and Python 3.10.19 in Binder.

##   `babn.py`

This is the main module defining the `BabN` class for representing sexagesimal natural numbers. You can perform mathematical operations on objects of the `BabN` class using the operators +, -, *, **, /, and //, and combine them using parentheses, both in a program and interactively on the Python command line. It also allows you to obtain their reciprocals in the case of regular numbers, their approximate inverses in the general case, approximate square and cube floating roots and obtain divisors and lists of "nearest" regular numbers. See the `test-babn.py` script.

### Note:

*  Operator `/` return the approximate floating division of `a/b` for any pair of numbers.
*  Operator `//` is for the "Babylonian Division" of `a` by `b`, i.e. `a//b` returns `a` times the reciprocal of `b`, which requires `b` to be regular.

###  Use as an interactive calculator

Once MesoMath is installed, simply run:

    $ babcalc

Consult the [tutorial](https://mesomath.readthedocs.io/tutorial.html)!

## `hamming.py`

Regular or Hamming numbers are numbers of the form:

    H = 2^i * 3^j × 5^k
    
    where  i, j, k ≥ 0 

This module is used to obtain lists of such numbers and ultimately build a SQLite3 database of them up to 20 sexagesimal digits. This database is used by BabN to search for regular numbers close to a given one. See the scripts: `createDB.py` and `test-hamming.py`.

## `npvs.py`

This module defines the generic class `Npvs` for handling measurements in various units within a system. It is built using length measurements in the imperial system of units, from inches to leagues, as an example. This class is inherited by the `_MesoM` class which adapts it to Mesopotamian metrological use. The `_MesoM` class, in turn, is inherited by:

*  class `BsyG`: Babylonian counting System G (GAN2)
    * `šar2-gal <-6- šar'u <-10- šar2 <-6- bur'u <-10- bur3 <-3- eše3 <-6- iku`
*  class `BsyS`: Babylonian counting  System  (Exagesimal)
    * `šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš`
+*  class `BsyC`: Babylonian counting  System C (Common)
    * `u <-10- diš`
*  class `MesoM`: To represent physical quantities, inherited by:
    *  class `Blen`: Babylonian length system
        * `danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si`
    *  class `Bsur`: Babylonian surface system
        * `gan <-100- sar <-60- gin <-180- se`
    *  class `Bvol`: Babylonian volume system
        * `gan <-100- sar <-60- gin <-180- se`
    *  class `Bcap`: Babylonian capacity system
        * `gur <-5- bariga <-6- ban2 <-10- sila3 <-10- GAR`
    *  class `Bwei`: Babylonian weight systemgu)
        * `gu2 <-60- ma-na <-60- gin2 <-180- še`
    *  class `Bbri`: Babylonian brick counting system
        * `gan <-100- sar <-60- gin <-180- se`




Please, read the [tutorials](https://mesomath.readthedocs.io) to see how to use all these classes.


