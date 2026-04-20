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
# # Plimpton 322: Basic Analysis
#
# |Plimpton 322 (Remastered by MesoMath)|||||
# |:---|:---|:---|:---|:---|
# |  𒑪𒑆 𒃵 𒌋𒐙  |  𒐕 𒑪𒑆  |  𒐖 𒑩𒑆  | 𒆠 | 𒐕  |
# |  𒑪𒐚 𒑪𒐚 𒑪𒑄 𒌋𒐘 𒑪   𒐚 𒌋𒐙  | 𒑪𒐚  𒑂  |  𒐕 𒎙  𒎙𒐙  | 𒆠 | 𒐖  |
# |  𒑪𒐙  𒑂 𒑩𒐕 𒌋𒐙 𒌍𒐗 𒑩𒐙  |  𒐕 𒌋𒐚 𒑩𒐕  |  𒐕 𒑪  𒑩𒑆  | 𒆠 | 𒐗  |
# |  𒑪𒐗 𒌋  𒎙𒑆 𒌍𒐖 𒑪𒐖 𒌋𒐚  |  𒐗 𒌍𒐕 𒑩𒑆  |  𒐙  𒑆  𒐕  | 𒆠 | 𒐘  |
# |  𒑩𒑄 𒑪𒐘  𒐕 𒑩   |  𒐕  𒐙  |  𒐕 𒌍𒑂  | 𒆠 | 𒐙  |
# |  𒑩𒑂  𒐚 𒑩𒐕 𒑩   |  𒐙 𒌋𒑆  |  𒑄  𒐕  | 𒆠 | 𒐚  |
# |  𒑩𒐗 𒌋𒐕 𒑪𒐚 𒎙𒑄 𒎙𒐚 𒑩   | 𒌍𒑄 𒌋𒐕  | 𒑪𒑆  𒐕  | 𒆠 | 𒑂  |
# |  𒑩𒐕 𒌍𒐗 𒑩𒐙 𒌋𒐘  𒐗 𒑩𒐙  | 𒌋𒐗 𒌋𒑆  | 𒎙  𒑩𒑆  | 𒆠 | 𒑄  |
# |  𒌍𒑄 𒌍𒐗 𒌍𒐚 𒌍𒐚  |  𒑄  𒐕  | 𒌋𒐖 𒑩𒑆  | 𒆠 | 𒑆  |
# |  𒌍𒐙 𒌋   𒐖 𒎙𒑄 𒎙𒑂 𒎙𒐘 𒎙𒐚  |  𒐕 𒎙𒐖 𒑩𒐕  |  𒐖 𒌋𒐚  𒐕  | 𒆠 |𒌋   |
# |  𒌍𒐗 𒑩𒐙  | 𒑩𒐙  |  𒐕 𒌋𒐙  | 𒆠 |𒌋𒐕  |
# |  𒎙𒑆 𒎙𒐕 𒑪𒐘  𒐖 𒌋𒐙  | 𒎙𒑂 𒑪𒑆  | 𒑩𒑄 𒑩𒑆  | 𒆠 |𒌋𒐖  |
# |  𒎙𒑂 𒃵  𒐗 𒑩𒐙  |  𒐖 𒑩𒐕  |  𒐘 𒑩𒑆  | 𒆠 |𒌋𒐗  |
# |  𒎙𒐙 𒑩𒑄 𒑪𒐕 𒌍𒐙  𒐚 𒑩   | 𒎙𒑆 𒌍𒐕  | 𒑪𒐗 𒑩𒑆  | 𒆠 |𒌋𒐘  |
# |  𒎙𒐗 𒌋𒐗 𒑩𒐚 𒑩   | 𒑪𒐚  |  𒑩𒐗  | 𒆠 |𒌋𒐙  |

# %% [markdown]
# ## Essential Imports and Notebook Setup

# %%
from math import (gcd, pi, acos)
from mesomath import BabN as bn
from mesomath.nb_utils import setup_scribal_environment

from IPython.display import display_markdown

setup_scribal_environment(font_size="1.6em")

KI_GLYPH = "\N{CUNEIFORM SIGN KI}"

# %% [markdown]
# ## Data
#
# Plimpton 322 data from [Wikipedia](https://en.wikipedia.org/wiki/Plimpton_322#Content)

# %%
PLIMPTON_322 = [
    ["1:59:00:15", "1:59", "2:49", "1"],
    ["1:56:56:58:14:50:06:15", "56:07", "1:20:25", "2"],
    ["1:55:07:41:15:33:45", "1:16:41", "1:50:49", "3"],
    ["1:53:10:29:32:52:16", "3:31:49", "5:09:01", "4"],
    ["1:48:54:01:40", "1:05", "1:37", "5"],
    ["1:47:06:41:40", "5:19", "8:01", "6"],
    ["1:43:11:56:28:26:40", "38:11", "59:01", "7"],
    ["1:41:33:45:14:03:45", "13:19", "20:49", "8"],
    ["1:38:33:36:36", "8:01", "12:49", "9"],
    ["1:35:10:02:28:27:24:26:40", "1:22:41", "2:16:01", "10"],
    ["1:33:45", "45", "1:15", "11"],
    ["1:29:21:54:02:15", "27:59", "48:49", "12"],
    ["1:27:00:03:45", "2:41", "4:49", "13"],
    ["1:25:48:51:35:06:40", "29:31", "53:49", "14"],
    ["1:23:13:46:40", "56", "53", "15"],
]

