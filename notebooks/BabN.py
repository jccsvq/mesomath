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
# # BabN testing
#
# ## Entering sexagesimal numbers
#
# ### Decimal input
#
# First of all, we import the `BabN` class under the name `bn` to shorten keyboard input

# %%
from mesomath.babn import BabN as bn



# %% [markdown]
# There are four ways to enter sexagesimal numbers, we start with the simplest: by their decimal equivalent

# %%
a = bn(405)

a   # type `a <return>` to display it


# %% [markdown]
# Let us see some of its properties

# %%
print(f"{a = }\n")           ## The number
print(f"{str(a) = }\n")      ## The string version of the number
print(f"{a.len() = }\n")     ## Number of sexagesimal digits
print(f"{len(a) = }\n")      ## Number of sexagesimal digits
print(f"{a.dec = }\n")       ## decimal quivalent
print(f"{int(a) = }\n")      ## decimal quivalent
print(f"{a.list = }\n")      ## list of sexagesimal digits
print(f"{a.factors = }\n")   ## tuple (i, j, k, l); number is (2^i * 3^j * 5^k * l)
print(f"{a.isreg = }\n")     ## is number regular?

a.explain()                  ## Print a short report about the number


# %% [markdown]
# Let us introduce a second number

# %%
b = bn(11111)

print(f"{b = }\n")           ## The number
print(f"{str(b) = }\n")      ## The string version of the number
print(f"{b.len() = }\n")     ## Number of sexagesimal digits
print(f"{len(b) = }\n")      ## Number of sexagesimal digits
print(f"{b.dec = }\n")       ## decimal quivalent
print(f"{int(b) = }\n")      ## decimal quivalent
print(f"{b.list = }\n")      ## list of sexagesimal digits
print(f"{b.factors = }\n")   ## tuplle (i, j, k, l); number is (2^i * 3^j * 5^k * l)
print(f"{b.isreg = }\n")     ## number is regular?

b.explain()                  ## Print a short report about the number


# %% [markdown]
# ### Sexagesimal input
#
# Sexagesimal numbers are entered as strings, using   `:`,  `;`, `.`, `,`,`-` and blank space (` `) as input separators:

# %%
c = bn('3:5:11:6:40')

c.explain()


# %%
d = bn("19.26.24")

d.explain()


# %%
strange_input = bn('1:2;3,4.5 6-7')
strange_input

# %% [markdown]
# ### Tuple input
#
# Any natural number n can be writen as `n = 2^i × 3^j × 5^k × l` where  `i, j, k, l  ≥ 0`, `i, j, k` are the powers of `2, 3` and `5`, and `l` is a "remainder" that should not be divisible by `2, 3` or `5`. The tuple  `(i,j,k,l)` is what `a.factors` returned above. This is interesting because we can generate regular numbers simply by adopting `l = 1`, entering the number as a tuple

# %%
e = bn((10, 17, 5, 1))

print(f"{e = }\n")
e.explain()


# %% [markdown]
# This number is regular and a multiple of `60`, its *floating* version is obtained using the `f()` or `float()` methods

# %%
print(f"{e.f() = }\n")
print(f"{e.float() = }\n")

(e.f()).explain()

# %% [markdown]
# use the widgets bellow to experiment generating regular numbers

# %%
from ipywidgets import interactive

def demo_ijk(i=1, j=1, k=1):
    n = bn((i, j, k, 1))
    print(f"{              n = }")
    print(f"{          n.dec = }")
    print(f"{          n.f() = }")
    print(f"{    (n.f()).dec = }")
    print(f"{        n.rec() = }")
    print(f"{  (n.rec().dec) = }")
    print(f"{    (n*n.rec()) = }")
    print(f"{(n*n.rec()).dec = }")
    print(f"{((n*n.rec()).f()) = }")

w = interactive(
    demo_ijk,
    i=(0, 20),
    j=(0, 20),
    k=(0, 20),
)
w

# %% [markdown]
#
#
# but if `l > 1` the number is not regular

# %%
f = bn((7, 23, 0, 9_999_991))

print(f"{f = }\n")
f.explain()


# %% [markdown]
# ### List input
#
# Finally, one last way to enter sexagesimal numbers is by using the list of their sexagesimal digits.

# %%
e = bn([2, 27, 37, 21, 0, 0, 0, 0, 0])

print(f"{e = }\n")
e.explain()


# %% [markdown]
# ## Basic arithmetic
#
# ### Addition
#
# Use the addition operator `+` to perform addition

# %%
a = bn('16.24.35')
b = bn('1.33.54.22')

print(f"{a = }, {b = }\n")
print(f"{a + b = }\n")
print(f"{b + a = }\n")


# %% [markdown]
# There's no need to use variables, we can do it directly
#

# %%
bn(45689) + bn(325874)


# %%
bn('34.18.52') + bn('1.11.14.16')

