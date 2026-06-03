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
# # `ChronDate`: Core Operations & Timeline Arithmetic

# %%
from mesomath import ChronDate as Date

# %% [markdown]
# ## **1. Instantiation (The Four Pathways)**
#
# A `ChronDate` instance can be constructed using four distinct chronological pathways, depending on the format of your source data:
#
# ### **Path 1: Julian Day Number (Absolute UT)**
#
# Instantiates a date directly from a standard floating-point Julian Day (JD) number. This is the core native format of the engine.

# %%
date = Date(1748872.5)
print(f"Direct JD instantiation: {date}")

# %% [markdown]
# ### **Path 2: Julian Calendar Date**
#
# Constructs an instance from a historical Julian year, month, and day. It automatically handles proleptic or standard configurations depending on the period.

# %%
date = Date.from_julian(-378, 5, 17)  # Instantiation from Julian Calendar (-378-05-17)
print(f"Julian calendar instantiation: {date}")

# %% [markdown]
# ### **Path 3: Gregorian Calendar Date**
#
# Constructs an instance using the modern Gregorian calendar rules, fully supporting proleptic extensions for deep historical retro-calculations.

# %%
date = Date.from_gregorian(2026, 5, 28)
print(f"Gregorian calendar instantiation: {date}")

# %% [markdown]
# ### **Path 4: Babylonian King Date (Historical Chronology)**
#
# The most advanced entry point. It resolves a canonical Babylonian date into an absolute astronomical point by querying the internal Parker-Dubberstein database. It requires the king code, the regnal year, the historical lunar month, and the tablet day.

# %%
# Query available historical king codes
print(Date.kings())

# %% [markdown]
# > *Note: The `Start Date (J)` in the table above corresponds to King's regnal year 1, month 1, day 1.*

# %%
# Year 26 of Artaxerxes II, Month 2 (Aiaru), Day 14
date = Date.from_babylonian(king_code="k012", year=26, month=2, day=14)
print(f"Babylonian historical instantiation: {date}")

# %% [markdown]
# ## **2. Core Operations & Timeline Arithmetic**
#
# Once instantiated, a `ChronDate` object operates as an immutable point on the timeline. Internally, all operations are calculated using absolute precision floating-point Julian Days (UT). However, the class exposes a fluid API to extract representations across modern and ancient calendars, query dynastic contexts, and perform timeline arithmetic.
#
# In the standard interactive terminal (`babcalc`), the class is available under the clean alias `Date`. Let us instantiate two anchors to explore these operations: an ancient tablet date from the Seleucid Era and a modern contemporary date.

# %%
date = Date.from_babylonian("k019", 45, 5, 19)
today = Date.from_gregorian(2026, 5, 29)

print(f"Ancient Anchor: {date}")
print(f"Modern Anchor:  {today}")

# %% [markdown]
# ### **2.1. Calendar Conversions & Introspection**
#
# `ChronDate` objects decouple the internal astronomical time placement from its civil expressions. Five core properties allow the inspection of any timeline node:
#
# * **`__call__()`:** Invoking the instance directly (`date()`) returns its raw, continuous Julian Day number as a standard Python `float`.
# * **`.julian`:** Returns a 7-element tuple representing `(year, month, day, hour, minute, second, microsecond)` in the Julian Calendar. It operates as a proleptic calendar for dates preceding its historical implementation.
# * **`.gregorian`:** Returns a 7-element tuple in the standard modern Gregorian Calendar (proleptic for deep historical retro-calculations).
# * **`.babylonian`:** Resolves the exact local Mesopotamian calendar parameters (Regnal Year, Lunar Month, and Tablet Day).
# * **`.context`:** Queries the internal historical database to extract political, dynastic, or co-regency details matching the active date.

# %%
print(f"Raw Julian Day float:        {date()}")
print(f"Julian Calendar tuple:       {date.julian}")
print(f"Proleptic Gregorian tuple:   {date.gregorian}")
print(f"Babylonian Calendar string:  {date.babylonian}")
print(f"Historical Dynastic Context: {date.context}")

# %% [markdown]
# ### **2.2. The Proleptic Babylonian Calendar**
#
# When calculating dates outside the strict limits of surviving historical records (such as modern dates), `MesoTimes` projects a **Proleptic Babylonian Calendar**.

# %%
print(f"Modern Julian representation:   {today.julian}")
print(f"Modern Gregorian representation: {today.gregorian}")
print(f"Proleptic Babylonian computation: {today.babylonian}")
print(f"Proleptic Context fallback:     {today.context}")

