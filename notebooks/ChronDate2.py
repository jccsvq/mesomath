# ---
# jupyter:
#   jupytext:
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # **MesoTimes: Advanced Timekeeping, Ephemeris & Heliacal Scanning**

# %%
from mesomath import ChronDate as Date

# %% [markdown]
# # **1. Solar & Lunar Horizon Dynamics**
#
# ## **1.1. Geo-Astronomical Observatories (`ChronDate.sites`)**
#
# Every atmospheric and horizontal calculation in `MesoTimes` (such as twilight phases, moonrise, or heliacal events) depends strictly on local geographic parameters: **Latitude, Longitude, and Elevation**.
#
# To facilitate fluid context switching during computational sessions, `MesoTimes` embeds a static registry of ancient core observation sites and historical sanctuaries within `mesotimes.astronomy.core.mesopotamian_cities`.
#
# This data can be printed directly in the interactive REPL by invoking the static helper method `ChronDate.sites()` (aliased as `Date.sites()` or accessible from any instance):

# %%
print(Date.sites())

# %% [markdown]
# > **Observatory Scope Limits:**
# > At present, the astronomical engine pipelines are aligned to match the historical coordinates present in this native registry. Passing a string identifier not compiled within the internal `mesopotamian_cities` catalog will result in a validation error. Custom user coordinates cannot be dynamically injected without updating the underlying spatial calculation wrappers.
#
# ## **1.2. Master Almanacs & Structural Reporting**
#
# For macro-historical analysis, `ChronDate` exposes reporting engines that compile complex mathematical calculations into comprehensive, production-grade CLI dashboards.
#
# > **Terrestrial Rotation Delta T ($\Delta T$) and Mathematical Uncertainty**
# > To maintain absolute alignment with established canon research, `MesoTimes` utilizes the identical piecewise polynomial expansions and uncertainty tables compiled by **Fred Espenak and Jean Meeus** for NASA's *Five Millennium Canon of Eclipses*. At present, these parameters are native to the internal ephemeris clock loops.
#
# ### **1.2.1. The Daily Ephemeris View (`day_ephemeris`)**
#
# The `day_ephemeris()` method prints an instant diagnostic profile of the chosen date, combining civil timelines, localized solar positions, lunar table intervals, and planetary visibilities evaluated against their critical Arc of Vision (`Av`).

# %%
date = Date(1583129.58611)
print(date.day_ephemeris(city='Susa', ziggurat=50.0))

# %% [markdown]
# ### **1.2.2. The Annual Historical Almanac (`year_almanac`)**
#
# To study long-term chronological drifts, `year_almanac()` tracks the physical rotation variables of the Earth ($\Delta T$, geographic longitude shifts, and sigma error margins), maps solar equinoxes/solstices, finds planetary oppositions (*Sarsu* markers), and references verified historical eclipse records.

# %%
print(date.year_almanac(city="Babylon", ziggurat=15.5))

# %% [markdown]
# > **Local Eclipse Circumstances & External Tooling**
# > The eclipse data printed by `year_almanac()` is pulled from a historical global visibility database. `MesoTimes` **does not compute localized eclipse circumstances** (such as exact contact times $P_1/U_1$, internal path limits, or dynamic local magnitudes). For high-precision mapping of local eclipse tracks, users are encouraged to consult dedicated astronomical computing services:
# > * **NASA JavaScript Lunar Eclipse Explorer:** https://eclipse.gsfc.nasa.gov/JLEX/JLEX-AS.html
# > * **NASA JavaScript Solar Eclipse Explorer:** https://eclipse.gsfc.nasa.gov/JSEX/JSEX-AS.html
# > * **IMCCE Lunar Eclipses Forms:** https://ssp.imcce.fr/forms/lunar-eclipses
# > * **IMCCE Solar Eclipses Forms:** https://ssp.imcce.fr/forms/solar-eclipses
#
# ### **1.2.3. The Monthly Lunar Phase Almanac (`month_almanac`)**
#
# When `full=True` is provided, `month_almanac()` tracks standard syzygies and triggers a full mathematical reconstruction of a Babylonian diary month, measuring intervals in exact cuneiform *UŠ* units.

