"""
Metrological Expresion Parser
=============================

`parser/interpreter.py` This module implements the Babylonian metrological expression interpreter based on **PEG** grammars.

The interpreter must be able to accept all 75 types of **MesoMath** output
expressions so that they can be fed back as inputs.
"""

from typing import Any

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from mesomath import BabN
from mesomath.npvs import normalize

# --- GRAMMAR DEFINITIONS ---

# Main grammar used to parse complex metrological strings
# It supports standard integers, fractions, sexagesimal parenthetical notation,
# and BabN (positional sexagesimal like 2:53).
#: Main grammar used to parse complex metrological strings
MESO_GRAMMAR = r"""
    entry        = (measure space)*
    measure      = value space unit_name
    value        = (sexag plus_frac?) / (babn plus_frac?) / (integer plus_frac?) / fractional
    
    sexag        = "(" ~"[^)]+" ")"
    babn         = ~r"[0-9]+(:[0-9]+)+"
    
    plus_frac    = "+" fractional
    fractional   = ~r"[1-5]/6" / ~"1/2" / ~"1/3" / ~"2/3" / ~"5/6"
    
    integer      = ~r"[0-9]+"
    unit_name    = ~r"[a-z1-3šś\'\-]+"
    space        = ~r"\s*"
"""

# Simplified grammar used specifically for interpreting the content
# inside sexagesimal parentheses (e.g., "(1 u 7 dis)")
#: Simplified grammar used specifically for Systems S and G
SEXAG_GRAMMAR = r"""
    entry        = (measure space)*
    measure      = value space unit_name
    value        = integer / fractional
    integer      = ~r"[0-9]+"
    fractional   = ~r"[1235]/6" / ~"1/2" / ~"1/3"
    unit_name    = ~r"[a-z1-3\-]+"
    space        = ~r"\s*"
"""


class SexagInterpreter(NodeVisitor):
    """
    Interpreter for the contents of sexagesimal parenthetical expressions.
    It resolves units based on a specific sexagesimal system (e.g., BsyS, BsyG).
    """

    def __init__(self, sexsys: Any):
        """Class constructor

        :param sexsys: sexagesimal system S or G
        :type sexsys: Any
        """        
        self.grammar = Grammar(SEXAG_GRAMMAR)
        self.sexsys = sexsys

        # Get conversion factors from the provided sexagesimal system
        base_map = getattr(sexsys, "dic_cfact", {})

        # Fallback map for common units if not defined in the system
        emergency_map = {
            "dis": 1,
            "as": 1,
            "u": 10,
            #"iku": 1,
            #"ges": 60,
            #"ges2": 60,
        }

        # Merge maps: base_map (specific system) takes priority over emergency_map
        self.pos_map = {**emergency_map, **base_map}

    def visit_measure(self, node, visited_children):
        """Processes a single measurement unit and multiplies by its factor."""
        val, _, u_name = visited_children

        if u_name in self.pos_map:
            return val * self.pos_map[u_name]

        raise ValueError(f"'{u_name}' is not a valid unit name.")

    def visit_entry(self, node, visited_children):
        """Sums all processed measurements within the parentheses."""
        return sum(child[0] for child in visited_children)

    def visit_value(self, node, visited_children):
        """Converts numerical text to float."""
        return float(node.text)

    def visit_unit_name(self, node, visited_children):
        """Returns the raw unit name string."""
        return node.text

    def generic_visit(self, node, visited_children):
        """Default visitor for nodes without a specific visit method."""
        return visited_children or node.text


class MesoInterpreter(NodeVisitor):
    """
    Main interpreter for Mesopotamian metrological calculations.
    Coordinates between a metrological class (Length, Volume, etc.)
    and a sexagesimal system to resolve complex input strings.
    """

    def __init__(self, metrological_class: Any, sexagesimal_system: Any):
        """Class constructor

        :param metrological_class: The main class (Blen, Bvol, etc.) providing unit names and factors.
        :param sexagesimal_system: The sexagesimal system (BsyS and BsyG) for internal resolution.
        """
        self.grammar = Grammar(MESO_GRAMMAR)
        self.mclass = metrological_class
        self.sexsys = sexagesimal_system

    def parse(self, text: str) -> float:
        """
        Normalizes the input text and parses it against the MESO_GRAMMAR.
        Returns the total accumulated value.
        """
        clean_text = normalize(text).replace("+ ", "+")
        tree = self.grammar.parse(clean_text)
        return self.visit(tree)

    def visit_entry(self, node, visited_children) -> float:
        """Sums all individual measurements found in the string."""
        return sum(child[0] for child in visited_children)

    def visit_measure(self, node, visited_children) -> int:
        """
        Resolves the final value of a measure by checking unit priorities:
        1. Current metrological class (e.g., Blen factors).
        2. Sexagesimal system associated with the class.
        """
        val_dec, _, u_name = visited_children

        # 1st Priority: Match against the metrological class units
        if hasattr(self.mclass, "uname") and u_name in self.mclass.uname:
            idx = self.mclass.uname.index(u_name)
            return int(round(val_dec * self.mclass.cfact[idx]))

        # 2nd Priority: Match against the internal sexagesimal system units
        if hasattr(self.sexsys, "uname") and u_name in self.sexsys.uname:
            idx = self.sexsys.uname.index(u_name)
            return int(round(val_dec * self.sexsys.ufact[idx]))

        raise ValueError(f"Unknown unit: {u_name}")

    def visit_sexag(self, node, visited_children) -> float:
        """
        Handles parenthetical sexagesimal expressions by delegating
        to the SexagInterpreter.
        """
        inner = node.text[1:-1].strip()
        sub_parser = SexagInterpreter(self.sexsys)
        return sub_parser.visit(sub_parser.grammar.parse(inner))

    def visit_value(self, node, visited_children) -> float:
        """Processes numerical values, including optional fractions (e.g., 5 + 1/2)."""
        res = visited_children[0]
        main_val, opt_frac = res[0], res[1]
        total = float(main_val)
        if opt_frac:
            total += opt_frac[0]
        return total

    def visit_plus_frac(self, node, visited_children) -> float:
        """Returns the value of a fraction following a '+' sign."""
        return visited_children[1]

    def visit_fractional(self, node, visited_children) -> float:
        """Maps fraction strings to their floating-point equivalents."""
        frac_map = {"1/6": 1 / 6, "1/3": 1 / 3, "1/2": 0.5, "2/3": 2 / 3, "5/6": 5 / 6}
        return frac_map[node.text.strip()]

    def visit_integer(self, node, visited_children) -> int:
        """Converts integer text to int."""
        return int(node.text)

    def visit_babn(self, node, visited_children) -> int:
        """Resolves BabN positional notation (e.g., 2:53) to its decimal value."""
        return BabN(node.text).dec

    def visit_unit_name(self, node, visited_children) -> str:
        """Returns the raw unit name."""
        return node.text

    def generic_visit(self, node, visited_children) -> Any:
        """Default fallback for node visitors."""
        return visited_children or node.text
