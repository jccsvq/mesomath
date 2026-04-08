"""
MesoMath Metrological Data Module: Proust's Tables
--------------------------------------------------
This module contains the numerical and metrological grapheme maps used for 
authentic cuneiform transliteration. These datasets are derived from the 
research and systematic tabulations provided by Christine Proust.

Source Reference:
    Proust, C. (2009). "Numerical and Metrological Graphemes: From Cuneiform 
    to Transliteration". Cuneiform Digital Library Journal, 2009(1).
    URL: https://cdli.ucla.edu/pubs/cdlj/2009/cdlj2009_001.html
    Alternative: https://www.academia.edu/867780/

Usage in MesoMath:
    These dictionaries provide the 'greedy' mapping for the _transliterate() 
    engine, ensuring that decimal values are decomposed into historically 
    accurate graphemes rather than pure sexagesimal notation.

License/Attribution:
    Data compiled and adapted for MesoMath v2.0.0rc0. 
    Users of this data should cite the original author as per the CDLJ 
    Open Access guidelines.
"""
from . import capacities, weights, surfaces, lengths

# Mapping of class names to their data dictionaries
# This allows MesoM.transliterate() to be generic
MAPS = {
    "Bcap": capacities.DATA,
    "Bwei": weights.DATA,
    "Bsur": surfaces.DATA,
    "Blen": lengths.DATA,
}

def get_map_for(obj_type: str):
    """Returns the DATA dictionary corresponding to the object type."""
    return MAPS.get(obj_type, {})