# %%
print(date.month_almanac(city="Babylon", AoV=12.0, uncertainty=0.833, full=True))

# %% [markdown]
# # **2. Planetary Engines & Heliacal Scanners**
#
# `MesoTimes` analyzes the calculation of the "wandering gods" (*bibbū*) according to the geometric orbital mechanics of the Earth's position. The engine natively calculates anomalies of time and space (maximum elongation angles) and mechanical stationarities in planetary longitude (retrogradation).
#
# ## **2.1. Inferior Planets Dispatchers (`mercury_almanac`, `venus_almanac`)**
#
# For planets closer to the Sun than Earth, the API tracks inner geometric configurations: Inferior and Superior Conjunctions, Maximum Spatial Elongations (measured in absolute degrees), and the critical turning points where the planet stalls in longitude (Station 1 and Station 2) before changing direction.

# %%
print(date.mercury_almanac())

# %%
print(date.venus_almanac())

# %% [markdown]
# ## **2.2. Superior Planets Dispatchers (`mars_almanac`, `jupiter_almanac`, `saturn_almanac`)**
#
# For outer bodies, the geometric loops omit interior conjunctions and switch to tracking clean absolute Oppositions (*Sarsu* markers) and their surrounding stationary retrogradations.

# %%
print(date.mars_almanac())

# %%
print(date.jupiter_almanac())

# %%
print(date.saturn_almanac())

# %% [markdown]
# ## **2.3. Heliacal Station Scan (`heliacal_phases`)**
#
# The most critical astronomical tool for matching historical clay diaries is the `heliacal_phases(planet, city)` scanner. It evaluates local horizon glares, atmospheric dust extinction models, and specific arcs of vision to determine the exact civil calendar day when a planet breaks out of or vanishes into the solar glare.
#
# It identifies the classical heliacal milestones:
# * **$\Gamma$ (Gamma) / $\Xi$ (Xi):** First Morning Appearance (East).
# * **$\Omega$ (Omega) / $\Sigma$ (Sigma):** Last Evening Appearance (West).
# * **$\Delta$ (Delta):** Heliacal Setting (Morning/East).
# * **$\mathrm{E}$ (Epsilon):** Heliacal Setting (Evening/West).

# %%
print(date.heliacal_phases("Mercury", city="Babylon"))

# %% [markdown]
# > **Scan Window Limits:**
# > The internal search loops of `heliacal_phases()` use a standard bounded optimization bracket of **60 days** from the reference baseline date. If a specific heliacal phenomenon falls outside this window, the CLI report logs it as `Not found in window`.
#
# # **3. Visual CLI Rendering (Terminal Charts)**
#
# To provide a rapid, intuitive diagnostic of the night sky without forcing the user to interpret raw ephemeris tables, `ChronDate` includes an interactive ASCII-art visualization engine.
#
# ## **3.1. Celestial Overview (`night_at_a_glance`)**
#
# The `night_at_a_glance(city)` method aggregates the computed horizontal visibility curves of the Sun, Moon, and all five naked-eye planets into a continuous 24-hour horizontal bar chart plotted directly onto the terminal.
#
# It maps standard universal time (UT) against computed localized solar time, rendering twilight densities and horizon transitions according to classical structural boundaries:

# %%
print(date.night_at_a_glance(city="Susa"))

