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
# # `metrotable` tutorial
#
#
#
# ## Introduction
#
# Python3 command line application based on [MesoMath](https://github.com/jccsvq/mesomath) for printing fragments of [**metrological tables**](https://cdli.earth/articles/cdlj/2009-1.pdf) in the style of those used by ancient Babylonian scribes and their apprentices.
#
# The metrological tables showed the correspondence between the additive values ​​of measurements of length, surface, weight, etc. and the abstract multiplicative sexagesimal numbers required by multiplicative arithmetic (calculations of areas, volumes, etc.). A modern analogy would be the following: we have a square with a side measuring one yard, two feet, and five inches (the additive measurement), and we want to calculate its area. We would need to convert the measurement to a homogeneous unit, for example, inches, with 65 inches. With this value, we can calculate the area of ​​the square as 65^2 = 4225 square inches. This value of 65 would be our abstract multiplicative number, and a modern metrological table would show us an entry for the association:
#
#     1 yard 2 feet 5 inches -> 65
#
# ## Running `metrotable`

# %%
# ! metrotable


# %% [markdown]
# The output: "Nothing to do, exiting!" indicates that `metrotable` is there, but you haven't told it what to do. You can try also:

# %% [markdown]
# Let us now try:

# %%
# ! metrotable -h

# %% [markdown]
# or, if you prefer long options:
#
#     $ metrotable --help
#
# to get a listing of short and long options
# ## How to use
#
# ### First steps
#
# Start by option `-r` to take a look at the metrological systems covered by this application:
#

# %%
# ! metrotable -r

# %% [markdown]
# or

# %%
# ! metrotable -ra

# %% [markdown]
# Most interestingly, here are some examples to get an idea of what the program offers:

# %%
# ! metrotable -x 1

# %% [markdown]
# or with the  `-v` or `--verbose` options to obtain a header with more information and a new column with the reciprocals of the abstract numbers if they are regular or "igi nu" ("not regular" in Sumerian) if they are not:

# %%
# ! metrotable -x 1 -v

# %% [markdown]
# and, in the same way:

# %%
# ! metrotable -x 2 -v

# %%
# ! metrotable -x 3 -v

# %%
# ! metrotable -x 4 -v

# %% [markdown]
# ### Defining a metrological table
#
# The program needs four pieces of data to calculate a segment of a metrological table:
#
# * Metrological table type (options `-t` or `--type`)
#     * L:   length measurements
#     * Lh:   length measurements (Heights)
#     * S:   surface measurements
#     * V:   volume measurements
#     * C:   capacity measurements
#     * W:   weight measurements
#     * SysS:   System S to count objects
#     * SysG:   System G to count objects
# *  Starting measurement value (options `-t` or `--min`)
# *  Final measurement value (options `-M` or `--max`)
# *  measurement increment between table rows (options `-i` or `--inc`)
#
# For example, the following will reproduce example 1 (add `-v` at will).:

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi'

# %% [markdown]
# ###  Using successive increments
#
# We can subdivide the table into different sections with different increments by entering MAX and INC as comma-separated lists. For instance, by using:
#
#     MAX = '2 kus,12 kus,5 ninda'
#     INC = '5 susi,1 kus,6 kus'
#
# in
#
#     ! metrotable -t L -m '10 susi' -M '2 kus,12 kus,5 ninda' -i '5 susi,1 kus,6 kus' -v
#
# we obtain the table from 10 susi to 2 kus with increment of 5 susi, from 2 ku to  12 kus (1 ninda) with increment by 1 kus and from this point to 5 ninda by 6 kus:

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus,12 kus,5 ninda' -i '5 susi,1 kus,6 kus' -v

# %% [markdown]
# ### Other options
#
# #### Options `-n` `--noheader`  
#
# Suppresses the printing of the table header, which can be useful if you want to join table segments by shell scripting.
#
#     $ metrotable ...  > table.txt
#     $ metrotable ... -n >> table.txt
#     $ metrotable ... -n >> table.txt
#     ...
#
# #### Options `-f` `--force`
#
# It allows the calculation of abstract numbers by forcing any unit as the base unit. For instance:

# %%
# ! metrotable -t W -m '1 mana' -M '5 mana' -i '1 mana' 

# %%
# ! metrotable -t W -m '1 mana' -M '5 mana' -i '1 mana' -f 0

# %% [markdown]
# #### Options `-w`  `--width`
#
# Changes the default of 20 chars width  of the measurement text field

# %%
# ! metrotable -t W -m '1 mana' -M '5 mana' -i '1 mana' -w 30

# %% [markdown]
# #### Options `-p` `--pedantic`
#
# Will print the coefficients of the units expressed in the system S  (system G for surfaces and volumes) making the output more closely mimic the way the measurements were actually inscribed on the clay tablets, but it complicates things for the modern reader:

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -pv

# %% [markdown]
# This may distort the output; combine it with `-w`:

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -pvw 30

# %% [markdown]
# #### Option `-F --fractions`
#
# Use the `-F0` option to have the output use the fractions `1/3, 1/2, 2/3, 5/6'`, `-F1` to also include the fraction `1/6`:

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi'

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -F0

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -F1

# %% [markdown]
# You may combine it with `-p` (pedantic mode):

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -pF0

# %%
# ! metrotable -t L -m '10 susi' -M '2 kus' -i '5 susi' -pF1

# %% [markdown]
# #### Options `-a --academic`
#
# You can combine the `-F --fractions` options with `-a --academic` to obtain listings using the academic names of the units:

# %%
# ! metrotable -x 1 -aF1 -f0 -v
