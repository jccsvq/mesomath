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
# # Metrological classes
#
# ## Basics
#
# In the following, it is assumed that your startup script contains the lines:

# %%
# Essential imports
from mesomath.babn import BabN as bl  # Sexagesimal arithmetic
from mesomath.npvs import Blen as bl  # Length (horizontal and vertical)
from mesomath.npvs import Bsur as bs  # Surface
from mesomath.npvs import Bvol as bv  # Volume
from mesomath.npvs import Bcap as bc  # Capacity
from mesomath.npvs import Bwei as bw  # Weight
from mesomath.npvs import BsyG as bG  # Counting system G
from mesomath.npvs import BsyS as bS  # Counting system S
from mesomath.npvs import BsyC as bC  # Counting system C
from mesomath.npvs import Bbri as bb  # Brick count


# %% [markdown]
# so that we can access the classes `BabN`, `Blen`, `Bsur`,... using the shorter aliases `bn`, `bl`, `bs`, etc. If you are using `babcalc`, this has already been done for you automatically.
#
# This is what the classes `bl`, `bs`, `bv`, `bc`, `bw`, `bG`, `bS` and `ba` represent:
#
#     class  bl: Babylonian length system:
#                danna <-30- UŠ <-60- ninda <-12- kuš3 <-30- šu-si
#
#     class  bs: Babylonian surface system:
#                GAN2 <-100- sar <-60- gin2 <-180- še
#
#     class  bv: Babylonian volume system:
#                GAN2 <-100- sar <-60- gin2 <-180- še
#
#     class  bc: Babylonian capacity system:
#                gur <-5- bariga <-6- ban2 <-10- sila3 <-60- gin2 <-180- še
#
#     class  bw: Babylonian weight system:
#                gu2 <-60- ma-na <-60- gin2 <-180- še
#
#     class  bG: Babylonian counting System G:
#                šar2-gal <-6- šar'u <-10- šar2 <-6- bur'u <-10- bur3 <-3- eše3 <-6- iku
#
#     class  bS: Babylonian counting System S:
#                šar2-gal <-6- šar'u <-10- šar2 <-6- geš'u <-10- geš <-6- u <-10- diš
#
#     class  bC: Babylonian counting System C:
#                u <-10- diš
#
#     Class  bb: Babylonian brick counting system:
#                GAN2 <-100- sar <-60- gin2 <-180- še
#
# However, for ease of writing, the real or academic names of the units in these metrological systems have been simplified by removing capital letters, numbers, hyphens, and diacritics. Therefore, for inputting measurements, we will use the following unit names:
#
# Class|Metrology|Units
# -----|---------|-----
# bl| Babylonian length system|  susi, kus, ninda, us, danna
# bs| Babylonian surface system|  se, gin, sar, gan
# bv| Babylonian volume system|  se, gin, sar, gan
# bc| Babylonian capacity system|  se, gin, sila, ban, bariga, gur
# bw| Babylonian weight system|  se, gin, mana, gu
# bG| Babylonian System G|  iku, ese, bur, buru, sar, saru, sargal
# bS| Babylonian System S|  dis, u, ges, gesu, sar, saru, sargal
# bS| Babylonian System C|  dis, u
# bb| Babylonian brick counting system|  se gin sar gan
#
# >Note that scribes wrote volumes as an equivalent surface area multiplied by a standard height of 1 kus; thus, they used the same metrology for surfaces and volumes. Here, however, two different classes will be used, so that one can multiply a surface area by a length to obtain a volume, but one cannot multiply a volume by a length to obtain a four-dimensional volume, which was probably beyond the scribes' understanding.
#
# At any time, you can review the names of the units in each system and their factors through the following, e.g., for capacities:

# %%
bc.uname

# %%
bc.ufact

# %% [markdown]
# and the academic names:

 # %%
 bc.aname

# %% [markdown]
# or

# %%
print(*bc.scheme(bc))

# %%
print(*bc.scheme(bc,1))

# %% [markdown]
# >**There is no class dedicated to Babylonian height measurements**; this is by design because it is unnecessary. The only difference between horizontal and vertical length measurements lies in their metrological tables, and this is covered in the [`metrotable` tutorial](metrotable.ipynb) utility. However, if you need one, you can easily [create one](extensions.ipynb) yourself.

# %% [markdown]
# ## Entering measurements
#
# In a similar way to what we saw for sexagesimal numbers with the `bn` class. We can introduce measurements in two different ways:

# %%
a = bl(11111)
print(f"{a = }\n")

b = bl('5 ninda 25 susi')
print(f"{b = }\n")

