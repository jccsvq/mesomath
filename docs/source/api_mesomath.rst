.. _api_mesomath:

MesoMath Ecosystem (Arithmetic and Metrology)
=============================================

This section documents the public API exposed directly from the root of the ``mesomath`` package.

Main Components
---------------

.. We document the remapped classes simulating that they originate at the root thanks to the modified __module__.

BabN (Natural Sexagesimal Numbers)
..................................
.. autoclass:: mesomath.BabN
   :members:
   :special-members: __init__
   :show-inheritance:

BabF (Sexagesimal Fractions)
............................
.. autoclass:: mesomath.BabF
   :members:
   :special-members: __init__
   :show-inheritance:

Metrology Units (NPVs)
----------------------

Blen (Length)
.............
.. autoclass:: mesomath.Blen
   :members:

Bsur (Surface Area)
...................
.. autoclass:: mesomath.Bsur
   :members:

Bvol (Volume)
.............
.. autoclass:: mesomath.Bvol
   :members:

Bcap (Capacity)
...............
.. autoclass:: mesomath.Bcap
   :members:

Bwei (Weight)
.............
.. autoclass:: mesomath.Bwei
   :members:

Bbri (Bricks)
.............
.. autoclass:: mesomath.Bbri
   :members:

BsyC (System C)
...............
.. autoclass:: mesomath.BsyC
   :members:

BsyG (System G)
...............
.. autoclass:: mesomath.BsyG
   :members:

BsyK (System K)
...............
.. autoclass:: mesomath.BsyK
   :members:

BsyS (System S)
...............
.. autoclass:: mesomath.BsyS
   :members:


Internal Support Submodules
---------------------------

npvs module
...........
.. automodule:: mesomath.npvs
   :members:
   :show-inheritance:

metrology_presets module
........................
.. automodule:: mesomath.metrology_presets
   :members:
   :show-inheritance:

nb_utils module
...............
.. automodule:: mesomath.nb_utils
   :members:
   :show-inheritance:

utils module
............
.. automodule:: mesomath.utils
   :members:
   :show-inheritance:



If you need to extend the behavior or work with low-level parsers:

Interpreter (Parser)
....................
.. automodule:: mesomath.parser.interpreter
   :members:
   :show-inheritance:

Hamming (Regular Numbers)
.........................
.. automodule:: mesomath.hamming
   :members:
   :show-inheritance:

Glyphs (Epigraphy)
..................
.. automodule:: mesomath.glyphs
   :members:
   :show-inheritance:
