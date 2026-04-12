# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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
# # The Metrological Detective: `.lookup()`
#
# One of the most complex tasks in cuneiform studies is identifying what a "floating" 
# sexagesimal number (like `20` or `1:30`) represents in a specific context. 
#
# The `.lookup()` method performs a reverse search across all units of a metrological 
# class, testing the value at different orders of magnitude.

# %%
from mesomath import Bcap as bc
from mesomath import Blen as bl
from mesomath.nb_utils import setup_scribal_environment

setup_scribal_environment()

# %% [markdown]
# ## 1. Basic Search
# By default, `.lookup()` shows all units that can be represented by the given 
# abstract value. 
#
# *Example: What does the value '20' represent in the Capacity system?*

# %%
bc.lookup(20)

# %% [markdown]
# ## 2. Academic and Historical Transliteration
# For researchers, the notation is key. You can toggle `academic` notation (using `;` 
# for sexagesimal fractions) and `translit` to see the Nippur-style names of the units.

# %%
# High-precision lookup with academic transliteration
bc.lookup("20", academic=True, translit=True)

# %% [markdown]
# ## 3. Epigraphic Mode (Cuneiform)
# You can see the matches in Unicode Cuneiform. This is extremely useful for 
# direct comparison with a physical tablet or a photo.

# %%
# Looking for '1:30' in Length with cuneiform rendering
bl.lookup("1:30", cuneiform=True)

# %% [markdown]
# ## 4. Professional Analysis (`verbose` and `strict`)
# * `verbose=True`: Adds the modern SI equivalents (meters, liters, etc.).
# * `strict=True`: Only shows matches where the sexagesimal representation 
#    is an exact match, ignoring partial approximations.

# %%
# Deep analysis of the value '40' in Length
bl.lookup(40, strict=True, verbose=True)

# %% [markdown]
# ## 5. Advanced Layout Control
# You can adjust the output table using `width` for the names column and 
# `fractions` to control the precision of the results.
#
# > **Note**: `.lookup()` is a class method. You call it directly from 
# > the class (e.g., `Bcap.lookup()`) without needing to create an object.
