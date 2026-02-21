
# Introduction to `mesomath`

`mesomath` is not just a calculator; it is a digital bridge to the mathematical mind of the ancient Mesopotamian scribe. While modern mathematics relies on abstract decimal notation, the Old Babylonian period (c. 1900–1600 BCE) developed a sophisticated sexagesimal (base-60) system that combined floating-point arithmetic with a complex web of metrological units.

## Core Concepts

### 1. Sexagesimal Arithmetic (`babn.py`)

Unlike modern calculators, `mesomath` treats numbers in their "floating" aspect. In the Babylonian context, the absolute value of a number often depended on its metrological context rather than a fixed decimal point. The `BabN` class implements this logic, allowing for:

* **Reciprocal-based division**: Traditional Babylonian division was performed by multiplying by the reciprocal of "regular" numbers.
* **Hamming Numbers**: Integration with a SQLite database to handle regular numbers up to 20 sexagesimal digits.

### 2. Metrological Systems (`npvs.py`)

The project manages physical quantities through a hierarchy of Non-Place-Value Systems (NPVS).

* **Inheritance**: All metrological classes (length, area, volume, capacity, weight, and bricks) inherit from a generic `MesoM` class.
* **Interoperability**: You can convert between systems—such as finding the capacity of a grain pile from its measured volume—using historically accurate factors.

## Why version {{ release }}?

This version marks a transition from pure calculation to **simulation of administrative tasks**. With the introduction of `rations()` and `silver_payments()` in the base metrology classes, the library now supports the analysis of historical economic documents directly from their raw measurements.

## Project Structure

The ecosystem is divided into three main pillars:

1. **The Core Library**: `babn.py`, `npvs.py`, and `hamming.py`.
2. **The Toolset**: Command-line utilities (`babcalc`, `metrotable`, `mtlookup`, `bmultable`) designed for the shell-oriented researcher.
3. **The Interactive Lab**: Jupyter Notebooks (available via Binder) for educational and exploratory use.