# %% [markdown]
# Integers may be added directly

# %%
bn('33.14.22') + 34



# %%
5523 + bn('33.14.22')


# %% [markdown]
# Of course, we are not limited to two addends

# %%
a + b + bn('33.14.22') + 34

# %% [markdown]
# ### Subtraction
#
# Use the subtraction operator `-`
#
# Subtraction, like addition, always gives absolute (not floating) results. It also returns the absolute difference of numbers. This is by design, because Mesopotamian mathematics lacked negative numbers and to save us from mistakes. Thus, subtraction in this application is a commutative operation.

# %%
print(f"{bn(45689) - bn(325874) = }\n")
print(f"{bn(325874) - bn(45689) = }\n")


# %% [markdown]
# ### Multiplication
#
# Use the multiplication operator `*`. Multiplication is absolute by default:

# %%
a = bn('34:59:31:12')
b = bn('14:3:45')

print(f"{a = }, {b = }\n")
print(f"{a * b = }\n")
print(f"{(a * b).f() = }\n")


# %% [markdown]
# but we can change this default

# %%
bn.floatmult = True       ## This changes the default!
print(f"{a * b = }\n")


# %% [markdown]
# and restore it again

# %%
bn.floatmult = False       ## This changes the default!
print(f"{a * b = }\n")


# %% [markdown]
#
# ### Powers
#
# Use the power operator `**`:

# %%
print(f"{a = }\n")
print(f"{a ** 2 = }\n")
print(f"{a ** 3 = }\n")

# %% [markdown]
# ### Division
#
# Class `BabN` has two types of division defined, __both are floating__:
#
# *  **`a/b`** **Approximate floating** division of two arbitrary numbers. This is the translation of our ***modern division*** into the world of Babylonian floating numbers, although we have no evidence that they knew it.
# *  **`a//b`** This is the **Babylonian division**, that is, the product of `a` by the reciprocal of `b`, which implies that `b` has to be a **regular** number.
#
# Let us try:

# %%
a = bn('14.15.16')
b = bn('12.2')
q = a / b

print(f"{a = }, {b = }\n")
print(f"a / b = {q = }\n")

# %% [markdown]
# Now, as a check

# %%
print(f"{b * q = }\n")


# %% [markdown]
# a value that, in the world of floating numbers, is very similar to `a`.
#
# How do we relate the previous results to decimal division?

# %%
print(f"{a.dec = }, {b.dec = }\n")
print(f"{a.dec / b.dec = }\n")


# %% [markdown]
# as we are in world of Babylonian floating numbers, we have to divide `q` by some power `n` of `60`

# %%
for n in range(1,7):
    print(f"q.dec / (60 ** {n}) = {q.dec / (60 ** n)}")


# %% [markdown]
# the above result shows us than `n = 5` in this case.
#
# We can change the number of digits in the result (approximately, sorry) by changing the class atribute `BabN.rdigits`:

# %%
print(f"defaulf {bn.rdigits = }\n")
old_rdigits = bn.rdigits             ## backup of default `BabN.rdigits`
bn.rdigits = 10                      ## This changes the default!
print(f"{a / b = }\n")
bn.rdigits = old_rdigits             ## restores the default 


# %% [markdown]
# Let us try the Babylonian division:

# %%
print(f"{a = }, {b = }\n")
print(f"{a // b = }\n")


# %% [markdown]
# well, `b` is not regular. Let us use another value

# %%
b = bn(405)

print(f"{a = }, {b = }, {b.isreg = }, reciprocal of b is: {b.rec() = }\n")
print(f"{a // b = }\n")


# %% [markdown]
# this result is exactly:

# %%
print(f"{a * b.rec() = }\n")


# %% [markdown]
# ### Roots
#
# #### Square root
#
# Use the `sqrt()` method:

# %%
print(f"Square root of 2: {bn(2).sqrt() = }\n")
print(f"testing...: { (bn(2).sqrt()) ** 2 = }\n")


# %% [markdown]
# we can round the above result to `6` sexagesimal digits

# %%
print(f"rounded to 6 digits: {((bn(2).sqrt()) ** 2).round(6) = }\n")
print(f"and 'floating' it: {(((bn(2).sqrt()) ** 2).round(6)).f() = }\n")


# %% [markdown]
# We see that effectively `1:24:51:10:7:46` is an approximation of the square root of `2`. To relate this sexagesimal floating value to the square root of two in the decimal system, let's calculate:

# %%
print(f"{(bn(2).sqrt()).dec/60.**5 = }")


# %% [markdown]
# which is similar to

# %%
from math import sqrt
print(f"{sqrt(2) = }\n")


# %% [markdown]
# Compare the following result:

# %%
print(f"{(30*bn(2).sqrt()).float()}\n")

