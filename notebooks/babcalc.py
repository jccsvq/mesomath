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
# # `babcalc` Sandbox
# This is an interactive environment for quick calculations. All MesoMath classes are pre-loaded with shorthand aliases.

# %%
import platform
import mesomath.__about__
from mesomath.nb_utils import setup_scribal_environment

# Import Arithmetic
from mesomath import BabN as bn

# Import Metrology with shorthand aliases
from mesomath import (
    Blen as bl, Bsur as bs, Bvol as bv, 
    Bcap as bc, Bwei as bw, Bbri as bb,
    BsyG as bG, BsyS as bS, BsyC as bC, BsyK as bK
)

# Import Historical Presets
from mesomath.metrology_presets import (
    CAPACITY_PROUST_81 as clist,
    WEIGHT_PROUST_82 as wlist,
    SURFACE_PROUST_83 as slist,
    LENGTH_PROUST_84 as llist
)

# Initialize Scribal Environment (Cuneiform support)
setup_scribal_environment()

print(f"MesoMath babcalc v{mesomath.__about__.__version__} [Python {platform.python_version()}]")
print("Ready for calculation. Use aliases: bn, bl, bs, bv, bc, bw, etc.")

# %% [markdown]
# ### Quick Reference & Examples:
#
# | Category | Alias | Example |
# | :--- | :--- | :--- |
# | **Arithmetic** | `bn` | `bn('20') * bn('3')` |
# | **Length** | `bl` | `bl('1:30 ninda')` |
# | **Surface** | `bs` | `bs('1 gan2')` |
# | **Capacity** | `bc` | `bc('1 gur')` |
#
# **Try your first calculation in the cell below:**

# %%
# Start calculating here! (e.g., area = bl('10 ninda') * bl('5 ninda'))
