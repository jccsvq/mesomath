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
# # `bmultable` tutorial

# %%
# ! metrotable

# %% [markdown]
# The above output indicates that `bmultable` is there, but you haven't told it what to do. You can try also:
#
#
# ## Options

# %%
# ! bmultable -h


# %% [markdown]
# ## List of tables learned by the scribes
#
# The list comprised only regular numbers and their reciprocals as multipliers... plus the number 7! You can obtain a listing of the tables by issuing:

# %%
# ! bmultable 0


# %% [markdown]
# ## Example
#
# The following prints the multiplication table for sexagesimal number `1:12`. Options `-p --principal` limit multiplicand to the list of *principal numbers*. Without this option the table includes al multiplicands between 1 and 59.

# %%
# ! bmultable 1:12 -p

# %% [markdown]
# With the `-f --fill` option, the sexagesimal digits are padded with zeros if necessary:

# %%
# ! bmultable 1:12 -pf

# %% [markdown]
# Finally, you can also change the sexagesimal digit separator with the `-s --separator` option:

# %%
# ! bmultable 1:12 -pfs .

# %%
