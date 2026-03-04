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
# # `mtlookup` tutorial
#
# ## Introduction
#
# Python3 command line application based on [MesoMath](https://github.com/jccsvq/mesomath) to search for the abstract number that corresponds to a measure or to list measures that correspond to a given abstract number (option: `-r`).
#
# ## Running `mtlookup`

# %%
# ! mtlookup

# %% [markdown]
# The above output indicates that `mtlookup` is there, but you haven't told it what to do. 
#
# ### Options:
#
# #### Options `-h, --help`
#
# list the program options:

# %%
# ! mtlookup -h


# %% [markdown]
# ### Metrologies
#
# Metrology is selected with the options `-t` or `--type`:
#
# * L:   length meassurements
# * Lh:   length meassurements (Heights)
# * S:   surface meassurements
# * V:   volume meassurements
# * C:   capacity meassurements
# * W:   weight meassurements
# * B:   brick count
# * SysS:   System S to count objects
# * SysG:   System G to count objects
#
# ### Direct search
#
# Returns the abstract value corresponding to a measurement in a given metrology. For instance:

# %%
# ! mtlookup -t L '1 us 30 ninda' 


# %% [markdown]
# You can use the verbose options `-v` or `--verbose`:

# %%
# ! mtlookup -t L '1 us 30 ninda' --verbose

# %% [markdown]
# ### Reverse search
#
# With the `-r` or `--reverse` options you get a list of measures that match the given abstract number:

# %%
# ! mtlookup -t L 1.30 -r 

# %%
# ! mtlookup -t L 1.30 -rv

# %% [markdown]
# In some cases, due to the discrete nature of the measurements and rounding, the last rows of the list only show approximate values:

# %%
# ! mtlookup -r -t L 6.40.38 

# %% [markdown]
# you can use options `-s --strict` to suppress them:

# %%
# ! mtlookup -r -t L 6.40.38 -w 30

# %% [markdown]
# ###  Pedantic mode
#
# Options `-p` `--pedantic` will print the coefficients of the units expressed in the system S  (system G for surfaces and volumes) making the output more closely mimic the way the measurements were actually inscribed on the clay tablets, but it complicates things for the modern reader:

# %%
# ! mtlookup -t V '128 gan 133 se' -p


# %%
# ! mtlookup -t V 3:33:20:0:44:20 -pr -w 55

# %% [markdown]
# ### Fractions
#
# Use the `-F0` option to have the output use the fractions `1/3, 1/2, 2/3, 5/6'`, `-F1` to also include the fraction `1/6`:

# %%
# ! mtlookup -t L 1.30 -r -F0

# %% [markdown]
# You may combine it with `-p` (pedantic mode):

# %%
# ! mtlookup -t L 1.30 -r -pF1 -w 30

# %% [markdown]
# ### Academic unit names
#
# You can combine the `-F --fractions` options with `-a --academic` to obtain listings using the academic names of the units:

# %%
# ! mtlookup -t L '1 us 30 ninda' -aF1

# %%
# ! mtlookup -t L 1.30 -r -pF1 -aw 30

# %%
