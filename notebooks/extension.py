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
# # Extending **MesoMath**
#
# ## The "Vertical Problem": Defining Height
#
# In many Mesopotamian mathematical problems, vertical measurements (height or depth) are treated with 
# specific units that, while sharing the same names as lengths, behave differently in calculations.
#
# Let's define a custom class `bh` (Babylonian Height) that inherits from the length system 
# (`bl` or `Blen`) but fixes the base unit to the *kuš3* (cubit).

# %%
from mesomath.npvs import Blen, Bsur, Bvol, Bcap
from mesomath.nb_utils import setup_scribal_environment

# Initialize cuneiform support
setup_scribal_environment()


# %%
# We define our custom height class
class bh(Blen):
    title: str = "Babylonian Height Measurement"
    ubase: int = 1  # Fixed to 'kus' (cubit)


# %% [markdown]
# ## Seamless Interaction
#
# Thanks to the polymorphic design of **MesoMath**, your custom classes are recognized by the core engine. 
#     You can multiply a standard surface (`Bsur`) by your new height (`bh`) to obtain a volume (`Bvol`) 
# without any type errors.

# %%
# 1. Define a surface of 1 sar
area = Bsur('1 sar')

# 2. Define a height using our custom class
height = bh('1 kus')

# 3. Calculate volume (Area * Height)
# The system recognizes 'bh' as a valid length for this operation.
volume = area * height

print(f"Volume: {volume}") 
# Output: 1 sar

# %% [markdown]
# ## Automatic Utilities
#
# By inheriting from `MesoM` (via `Blen`), your new class automatically gains all the new administrative and diagnostic tools of this version:
#
# 1. **Metrological Lists/Tables**: Generate tables for your custom units instantly.
#    

# %%
bh.metrolist('1 kus', '5 kus', '1 kus', verbose=True, ubase=None)

# %%
bh.metrolist('10 susi', '2 kus', '5 susi', verbose=True, width=30,fractions=2,actual=True)

# %%
           
bh.prtsex = 1
bh.metrolist('10 susi', '2 kus', '5 susi', verbose=True, width=30,fractions=2,actual=True)

# %% [markdown]
# The following are the options for the `.metrolist()` method:

# %%
help(bh.metrolist)


# %% [markdown]
# ## Late Babylonian Period Metrology
#
#
# **MesoMath** is designed to work with the metrology of the Old Babylonian period, but it can be extended to use the metrology of other periods. For example, for the Late Babylonian Period, we can start by defining a class `LBcap` for the capacities:

# %%
class LBcap(Bcap):  # Capacity
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period capacity units:

        **gur <-5- bariga <-6- ban2 <-10- sila3 <-10- GAR**

    """

    title: str = "Late Babylonian capacity measurement"
    uname: list[str] = "gar sila ban bariga gur".split()
    aname: list[str] = "GAR sila3 ban2 bariga gur".split()
    ufact: list[int] = [10, 10, 6, 5]
    cfact: list[int] = [1, 10, 100, 600, 3000]
    siv: float = 0.1
    siu: str = "litres"
    ubase: int = 3  # bariga

    def vol(self) -> object:
        """Convert capacity to volume measurement

        :return: volume measurement
        :rtype: "Bvol"
        """
        return LBvol(int(round(self.dec/(100/6))))

class LBvol(Bvol):  # Volume
    """This class implement Non-Place-Value System arithmetic
    for Late Babylonian Period volume units:

        **GAN2 <-100- sar <-60- gin2 <-180- še**

    """
    title: str = "Late Babylonian volume measurement"
    
    def cap(self) -> object:
        """Convert volume to capacity measurement"""
        return LBcap(int(round(self.dec*(100/6))))


# %% [markdown]
# and then:

# %%
a = LBcap('1000 sila')
b = a.vol()
print(f"{b =}")

# %%
b.explain() 

# %%
c = b.cap() 
print(f"{c =}")

# %%
c.SI() 

# %%
c.explain() 

# %%
LBcap.metrolist('1 bariga','3 bariga', '1 ban',1)

# %% [markdown]
# etc. but we should also redefine the rest of the classes to ensure consistency in the operations with the new units.
