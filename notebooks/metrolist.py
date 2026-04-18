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
# # System Schemas and Lists: `.metrolist()`
#
# While `.lookup()` identifies a single value, `.metrolist()` allows you to generate 
# complete conversion tables. Before generating a list, you can visualize the 
# system hierarchy using `.scheme()`.

# %%
from mesomath import Bcap as bc
from mesomath import Blen as bl
from mesomath import Bwei as bw
from mesomath.nb_utils import setup_scribal_environment

setup_scribal_environment()

# %% [markdown]
# ## 1. Visualizing the System Map: `.scheme()`
# The `.scheme()` method provides a "factor diagram" of the metrological class. 
# It shows the units and the mathematical factors that connect them.

# %%
# See the scheme for Length (Blen)
bl.scheme()

# %%
# See the scheme for Capacity (Bcap) in Cuneiform
print(*bc.scheme(cuneiform=True))

# %% [markdown]
# ## 2. Generating a Table: `.metrolist()`
# To generate a list, you need three main parameters: 
# `mmin` (start), `mmax` (end), and `step` (increment).
#
# *Example: A table of Capacity from 1 silà to 10 silà.*

# %%
bc.metrolist(mmin="1 sila3", mmax="10 sila3", step="1 sila3")

# %%
bc.metronotebook(mmin="1 sila3", mmax="10 sila3", step="1 sila3", verbose=True)

# %% [markdown]
# ## 3. Epigraphic Details: Substances and Colophons
# In administrative texts, measurements are often tied to a substance (barley, oil, etc.).
# You can use `subst` to add a glyph and `colophon=True` to get a statistical summary.

# %%
# Capacity list for Barley (she) with a colophon summary
bc.metronotebook(
    mmin="10 sila3", mmax="1 ban2 4 sila3", step="2 sila3", 
    subst="se", colophon=True, verbose =True
)

# %% [markdown]
# ## 4. Academic and Cuneiform Views
# You can toggle `actual` (academic names), `translit` (Nippur style), or `cuneiform`.
# Notice how `incipit=True` ensures the substance glyph only appears on the first line.

# %%
# A professional sequence in cuneiform with substance (wood/beams)
bl.metronotebook(
    mmin="1 ninda", mmax="5 ninda", step="1 ninda",
    cuneiform=True, subst="ges", incipit=True,
    verbose=True
)

# %% [markdown]
# ## 5. Professional Export (`.metrohtml` and `.metrolatex`)
# For those working on papers or digital editions, the sister methods 
# `.metrohtml()` and `.metrolatex()` return formatted code ready for publication.

# %%
# Generating a LaTeX table for Capacity
# (The parameters are identical to .metrolist)
latex_table = bc.metrolatex(
    mmin="1 ban2", mmax="5 ban2", step="1 ban2", 
    verbose=True
)
print("LaTeX code for publication generated.")
print(latex_table)

# %%
# Generating a LaTeX table for Capacity
# (The parameters are identical to .metrolist)
html_table = bc.metrohtml(
    mmin="1 ban2", mmax="5 ban2", step="1 ban2", 
    verbose=True
)
print("HTML code for publication generated.")
print(html_table)

# %% [markdown]
#   <table>
#   <tr>
#     <th>Measurement</th>
#     <th>Sexag. (gin)</th>
#     <th>Reciprocal</th>
#   </tr>
#   <tr style="border-top: 2px solid #5d4037;">
#     <td>1 ban</td>
#     <td>10</td>
#     <td>6</td>
#   </tr>
#   <tr>
#     <td>2 ban</td>
#     <td>20</td>
#     <td>3</td>
#   </tr>
#   <tr>
#     <td>3 ban</td>
#     <td>30</td>
#     <td>2</td>
#   </tr>
#   <tr>
#     <td>4 ban</td>
#     <td>40</td>
#     <td>1:30</td>
#   </tr>
#   <tr>
#     <td>5 ban</td>
#     <td>50</td>
#     <td>1:12</td>
#   </tr>
# </table>

# %% [markdown]
# ### 6. Segmented Lists
# You can generate complex tables with different increments by passing lists to 
# `mmax` and `step`. This mimics the structure of standard Babylonian metrological tables.

# %%
# A table that grows by 10 susi up to 2 kus, then by 1 kus up to 12 kus and by 6 kus up to 5 ninda
bl.metronotebook(
    mmin="10 susi", 
    mmax=["2 kus", "12 kus", "5 ninda"], 
    step=["5 susi", "1 kus", "6 kus"],
    translit=True,
    verbose=True,
    ubase=1,       # kus, for vertical measurements
    details=True,  # to fold output
)

# %% [markdown]
# ### 7. Using Historical Presets (Proust Series)
# MesoMath includes the standard metrological series from Nippur, as documented 
# by Christine Proust. These are accessible via the `metrology_presets` module.

# %%
from mesomath.metrology_presets import CAPACITY_PROUST_81 as C81

C81

# %%
# Generate the complete standard Nippur series for Capacity. Transliteration.
# Using the preset directly in metrolist
a,b,c = C81.select(3,5)
caption = bc.title + "<br>" + " ".join(bc.scheme(actual=True))

bc.metronotebook(a, b, c, translit=True, subst="ziz2", incipit=True, 
                 verbose=True, details=True, caption=caption, actual=True
                )

# %%
# Generate the complete standard Nippur series for Capacity. Cuneiform.
# Using the preset directly in metrolist
a,b,c = C81.select(3,5)
caption = bc.title + "<br>" + " ".join(bc.scheme(cuneiform=True))

bc.metronotebook(a, b, c, cuneiform=True, subst="ziz2", incipit=True, 
                 verbose=True, details=True, caption=caption
                )

# %% [markdown]
# ### 8. The MetrologySeries Dataclass
#
# You can create your own MetrologySeries. This is particularly useful when working with non-standard archives or specific commodities.

# %%
from mesomath.metrology_presets import MetrologySeries
# Define a series using raw integer values
my_series = MetrologySeries(
    name='Silver Logistics',
    ini=1000, 
    endlist=[1500, 2500], 
    inclist=[100, 200], 
    unit_class='Weight'
)
# Display the custom steps
my_series

# %%
# Now, let us use `my_series`
a, b, c = my_series.select(0,1)
caption = bw.title + "<br>" + " ".join(bw.scheme())

bw.metronotebook(a,b,c, verbose=True, caption=caption)

# %%
