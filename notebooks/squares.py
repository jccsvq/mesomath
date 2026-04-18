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

# %%
from mesomath.nb_utils import setup_scribal_environment

setup_scribal_environment(font_size="1.6em")

# %%
"""Write a markdown table of the area of squares as a function of their edge.
"""
# Required imports
from mesomath import Blen as bl
from mesomath.utils import gen_multi_range as gmr
from mesomath.metrology_presets import LENGTH_PROUST_84 as llist
from  IPython.display import display_markdown

# Selecting range from Proust's presets
a,b,c = llist.select(4,6)

# Table header
output = "| Side | Surface |\n|:---|---:|\n"
# Table body
for _ in gmr(bl,a,b,c):
    ll = bl(_[0])
    ll2 = ll * ll
    
    output += f"| {ll.cuneiform:<20} | {ll2.cuneiform:<37} |\n"
# Table to notebook
display_markdown(output, raw=1)
