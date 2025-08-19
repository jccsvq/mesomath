![mesomath](mesomath.png)
## Intro

This package is intended for the arithmetic of natural sexagesimal numbers, mainly in their "floating" aspect (i.e., by removing all possible trailing sexagesimal zeros from the right), as performed by the Babylonian scribes and their apprentices in ancient times.

Inpired by the arithmetic part of Baptiste Mélès' [MesoCalc](https://github.com/BapMel/mesocalc), it aims to bring this type of calculation to Python programming and to the command line as a calculator.

`MesoMath` contains three modules:

*  `babn.py`
*  `hamming.py`
*  `mesolib.py`

one utility script:

*  `createDB.py`

one example script:

*  `example-melville.py`

and three test/demo scripts:

*  `test-babn.py`
*  `test-hamming.py`
*  `test-mesolib.py`

##   `babn.py`

This is the main module defining the `BabN` class for representing sexagesimal natural numbers. You can perform mathematical operations on objects of the `BabN` class using the operators +, -, *, **, /, and //, and combine them using parentheses, both in a program and interactively on the Python command line. It also allows you to obtain their reciprocals in the case of regular numbers, their approximate inverses in the general case, approximate square and cube floating roots and obtain divisors and lists of "nearest" regular numbers. See the `test-babn.py` script.

### Note:

*  Operator `/` return the approximate floating division of `a/b` for any pair of numbers.
*  Operator `//` is for the "Babylonian Division" of `a` by `b`, i.e. `a//b` returns `a` times the reciprocal of `b`, which requires `b` to be regular.

## `hamming.py`

Regular or Hamming numbers are numbers of the form  

    H = 2i × 3j × 5k
           where 
     i,  j,  k  ≥  0 

This module is used to obtain lists of such numbers and ultimately build a SQLite3 database of them up to 20 sexagesimal digits. This database is used by BabN to search for regular numbers close to a given one. See the scripts: `createDB.py` and `test-hamming.py`.

## `mesolib.py`

This is a rather obsolete module, as its functionality has been moved to the methods of the `BabN` class. It can be safely ignored and will likely be removed in the future. In any case, please refer to the `test-mesolib.py` script.

##  `createDB.py`

Use:

    $ python3 createDB.py

to create the default regular number database `regular.db3` in your directory.  You can also use:

    $ python3 createDB.py -o 'path/name'

to create it in a non-standar location. In this case, think of using:

    BabN.database = 'path/name'

to inform `BabN`  of its location.

##  `example-melville.py`

This script shows the application of MesoMath to the solution of two real examples given by Duncan J. Melville in: [Reciprocals and Reciprocal algorithms in Mesopotamian Mathematics (2005)](https://www.researchgate.net/publication/237309438_RECIPROCALS_AND_RECIPROCAL_ALGORITHMS_IN_MESOPOTAMIAN_MATHEMATICS)

    Searching the reciprocal of 2:5  according to D. J. Melville (2005)

    Example 1: from Table 2. Simple Reciprocal algorithm

    d1 = BabN('2:5')
    d1tail = BabN(5)
    d1head = BabN(2)
    r1 = d1tail
    r2 = r1.rec()
    r3 = d1 * r2
    r4 = r3.rec()
    r5 = r4 * r2

    Result r5 =  28:48

    Example 2: from Table 3. using "The Technique"

    r1 = d1tail
    r2 = r1.rec()
    r3 = d1head * r2
    r4 = r3+BabN(1)
    r5 = r4.rec()
    r6 = r5 * r2

    Result using "The Technique" (Table 3):  28:48