# %% [markdown]
# In the first case, `a` is defined as a certain (integer) number of times the smallest unit ("susi" in the case of lengths). In the second case, we define the value for `b` textually. Note that we can only use integer values ​​in both cases. Both input methods are available for all classes.
#
# >In fact, there is a **third** entry method that will be seen at the end of this section.
#
# Once you have defined measurements, you can "explain" them:

# %%
a.explain()


# %%
b.explain()

# %% [markdown]
#
# This will give us information about the nature of the measurement and the properties of the measurement system being used.
#
# Note that the value given as "Sexagesimal floating value of the above:" is generated by the `.sex()` method; however, this method accepts a numeric parameter to indicate the unit relative to which this sexagesimal floating value is calculated. This parameter defaults to zero, indicating the first unit in the list provided by `.explain()`: `Unit names: ['susi', 'kus', 'ninda', 'us', 'danna']`

# %%
a.sex()   # susi as the base unit

# %%
a.sex(0)  # the same as .sex()

# %%
a.sex(1)  # kus as the base unit

# %%
a.sex(2)  # ninda as the base unit

# %%
a.sex(3)  # us as the base unit

# %%
a.sex(4)  # danna as the base unit

# %% [markdown]
# This will be useful if you intend to recreate **Metrological lists**. For example, the following code
# will print an excerpt of the metrological table for length using ninda (x.sex(2)) as base unit:

# %%
ls =[]
for i in range(1,10):
    ls.append(str(i)+' susi')
for i in '10 15 20 25'.split():
    ls.append(i+' susi')
ls.append('1 kus')
for i in '10 15 20 25'.split():
    ls.append('1 kus '+i+' susi')
ls.append('2 kus')
for i in ls:
    x=bl(i)
    print(f'{str(x).ljust(15)} -> {str(x.sex(2)).rjust(6)}')

# %% [markdown]
# (See page 8 of [Floating calculation in Mesopotamia](https://hal.science/hal-01515645v2/document) by Christine Proust).
#
# But you will rarely need to resort to this since you have specialized tools available:
#
# * The [`metrotable`](metrotable.ipynb) tool, which specializes in printing segments of metrological tables.
# * The [`mtlookup.py`](mtlookup.ipynb) tool, which simulates direct and inverse searches in metrological tables.
# * The `.metrolist()` method that we will see bellow.

# %% [markdown]
# Since version v1.1.0 you can get the metrological value of an object directly using the `.metval()` method:

# %%
bl('1 kus 15 susi').metval()

# %% [markdown]
# ## Operations
#
# For objects of the same class, the following operations are available:
#
# * Addition
# * Subtraction (returns the absolute value of the difference)
# * Multiplication by a number
# * Division by a number
# * Logical operations
#
# Let's look at some examples:

# %%
a >= b

# %%
a + b

# %%
a - b

# %%
b - a                   # a-b == b-a !!!

# %%
a - b == b - a

# %%
2 * a

# %%
b * 2

# %%
b * 2.5

# %%
a / 2

# %%
(a + 2 * b) / 5

# %%
(a + 2 * b) / 5.3

# %% [markdown]
# Additionally, for length measurements we can multiply them together to obtain surfaces and volumes, and for surfaces we can multiply them by lengths to obtain volumes:

# %%
s = a * b
print(f"{a = }, {b = }\n")
print(f"s = {a * b = }\n")


# %%
s.explain()

# %%
c = bl('2 kus')
print(f"{c = }\n")

v = s * c
print(f"v = {s * c = }\n")


 # %%
 v.explain()

# %%
v2 = a * b * c
print(f"v2 = {a * b * c = }\n")
v2 == v
print(f"{v2 == v = }\n")


# %% [markdown]
# ## Systems S and G
#
# In cases like this:

# %%
a = bv('128 gan')
print(f"{a = }\n")

# %% [markdown]
# we might prefer to see the coefficients of the units expressed in the **S system** ( or **G system** for surfaces and volumes), to do this:

# %%
bv.prtsex=True
print(f"{a = }\n")


# %% [markdown]
# This changes the default for objects of the `bv` class and makes the output more closely mimic the way the measurements were actually inscribed on the clay tablets, but it complicates things for the modern reader:

# %%
a = bv('128 gan 133 se')
print(f"{a = }\n")


# %% [markdown]
# If you want this to be the default for all metrological classes, use:
#
#     from mesomath.npvs import MesoM
#     MesoM.prtsex = True
#
# The third input method cited above makes use of these types of strings; in fact, the parentheses have been introduced to make them easier to parse as input:

# %%
b = bv('460800 gan 44 sar 20 gin')
b

# %%
c = bv('(7 sargal 6 sar 4 buru) gan (4 u 4 dis) sar (2 u) gin')
c

# %%
bv.prtsex = False
c

