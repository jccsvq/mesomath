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
# # Example of use of `BabN` class
#
# Taken from [Duncan J. Melville: Reciprocals and Reciprocal algorithms in Mesopotamian Mathematics (2005)](https://www.researchgate.net/publication/237309438_RECIPROCALS_AND_RECIPROCAL_ALGORITHMS_IN_MESOPOTAMIAN_MATHEMATICS)
#
# * Example 1: from Table 2. Simple Reciprocal algorithm
# * Example 2: from Table 3. using "The Technique"
#
# ## Example 1: Searching the reciprocal of 2:5  according to D. J. Melville (2005)
#
# from Table 2. Simple Reciprocal algorithm
#

# %%
from mesomath.babn import BabN


d1 = BabN("2:5")
r1 = d1.tail()
r2 = r1.rec()
r3 = d1 * r2
r4 = r3.rec()
r5 = r4 * r2

print(f"{d1 = }")
print(f"{r1 = }")
print(f"{r2 = }")
print(f"{r3 = }")
print(f"{r4 = }")
print(f"{r5 = }\n")

print(f"Result: {r5 = }\n")

# %%
print(f"\nTesting: {d1 * r5 = }")


# %% [markdown]
# ## Example 2: from Table 3. using *The Technique*

# %%
r1 = d1.tail()
r2 = r1.rec()
r3 = d1.head() * r2
r4 = r3 + BabN(1)
r5 = r4.rec()
r6 = r5 * r2

print(f"{d1 = }")
print(f"{r1 = }")
print(f"{r2 = }")
print(f"{r3 = }")
print(f"{r4 = }")
print(f"{r5 = }")
print(f"{r6 = }")


print(f"\nResult: {r6 = }")

# %%
print(f"\nTesting: {d1 * r6 = }")

# %%
