"""Customized IPython REPL for MesoMath"""

import sys

from traitlets.config.loader import Config

from mesomath.wisdom import get_silver_payment


def start_ibabcalc():
    """
    ibabcalc interactive REPL
    """
    try:
        import IPython

        from mesomath import BabN as bn  # noqa: F401
        from mesomath import BabF as bf  # noqa: F401
        from mesomath import Bbri as bb  # noqa: F401
        from mesomath import Bcap as bc  # noqa: F401
        from mesomath import Blen as bl  # noqa: F401
        from mesomath import Bsur as bs  # noqa: F401
        from mesomath import BsyC as bC  # noqa: F401
        from mesomath import BsyG as bG  # noqa: F401
        from mesomath import BsyK as bK  # noqa: F401
        from mesomath import BsyS as bS  # noqa: F401
        from mesomath import Bvol as bv  # noqa: F401
        from mesomath import Bwei as bw  # noqa: F401
        from mesomath.__about__ import __version__ as VERSION
        from mesomath.metrology_presets import CAPACITY_PROUST_81 as clist
        from mesomath.metrology_presets import LENGTH_PROUST_84 as llist
        from mesomath.metrology_presets import SURFACE_PROUST_83 as slist
        from mesomath.metrology_presets import WEIGHT_PROUST_82 as wlist
        from mesotimes import ChronDate as Date
        from mesotimes import BabStar as Star


        # Welcome message
        message = f"\n--- MesoMath Scribal Research Lab {VERSION} ---\n\n"
        message += f"""Powered by: IPython {IPython.__version__} | Python {sys.version.split()[0]}
Interactive environment loaded: Jupyter/IPython integration enabled.
Metrological presets (clist, wlist, etc.) ready for analysis
>> Scribal entry: {get_silver_payment()}
--------------------------------------------------------------------
        """

        # Here we define what we want the user to already have loaded
        namespace = {
            "bn": bn,
            "bf": bf,
            "bl": bl,
            "bs": bs,
            "bv": bv,
            "bc": bc,
            "bw": bw,
            "bG": bG,
            "bS": bS,
            "bC": bC,
            "bK": bK,
            "bb": bb,
            "clist": clist,
            "wlist": wlist,
            "slist": slist,
            "llist": llist,
            "VERSION": VERSION,
            "Date": Date,
            "Star": Star,
            "exit": exit,
            "quit": quit,
            "message": message,
        }

        config = Config()
        config.TerminalIPythonApp.display_banner = False
        config.InteractiveShellApp.exec_lines = [
            "print(message)",
            "del(message)",
        ]
        IPython.start_ipython(argv=[], user_ns=namespace, config=config)

    except ImportError:
        print(
            "Error: IPython is not installed. Please install mesomath with [notebook] extra."
        )


def main():
    """
    Entry point
    """
    start_ibabcalc()


if __name__ == "__main__":
    start_ibabcalc()
