"""This module contains some metrological data"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class MetrologySeries:
    """
    Dataclass to hold the initial and final points and increments needed to generate 
    the metrological list/table segments in the style of Nippur with the help of 
    the .metrolist() and associated methods.
    """
    name: str
    unit_class: str  # "Bcap", "Bsur", etc.
    ini: str
    endlist: List[str]
    inclist: List[str]
    subst: str = ""

    def __post_init__(self):
        object.__setattr__(self, "nframes", len(self.endlist)) # Number of steps

    def __repr__(self) -> str:
        """
        Displays a formatted table of the metrological series steps.
        """
        header = f"MetrologySeries: {self.name} ({self.unit_class})\n"
        header += "-" * 65 + "\n"
        header += f"{'Step':<6} | {'Start Value':<15} | {'End Value':<15} | {'Increment':<15}\n"
        header += "-" * 65 + "\n"

        rows = []
        current_start = self.ini
        for i in range(self.nframes):
            rows.append(
                f"{i:<6} | {current_start:<15} | {self.endlist[i]:<15} | {self.inclist[i]:<15}"
            )
            current_start = self.endlist[
                i
            ]  # The end of one step is the start of the next

        return header + "\n".join(rows) + "\n" + "-" * 65

    def select(
        self, start_step: int, end_step: int
    ) -> Tuple[str, List[str], List[str]]:
        """
        Returns a slice of the series to feed .metrolist().

        :param start_step: The index of the first step (inclusive).
        :param end_step: The index of the last step (inclusive).
        :return: A tuple (initial_value, sliced_endlist, sliced_inclist)
        """
        if start_step < 0 or end_step >= self.nframes or start_step > end_step:
            raise IndexError(
                f"Selection range {start_step}-{end_step} is out of bounds for nframes={self.nframes}"
            )

        # If we start at step 0, the initial value is the series 'ini'.
        # If we start later, the initial value is the 'endlist' of the PREVIOUS step.
        new_ini = self.ini if start_step == 0 else self.endlist[start_step - 1]

        new_endlist = self.endlist[start_step : end_step + 1]
        new_inclist = self.inclist[start_step : end_step + 1]

        return (new_ini, new_endlist, new_inclist)


# For the generation of metrological lists
# Capacities
bc_ini = "1 gin"
bc_endlist = [
    "3 gin",
    "20 gin",
    "2 sila",
    "2 ban",
    "1 bariga",
    "1 gur",
    "2 gur",
    "20 gur",
    "120 gur",
    "1200 gur",
    "7200 gur",
    "72000 gur",
    "216000 gur",
]
bc_inclist = [
    "30 se",
    "1 gin",
    "10 gin",
    "1 sila",
    "5 sila",
    "1 ban",
    "1 bariga",
    "1 gur",
    "10 gur",
    "60 gur",
    "600 gur",
    "3600 gur",
    "36000 gur",
]

# Weigths
bw_ini = "1 se"

bw_endlist = [
    "30 se",
    "40 se",
    "45 se",
    "50 se",
    "60 se",
    "90 se",
    "100 se",
    "105 se",
    "115 se",
    "120 se",
    "130 se",
    "135 se",
    "145 se",
    "150 se",
    "160 se",
    "165 se",
    "175 se",
    "1 gin",
    "2 gin",
    "20 gin",
    "2 mana",
    "30 mana",
    "2 gu",
    "20 gu",
    "120 gu",
    "600 gu",
    "3600 gu",
    "36000 gu",
    "216000 gu",
]

bw_inclist = [
    "1 se",
    "10 se",
    "5 se",
    "5 se",
    "10 se",
    "30 se",
    "10 se",
    "5 se",
    "10 se",
    "5 se",
    "10 se",
    "5 se",
    "10 se",
    "5 se",
    "10 se",
    "5 se",
    "10 se",
    "5 se",
    "30 se",
    "1 gin",
    "10 gin",
    "1 mana",
    "10 mana",
    "1 gu",
    "10 gu",
    "60 gu",
    "600 gu",
    "3600 gu",
    "36000 gu",
]

# Surfaces
bs_ini = "20 gin"

bs_endlist = [
    "2 sar",
    "20 sar",
    "1 gan",
    "6 gan",
    "18 gan",
    "36 gan",
    "360 gan",
    "2160 gan",
    "21600 gan",
    "64800 gan",
]

bs_inclist = [
    "10 gin",
    "1 sar",
    "10 sar",
    "50 sar",
    "1 gan",
    "6 gan",
    "18 gan",
    "180 gan",
    "1080 gan",
    "10800 gan",
]

# Lengths
bl_ini = "1 susi"

bl_endlist = [
    "1 kus",
    "2 kus",
    "1 ninda",
    "10 ninda",
    "40 ninda",
    "1 us",
    "2 us",
    "1 danna",
    "2 danna",
    "20 danna",
    "30 danna",
    "50 danna",
    "60 danna",
]

bl_inclist = [
    "1 susi",
    "5 susi",
    "1 kus",
    "6 kus",
    "10 ninda",
    "5 ninda",
    "10 ninda",
    "1 us",
    "5 us",
    "15 us",
    "1 danna",
    "5 danna",
    "10 danna",
]

#: Capacity metrology series
CAPACITY_PROUST_81 = MetrologySeries(
    name="Proust 8.1 Capacities",
    ini=bc_ini,
    endlist=bc_endlist,
    inclist=bc_inclist,
    unit_class="se",
)
#: Weight metrology series
WEIGHT_PROUST_82 = MetrologySeries(
    name="Proust 8.2 Weights",
    ini=bw_ini,
    endlist=bw_endlist,
    inclist=bw_inclist,
    unit_class="ku_babbar",
)
#: Surface metrology series
SURFACE_PROUST_83 = MetrologySeries(
    name="Proust 8.3 Surfaces",
    ini=bs_ini,
    endlist=bs_endlist,
    inclist=bs_inclist,
    unit_class="a-sa",
)
#: Length metrology series
LENGTH_PROUST_84 = MetrologySeries(
    name="Proust 8.4 Lengths",
    ini=bl_ini,
    endlist=bl_endlist,
    inclist=bl_inclist,
    unit_class="",
)
