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
# # **Sexagesimal Fractions (`BabF` class)**
#
# The `BabF` class provides a robust implementation for the sexagesimal representation of non-negative rational fractions and their basic arithmetic operations. To preserve absolute mathematical precision throughout cuneiform data analysis, `BabF` performs exact fraction arithmetic internally, avoiding the floating-point rounding errors inherent to the IEEE 754 standard.
#
# ## **1. Instantiation and Representation Methods**
#
# A `BabF` object can be instantiated using three distinct semantic patterns depending on the nature of the historical source material.
#
# ### **Pattern 1: Explicit Numerator and Denominator**
#
# The most basic constructor accepts two arguments: `BabF(p, q)`. Both the numerator (`p`) and the denominator (`q`) can be loose integers, decimal strings, positional sexagesimal strings, or native `BabN` objects.

# %%
from mesomath import BabF as bf, BabN as bn

# %%
f = bf(74, 28)
g = bf(5, 8)

print(f"{f =}, {g =}")

# %%
p = bn('32:54')
q = bn('43:18')
f2 = bf(p, q)

print(f"{f2 =}")

# %% [markdown]
# Alternatively, structured strings containing a forward slash (`/`) are parsed automatically into their respective components:

# %%
f3 = bf('32:54 / 43:18')

print(f"{f3 =}")
print(f"{f2 == f3 =}")

# %% [markdown]
# ### **Pattern 2: Positional Sexagesimal Expansion**
#
# Fractions can be defined via a single positional string using the character `@` as the "sexagesimal radix point" (defined by the class constant `BabF.SEP`). In this mode, the denominator is dynamically computed as an exact power of sixty ($60^n$), where $n$ represents the number of fractional sexagesimal places.
#
# This pattern is highly effective for importing historical astronomical parameters, such as the mean synodic months compiled by ancient and medieval scholars:

# %%
synodic = {
    "Banu_Musa": bf('29@31:50:5:43:23'),
    "Brahmagupta": bf('29@31:50:5:43:24'),    
    "al_Hashimi": bf('29@31:50:5:43:33'),        
    "Ibn_al_Muthanna": bf('29@31:50:5:44:33'),        
    "Alfonsine_Tables": bf('29@31:50:7:37:27:8:25'),   
    "Bonjorn": bf('29@31:50:7:53:39:49'),     
    "Levi_ben_Gerson": bf('29@31:50:7:54:25:3:32'),   
    "al_Hajjaj": bf('29@31:50:8:9:20'),
    "al_Biruni": bf('29@31:50:8:9:20:13'),      
    "Ibn_Yunus": bf('29@31:50:8:9:24'),         
    "Ptolemy": bf('29@31:50:8:48'),      
    "Geminus": bf('29@31:50:18'),         
    }

# %% [markdown]
# *(Values taken from B. Goldstein's: *Ancient and Medieval Values for the Mean Synodic Month* - Journal for the History of Astronomy, 34, 65 - 74)*
#
# Iterating through these objects highlights how `BabF` maintains the exact fractional structure while offering decimal evaluation capabilities:

# %%
for author, period in synodic.items():
    print(f"{author:>16} -> {period.__str__():37} ({period.as_float})")

# %% [markdown]
# ### **Pattern 3: Repeating Sexagesimal Digits**
#
# The class method `BabF.repeated()` allows the instantiation of purely repeating fractional digits. This corresponds to the mathematical expression $\frac{p}{60^n - 1}$, mapping periodic sexagesimal expansions into exact rational fractions:

# %%
h = bf.repeated('8:34:17')

print(f"{h =}")

# %%
print(f"{h.expand(9) =}")

# %%
print(f"{h.simplified =}")

# %% [markdown]
# *Note: In the example above, the repeating sequence `8:34:17` resolves exactly to $\frac{1}{7}$, providing an elegant tool to handle non-regular sexagesimal denominators.*
#
# More complex, mixed repeating fractions can be built by combining standard instances with scaled periodic parts:

# %%
h2 = bf('2@37') + bf.repeated('8:34:17') / 60
print(f"{h2.expand(10) =}")

# %%
print(f"{h2 =}")

# %%
print(f"{h2.simplified =}")

# %% [markdown]
# ## **2. Introspection and Internal Properties**
#
# Each `BabF` instance exposes specialized properties to query its internal state, convert to decimal formats, or obtain numerical variations:

# %%
f = bf(74, 28)
print(f"{f.p =}, {f.q =}")         # Returns the numerator and denominator as BabN objects

# %%
print(f"{f.as_dec_fraction =}")    # Returns a string formatted as standard decimal integers

# %%
print(f"{f.as_float =}")           # Computes the lossy floating-point representation

# %%
print(f"{f.simplified =}")         # Returns a new BabF object reduced to lowest terms

# %%
print(f"{f.rec =}")                # Returns the exact reciprocal fraction (inverse)

# %% [markdown]
# To visualize the precise fractional representation back into a manageable cuneiform string, the `.expand(max_digits)` method divides the internal parameters up to the specified limit of sexagesimal digits:

# %%
print(f"{f.expand(8) =}")          # Forces expansion to 8 fractional places

# %% [markdown]
# ## **3. Arithmetic and Relational Operations**
#
# `BabF` implements total ordering and full operator overloading. Operations are evaluated using cross-multiplication formulas to ensure absolute mathematical fidelity. Mixed operations between `BabF`, `int`, and `BabN` are fully supported out of the box.

# %%
g = bf(5, 8)
print(f"Relational comparison (g < f): {g < f}")

# %%
print(f"Subtraction (f - g): {f - g}")

# %%
print(f"Exponentiation (f**2): {f**2}")

# %%
print(f"Division quotient (f / g): {f / g}")

# %%
print(f"Reduced division quotient: {(f / g).simplified}")

# %% [markdown]
# > **Safety Guardrails:** To protect the integrity of historical metrological and astronomical calculations, `MesoMath` strictly forbids direct operations between `BabF` and Python `float` types. Attempting mixed floating-point arithmetic will trigger an explicit `TypeError`. Users must explicitly declare a conversion using the `BabF` constructor patterns or fallback to the `.as_float` property.
#
# ## **4. Cuneiform Convergence (Interoperability with `BabN`)**
#
# Since historical cuneiform notation lacked an explicit radix point or separator to isolate the fractional part, advanced tablet reproduction can be achieved by feeding the result of a `BabF.expand()` directly back into a `BabN` positional instance after replacing the `@` sign with `:`. This is automatically handled by the `.to_cunei()` method.
#
# This layout replicates the precise, seamless visual reading flow of ancient Mesopotamian mathematical texts:

# %%
# Initialize cuneiform rendering and notebook visual structures
from mesomath.nb_utils import setup_scribal_environment

# Uncomment the following line to see the cuneiform 
# (this will break the alignment of other cells):
#
# setup_scribal_environment()

# %%
h2 = bf('2@37') + bf.repeated('8:34:17') / 60
print(f"Cuneiform output representation:\n{h2.to_cunei()}")
