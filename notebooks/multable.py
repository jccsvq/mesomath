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
# # The Scribe's School: Multiplication Tables
#
# In the Old Babylonian period, students memorized multiplication tables of "regular" numbers. 
# In **MesoMath**, the `BabN.multable()` method reconstructs these tablets following 
# the standard scribal format.

# %%
from mesomath import BabN as bn
from mesomath.nb_utils import setup_scribal_environment

# Initialize cuneiform support
setup_scribal_environment()

# %% [markdown]
# ## 1. Standard Output
# By default, `.multable()` prints the multiplication table for the given number 
# across the standard Babylonian sequence: 1 to 20, followed by 30, 40, and 50.
# The output of `.multable()` is in `markdown` format and should be properly aligned 
# in a terminal, but not in Jupyter notebooks. The alternative method `.multable_nb` 
# is specific to notebooks.

# %%
# Standard table for 25
bn(25).multable()

# %%
# Standard table for 25
bn(25).multable_nb()

# %% [markdown]
# ## 2. Visual Customization
# The method allows you to toggle different visual aspects of the table to match 
# the style of different historical periods or publications:
#
# * `cuneiform`: Renders the table using Unicode Cuneiform.
# * `stroke`: Adds a horizontal separator between the multiplier and the result.
# * `floating`: Displays results without the leading unit (1:0:0...) where applicable.
#
# %% [markdown]
# Ancient tables weren't always standard. You can pass a custom list of multipliers 
# to the method to focus on specific values.

# %%
# A custom table for 40, only for specific values
bn(40).multable_nb(indices=[2, 5, 10, 40])

# %%
# A "cleaner" table for 1:15 (75) with strokes and cuneiform
bn("1:15").multable_nb(cuneiform=True, stroke=True)

# %% [markdown]
# ## 3. Metrological Format (`fill=True`)
# The `fill` (Pretty Alignment) parameter ensures that the sexagesimal digits 
# are correctly aligned in columns, emulating the structured layout of physical clay tablets.

# %%
# Using fill=True to see leading zeros in a table for 40
bn(40).multable_nb(fill=True)

# %% [markdown]
# > **Scribe's Tip**: When using `cuneiform=True`, the system automatically inserts the 
# > term **a-rá** (𒀀 𒁺) between the index and the product, just as an apprentice 
# > scribe would have done in the *Edubba* (tablet house).

# %%
# Let's abuse the method...
bn('11.22.00.00.44.54').multable_nb(indices=[2, 5, 10, 40],cuneiform=True,stroke=True)
