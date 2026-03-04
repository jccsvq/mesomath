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
# # Economic Calculations
#
# The following three methods can help us study the economic problems commonly addressed by scribes. They offer a shortcut, saving us from having to work with metrological tables and reciprocal numbers.
#
# Let us start by importing classes:

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
from mesomath.npvs import Bbri as bb  # Brick count


# %% [markdown]
# ## `.labor_cost()`
#
# This method calculates the cost of a project in terms of man-days to be paid or the number of workers needed to complete the project in one day, based on the work to be carried out and the work quota that each worker is expected to complete per day.
#

# %%
canal = bv('10 sar')
quota = '20 gin'  # 1/3 sar per day
wages = canal.labor_cost(quota)
print(f"{wages} men required to finish in a day.")

# %%
help(bv.labor_cost)

# %% [markdown]
# ## `.rations()`
#
# This method calculates the cost of a project in rations of barley, beer, oil, etc. based on the work to be carried out and the work quota that each worker is expected to complete per day.
# for {meth}`.rations()<.rations>` method.

# %%
daily_ration = '2 sila'
total_grain = canal.rations(work_man='20 gin', wage=daily_ration)
print(f"Total barley: {total_grain}")

# %%
help(bv.rations)

# %% [markdown]
# ## `.silver_payments()`
#
# This method calculates the cost of a project in monetary terms (silver weight) based on the work to be carried out and the work quota that each worker is expected to complete per day.
# ver_payments()<.silver_payments>` method.

# %%
bricks = bb('2 sar')
silver_wage = '8 se'
total_silver = bricks.silver_payments(work_man='1 sar', wage=silver_wage)
print(f"Total silver payment: {total_silver}")


# %%
help(bv.silver_payments)