# %%
bl.prtsex = True
b = bl(333333)
b

# %%
c = bl('(1 u 5 dis) us (2 u 5 dis) ninda (1 u 1 dis) kus (3 dis) susi')
c
bl.prtsex = False  

# %% [markdown]
#
# ## Fractions
#
# There is also basic support for entering *principal fractions*: `1/6, 1/3, 1/2, 2/3, 5/6` (and only for them), they can be entered in several ways:

# %%
a=bl('0+1/3 ninda')
a

# %%
a=bl('+1/3 ninda')
a

# %%
a=bl('1/3 ninda')
a

# %%
a=bl('2 + 1/3 ninda')
a

# %%
a=bl('2 1/3 ninda')
a

# %%
a=bl('21/3 ninda')
a

# %% [markdown]
# For output using `1/3, 1/2, 2/3, 5/6` fractions, you can use the `.prtf()` method:

# %%
a=bl(11223344)
a

# %%
a.prtf()

# %% [markdown]
# If you activate `prtsex` you get:

# %%
bl.prtsex=True
a.prtf()

# %%
a.prtf(1)

# %% [markdown]
# These results can be used for input:

# %%
bl.prtsex=0
b=bl('(1 u 7 dis) 1/6 danna (4 dis) 1/2 us (5 dis) 5/6 ninda (1 dis) 1/3 kus (4 dis) susi')
b

# %%
b.prtf()

# %%
b.prtf(1)

# %%
b.dec

# %%
c=bl(a.prtf(1))
c.dec

# %% [markdown]
# ## Academic names
#
# Since v1.1.0, the .prtf() method has a second switch that allows the academic unit names to be used in the output:

# %%
a=bl(11223344)
a.prtf()

# %%
a.prtf(1)

# %%
a.prtf(1,1)

# %%
bl.prtsex=True
a.prtf(0,1)

# %%
a.prtf(1,1)

# %% [markdown]
# This kind of string can also be used as input:

# %%
b=bl('(1 u 7 dis) 1/6 danna (4 dis) 1/2 UŠ (5 dis) 5/6 ninda (1 dis) 1/3 kuš3 (4 dis) šu-si')
b.dec

# %% [markdown]
# equivalent to:

# %%
b=bl(a.prtf(1,1))
b.dec


# %% [markdown]
# ## Volume vs. Capacity
#
# There were two systems for measuring volume: **capacities**, used to measure grain, beer, and other types of food and goods, and **volume** proper, used to measure everything else. Here, they are represented by the metrological classes `Bcap` (imported here as `bc`) and `Bvol` (`bv`), respectively. Since they are two systems for measuring the same physical quantity, we can convert quantities from one system to the other with the methods `.cap()` and `.vol()`:

# %%
a = bv('1 gin')
a.explain()

# %%
b = a.cap()
b.explain()

# %%
(b.vol()).explain()

# %% [markdown]
# ## Bricks
#
# Volume measurements were frequently transformed into their "brick" equivalents. These were measured in "*sar-b*" (units or packages of 720 bricks), and each brick type was characterized by its "*Nalbanum*," or the number of *sar-b* of that type that fits in 1 *sar* of volume. The `.sarb()` method allows us to perform this transformation:

# %%
a = bv('1 sar')
a

# %%
b = a.bricks()
b

# %%
b.explain()

# %% [markdown]
# This is for  *nalbanum* =1.0  type-12 bricks, for type-2 bricks with decimal *nalbanum* = 7.20:

# %%
b = a.bricks(7.20)
b

# %%
b.SI()


# %% [markdown]
# If you have 10000 type-2 bricks, you can do:

# %%
c = bb(15 * 10000)
c

# %%
c.SI()

# %% [markdown]
# `c` is a Bbri object:

# %%
c.explain()


# %% [markdown]
# that you can convert into a volume:

# %%
d = c.vol(7.20)
d.explain()


# %% [markdown]
# Here is an excerpt from a table I found:
# [here](https://personal.us.es/cmaza/mesopotamia/edificios.htm#Tipos%20de%20ladrillos) (Spanish only, sorry):
#
# |Brick type|Nalb. (dec.) |Nalb. (sex.)|
# |------|---------|-----|
# |  1   |    9.00 |9|
# |  1a  |     8.33| 8:20|
# |  2   |     7.20 |7:12|
# |3 |  5.40 | 5:24|
# |4 |   5.00 |5|
# |5 |  4.80 |4:48|
# |7 |   3.33 |3:20|
# |8 |  2.70 |2:42|
# |9 |  2.25 |2:15|
# |10|  1.875 |1:52:30|
# |11|  1.20| 1:12|
# |12|1.00 |1  |

# %%