# %% [markdown]
# > **Mathematical Grounding of the Proleptic Engine**
# > The proleptic Babylonian calendar is structurally mapped using the year-and-month distribution schema of the **Metonic Cycle** (the 19-year intercalation cycle stabilized during the late Babylonian/Seleucid era).
# >
# > However, a strict mathematical Metonic mapping introduces a systematic drift of approximately **two hours per cycle**. To prevent this chronological desynchronization, `MesoTimes` does not rely on a rigid cycle; instead, it delegates the start and duration of every proleptic month to the **true astronomical neomenia calculated at Babylon's local visual horizon**. This hybrid approach guarantees that the projected calendar remains perfectly in phase with actual lunar physics over thousands of years.
#
# ### **2.3. Timeline Arithmetic and Ordering**
#
# `ChronDate` instances support standard arithmetic operators and total ordering comparisons. Because instances are immutable, shifting a date returns a completely new `ChronDate` node.
#
# * **Interval Derivation (`date1 - date2`):** Subtracting one instance from another yields a `float` representing the absolute distance between both nodes in elapsed days.
# * **Timeline Shifting (`date + int` / `date - int`):** Adding or subtracting loose integers steps the timeline forward or backward by that exact number of days.
# * **Relational Operators:** Relational checks (`>`, `<`, `>=`, `<=`, `==`, `!=`) evaluate chronological positioning by comparing the absolute underlying Julian Day values.

# %%
print(f"Days elapsed between anchors: {today - date} days")
print(f"Shifting timeline (+17 days): {(date + 17).babylonian}")
print(f"Chronological ordering check (today > date): {today > date}")

# %% [markdown]
# ### **2.4. Hashing and Collection Persistence**
#
# `ChronDate` implements secure hashing (`__hash__`). This enables instances to be safely stored within standard Python hashed collections, such as sets or as keys in dictionaries, preventing mutable side effects when managing large sets of archaeological text dates.

# %%
day_set = {date, (date + 17), today}
print("Iterating over a hashed set of ChronDate objects:")
for historical_date in day_set:
    print(f" -> {historical_date.babylonian}")

# %% [markdown]
# ### **2.5. Macro-Calendrical Matrix Dispatchers (`bab_year_calendar`)**
#
# To visualize the overarching lunisolar grid of any given historical or theoretical boundary, `ChronDate` exposes the `bab_year_calendar()` method. This engine acts as a dynamic dispatcher that decides, based on localized archaeological and algorithmic dataset availability, whether to render a strict empirical record or a cyclical astronomical projection.
#
# The structural grid outputs a terminal report tracking the localized nomenclature of months (*Nisānu* through *Addaru*), their calculated mathematical duration (29 to 30 days based on lunar horizon visibility), and their alignment with historical Julian dates.
#
# #### **Case A: The Regnal Era Matrix (Historical Empirical)**
#
# When initialized inside well-documented historical intervals, the header dynamically updates to display the formal regnal years of the localized rulers or global overarching eras:

# %%
date = Date.from_julian(74, 10, 15)
print(date.bab_year_calendar())

# %% [markdown]
# #### **Case B: The Imperial Era Matrix (Historical Seleucid)**
#
# As the historical timeline advances, the underlying engine automatically switches its anchoring references to trace long-form continuous reporting frameworks such as the Seleucid accounting loops:

# %%
date = Date.from_julian(75, 10, 15)
print(date.bab_year_calendar())

# %% [markdown]
# > **Chronological Boundary Artifact**
# > The year 386 of the Seleucid Era (75/76 CE) marks the absolute terminal boundary of the empirical data compiled in Parker & Dubberstein (1971). Because the underlying database lacks any subsequent historical records beyond JDE 1748871.5, the engine cannot fetch the start date of the following year's *Nisānu*. 
# >
# > Consequently, the 12th month (*Addaru*) is omitted from the tabular grid, and both the reported **Year ends on** boundary and the **Total year duration** (325 days) are historically incomplete and mathematically truncated.
#
# #### **Case C: The Proleptic Fallback Grid**
#
# If a target date falls into a structural chronological gap where the empirical cuneiform database (`kingdates`) does not contain verified data points, the method downgrades gracefully. It switches to a proleptic calculation model to simulate astronomical ideal cycles based on the neomenia as contemplated from a given `city` or custom horizon coordinates (falling back to Babylon by default, see the [next notebook](ChronDate2.ipynb) for a list of Observatories):

# %%
date = Date.from_julian(76, 10, 15)
print(date.bab_year_calendar(city="Babylon", ziggurat=0.0))

# %% [markdown]
# > **Intercalary Recognition (`Addaru II` / `Ululu II`)**
# > The historical grid reports empirical leap intercalations manually declared by the administration of the *Esagila* temple or royal decrees, while the proleptic framework applies mathematical cycle distributions. Intercalary months are explicitly tracked and logged in the terminal matrix output with a suffix (e.g., `Addaru II`).