# %% [markdown]
# ### **Interpreting the Chart Patterns**
#
# * **The Sky/Sun Strip:** Blocks of `#` mark full daylight hours. The transitions `::` and `.` trace the rapid progression of Civil, Navigational, and Astronomical Twilights, mapping the physical window of true observation darkness (empty spaces).
# * **The Planetary/Lunar Tracks:** A continuous line of dashes (`-`) or equality markers (`=`) indicates that the specific celestial body is physically **above the local horizon**.
# * **Historical Diagnostics:** In the chart above, one can instantly notice that while Mercury and Venus are above the horizon during twilight boundaries, they are trapped inside the intense solar glare curve (as corroborated by the `day_ephemeris()` output), whereas Jupiter and Saturn act as prominent *Evening Stars* during the first watch of the night.
#
# # **4. Babylonian Timekeeping & Elastic Day Metrics (`BabylonianDay`)**
#
# A standard civil day begins abstractly at midnight. In contrast, a historical **Babylonian Day** is fundamentally *elastic*: it begins officially at visual **Sunset** and lasts until the following sunset, shifting its raw duration and boundaries daily based on localized solar physics.
#
# The `ChronDate.bab_day_instance()` factory method unifies these two worlds, generating an isolated `BabylonianDay` instance. This class acts as a bi-directional metrological translator between continuous Julian Days (UT) and native Mesopotamian temporal frameworks.

# %%
b_day = date.bab_day_instance(city="Babylon", ziggurat=50.0)

# %% [markdown]
# ## **4.1. Day Anatomy and Horizon Boundaries (`.info`)**
#
# The `.info` property prints a structural dashboard of the active elastic day. It calculates the raw lengths of total darkness vs. daylight hours and exposes the microsecond-precise boundary limits in both Universal Time clocks and Julian Day metrics.

# %%
print(b_day.info)

# %%
print(f"String representation of active Babylonian Day: {b_day}")

# %% [markdown]
# ## **4.2. Night Vigils and Cuneiform Metrology (`get_time_units`, `get_vigil`)**
#
# `BabylonianDay` automatically divides the spatial and temporal flow of a day into traditional cuneiform increments:
# * **`UŠ` (Time Degrees):** The complete elastic day length is mapped uniformly to a $360^{\circ}$ rotational scale.
# * **`bēru` (Double-Hours):** The ultimate unit of Mesopotamian day-measurement ($1 \text{ bēru} = 30 \text{ UŠ}$), dividing the active day length into 12 proportional blocks.
# * **`maṣṣarātu` (Night Watches / Vigils):** The nocturnal phase is dynamically trisected into *barārītu* (First Vigil), *enmaššītu* (Middle Vigil), and *šadduru* (Morning Vigil).

# %%
# At the exact moment of the initial Sunset (Day Start)
print(f"Units at Sunset: {b_day.get_time_units(b_day.start_jd)}")

# %%
# Shifting deep into the night timeline
print(f"Units deep in the night: {b_day.get_time_units(b_day.start_jd + 0.15)}")

# %%
# High up into the morning daylight phase
print(f"Units in morning daylight: {b_day.get_time_units(b_day.sunrise_jd + 0.2)}")

# %% [markdown]
# ## **4.3. Automated Multi-Day Boundary Resolvers (`ut_to_ush`, `ush_to_ut`)**
#
# Because a Babylonian day starts in the afternoon of a standard modern calendar day and finishes in the afternoon of the next, mapping a standard decimal UT hour can be contextually ambiguous.
#
# Methods like `ut_to_ush()` internally build and test parallel matrix options (Option A: afternoon of yesterday vs Option B: morning of today) to match the correct historical cuneiform degree without manual user evaluation.

# %%
# Mapping an evening hour (17:30 UT belonging to the start boundary)
ush_evening = b_day.ut_to_ush(17.5)
print(f"UT 17.5 mapped to UŠ: {ush_evening:.2f}° UŠ")

# %%
# Inverting the computation back to decimal hours
print(f"Inverting back to UT decimal hours: {b_day.ush_to_ut(ush_evening)} hours")

# %% [markdown]
# ## **4.4. Chronological Offsets and Title Tracking**
#
# `BabylonianDay` instances override relational and arithmetic operators. Shifting days using addition or subtraction automatically scales the geographical and astronomical variables, while recursively parsing the underlying document `title` strings to update historical context counters.

# %%
b_day.title = "Tablet Esagila Anchor"

# Stepping forward into future horizons
future_bday = b_day + 3
print(f"Shifted Day Title: {future_bday.title}")

# %%
# Calculating relative retro-steps (Consolidating the net offsets string)
past_bday = future_bday - 5
print(f"Retro-shifted Day Title: {past_bday.title}")
