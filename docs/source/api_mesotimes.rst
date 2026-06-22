.. _api_mesotimes:

MesoTimes Ecosystem (Chronology and Astronomy)
==============================================

Integrated astronomical module as an alpha preview for time management and horizons.

The Facade of Times
-------------------

Date (ChronDate)
................
.. autoclass:: mesomath.ChronDate
   :members:
   :special-members: __init__
   :undoc-members:

Calendars
---------

.. automodule:: mesotimes.calendars
   :members:
   :undoc-members:

.. automodule:: mesotimes.proleptic
   :members:
   :undoc-members:

.. automodule:: mesotimes.almanac
   :members:
   :undoc-members:

.. automodule:: mesotimes.babday
   :members:
   :undoc-members:


Planetary and Heliacal Calculations
-----------------------------------

.. automodule:: mesotimes.astronomy.planets.finder
   :members:
   :undoc-members:

Models of Celestial Bodies
--------------------------

Core
....

.. automodule:: mesotimes.astronomy.core
   :members:

Sun
...

.. automodule:: mesotimes.astronomy.sun
   :members:

Moon
....

.. automodule:: mesotimes.astronomy.moon
   :members:

Planets
.......

.. automodule:: mesotimes.astronomy.planets.base
   :members:
   :show-inheritance:

.. automodule:: mesotimes.astronomy.planets.inferiors
   :members:
   :show-inheritance:

.. automodule:: mesotimes.astronomy.planets.superiors
   :members:
   :show-inheritance:

Stars (BabStar)
...............

.. autoclass:: mesotimes.BabStar
   :members:
   :special-members: __init__
   :undoc-members:

.. automodule:: mesotimes.astronomy.visibility
   :members: