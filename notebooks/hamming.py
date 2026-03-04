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
# # `hamming` module test

# %%
from mesomath.hamming import hamming, genCSV
from mesomath.babn import BabN as bn

print(hamming(1, 63))


# %%
print(hamming(1691)[0])

# %%
big_regular = hamming(1000000)[0]
print(big_regular)

# %%
bn(big_regular).float()

# %%
genCSV(63)