# %% [markdown]
# to the one appearing in tablet [YBC 7289](https://en.wikipedia.org/wiki/YBC_7289)
#
# <a target = "_blank" title="Urcia, A., Yale Peabody Museum of Natural History,  http://peabody.yale.edu, http://hdl.handle.net/10079/8931zqj
# derivative work, user:Theodor Langhorne Franklin, CC0, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:YBC-7289-OBV-labeled.jpg"><img width="256" alt="Labeled photograph of YBC 7289 identifying inscribed numbers" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/YBC-7289-OBV-labeled.jpg/256px-YBC-7289-OBV-labeled.jpg?20190204183004"></a>

# %% [markdown]
# #### Cube root
#
# Method `.cbrt()` returns the floating cube root of the numbers.

# %%
print(f"Cube root of 2: {bn(2).cbrt() = }\n")
print(f"testing...: { (bn(2).cbrt()) ** 3 = }\n")


# %% [markdown]
# etc...
#
# ## Complex expressions
#
# The Python engine is behind the scenes, which means we can combine elementary operations to build complex expressions:

# %%
a = bn('16.22')
b = bn('44.16')
c = bn('6.45')
d = ((a+b)*(a-b))//c**2
ll=[a,b,c,d]

print(f"{a = }, {b = }, {c = }\n")
print(f"{((a+b)*(a-b))//c**2 = }\n")
print(f"{ll = }\n")
print(f"{min(ll) = }\n")
print(f"{max(ll) = }\n")
print(f"{bn('44.16') in ll = }\n")


# %% [markdown]
# etc...
#
# ## Logical operators
#
# Logical operators are available and can be combined with integers. This can be useful in programming.

# %%
print(f"{a <= b and c.isreg = }\n")
print(f"{a < 300 = }\n")


# %% [markdown]
# ## Other BabN class  attribute
#
# `bn.fill` (in fact, `BabN.fill`) is set to `False` by default. You can change it to modify the aspect of the printed sexagesimal numbers by adding a left 0 to digits from 0 to 9 i.e. to convert them to 00, 01, ..., 09. This can be useful for alignment in tables:

# %%
z = bn('1.2.0.14.5.4.3')
print(f"{z = }\n")

bn.fill = True
print(f"With BabN.fill = True: {z = }\n")
bn.fill = False
print(f"With BabN.fill = False: {z = }\n")


# %% [markdown]
# ## Other BabN class methods
#
#
# ### `.rec()`
#
# This method returns the reciprocal of regular numbers, `None` for non-regular numbers (we have already seen it):

# %%
a=bn(400)
print(f"{a = }\n")

a.rec()
print(f"{a.rec() = }\n")
print(f"{type(a.rec()) = }\n")
print(f"{a * a.rec() = }\n")


b=bn(406)
print(f"{b = }\n")
print(f"{b.rec() = }\n")
print(f"{type(b.rec()) = }\n")


# %% [markdown]
# ### `.inv(n)`
#
# This is a replacement for .rec() for irregular numbers. Irregular numbers can be said to have infinite-digit reciprocals; this method calculates the first `n` of them.
#

# %%
b=bn(406)
print(f"{b = }, {b.isreg = }\n")
print(f"{b.inv() = }\n")
print(f"{b * b.inv() = }\n")

print(f"{b.inv(10) = }\n")
print(f"{b * b.inv(10) = }\n")


# %% [markdown]
# ### `.round(n)`
#
# Returns the first `n` sexagesimal digits of the number with rounding:

# %%
c = bn('8:52:1:10:56:9:27:29:15:44')
print(f"{c = }\n")
print(f"{c.round(4) = }\n")


# %% [markdown]
# Useful when working with approximate floating numbers. Alternatively, you can use the standard function `round`

# %%
round(c,4)


# %% [markdown]
# ### `.head(n)`
#
# Returns the first `n` sexagesimal digits of the number without rounding, without argument returns the first digit only:

# %%
print(f"{c = }\n")
print(f"{c.head() = }\n")
print(f"{c.head(3) = }\n")
print(f"{c.head(7) = }\n")


# %% [markdown]
# ### `.tail(n)`
#
# Returns the last `n` sexagesimal digits of the number, without argument returns the last digit only:

# %%
print(f"{c = }\n")
print(f"{c.tail() = }\n")
print(f"{c.tail(2) = }\n")
print(f"{c.tail(6) = }\n")


# %% [markdown]
# ### `.searchreg(minn, maxn, limdigits=6, prt=False)`
#
# Searches the `BabN.database` database for the closest regular number to the object's.
# `minn` and `maxn`: must be sexagesimal strings using ":" separator. `limdigits` max value is 20.

# %%
help(c.searchreg)

# %%
print(f"{c = }\n")
print(f"{c.searchreg('01', '59') = }\n")
print(f"{c.searchreg('01', '59', 19) = }\n")

bn(7).searchreg('06:40', '07:40', 4, True)

# %%