KI_GLYPH = "\N{CUNEIFORM SIGN KI}"

bn.fill = True

# Make a work copy of PLINTON_322
plim = PLIMPTON_322.copy()
# Apply correction to row #15
plim[14][2] = "1:46"

# %% [markdown]
# ## Plimpton 322 Content as Table

# %%
# Extrapolated "1" switch
# Use e1 = 0 to use extrapolated "1", e1 = 2 to do not use it
use_ones = False
e1 = 0 if use_ones else 2

output = "#### Plimpton 322 Content (corrected)\n||s|d|#|Row|\n|:---:|:---:|:---:|:---:|:---:|\n"

for line in plim:
    output += f"| {line[0][e1:]} | {line[1]} | {line[2]} | # |{line[3]} |\n"

display_markdown(output, raw=1)

# %% [markdown]
# ## Plimpton 322 Analysis
#
# Set `divide_by_gcd` bellow to `True`  to divide $s$ and $d$ by the their greatest common divisor before analysis.
#
# * Row: row number
# * Col. 1 (orig): Original Plimpton 322 column #1
# * Col. 1: Column 1 calculated as $(s//l)^2$, where:
# * s: shorter side
# * d: hypotenuse
# * l: longer side
# * gcd: greatest common divisor of $s$ and $d$
# * p: largest generating integer
# * q: smallest generating integer
#
# > **Archaeometric Note**: Notice how **row #11** requires division by the GCD (15) to reveal its generators $(2,1)$, while **row #15** (once the hypotenuse is corrected to $1:46$) works best without reduction to keep the long side $l$ as a regular sexagesimal number ($1:30$).

# %%
divide_by_gcd = True

output = (
    f"#### Table of Analysis Result (dividing by GCD = {divide_by_gcd})\n"+
    "|Row #|Col. 1 (orig.)|Col 1 (calculated)|$s$|$d$|$l$|$gcd$|$p$|$q$|\n|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"
         )

for line in plim:
    r = bn(line[3]).dec
    s, d = bn(line[1]), bn(line[2])
    gcdr = gcd(s.dec, d.dec)

    (s, d) = (s / gcdr, d / gcdr) if divide_by_gcd else (s, d)
    q2 = (d - s) / 2
    q = q2.sqrt()
    p = (d - q2).sqrt()
    ll = 2 * p * q
    col1 = ((d / ll) ** 2).float()
    output += f"| {r} | {line[0]} | {col1} | {s} | {d} | {ll} | {gcdr} | {p} |{q} |\n"
    # print(r, s, d, p, q)
display_markdown(output, raw=1)

# %% [markdown]
# ### Additional data
#
# Scribes did not use angles, but we do. The following information may be of interest.

# %%
divide_by_gcd = False

output = (
    f"#### Table of Analysis Result Continued (dividing by GCD = {divide_by_gcd})\n"+
    "|Row #|Angle (deg.)|$s$<br>IsReg?|$d$<br>IsReg?|$l$<br>IsReg?|\n|:---:|:---:|:---:|:---:|:---:|\n"
         )

for line in plim:
    r = bn(line[3]).dec
    s, d = bn(line[1]), bn(line[2])
    gcdr = gcd(s.dec, d.dec)

    (s, d) = (s / gcdr, d / gcdr) if divide_by_gcd else (s, d)
    q2 = (d - s) / 2
    q = q2.sqrt()
    p = (d - q2).sqrt()
    ll = 2 * p * q
    angle = 180 * acos(float(s.dec)/d.dec)/pi
    output += f"| {r} | {angle:6.6} | {s.isreg} | {d.isreg} | {ll.isreg} |\n"
    # print(r, s, d, p, q)
display_markdown(output, raw=1)

# %% [markdown]
# ## Remastering

# %%
# Extrapolated "1" switch
# Use e1 = 0 to use extrapolated "1", e1 = 2 to do not use it
use_ones = True
e1 = 0 if use_ones else 2

output = "#### Plimpton 322 (Corrected)\n||||||\n|:---|:---|:---|:---|:---|\n"
for line in plim:
    clin = [bn(_).cuneiform(stroke=1, alter=1) for _ in line]
    output += f"| {clin[0][e1:]} | {clin[1]} | {clin[2]} | {KI_GLYPH} |{clin[3]} |\n"

display_markdown(output, raw=1)
