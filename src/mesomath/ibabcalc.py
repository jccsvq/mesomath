"""Customized IPython REPL for MesoMath"""

from traitlets.config.loader import Config

def start_ibabcalc():
    """
    ibabcalc interactive REPL
    """    
    try:
        import IPython
        from mesomath.__about__ import __version__ as VERSION

        from mesomath import BabN as bn  # noqa: F401
        from mesomath import Blen as bl  # noqa: F401
        from mesomath import Bsur as bs  # noqa: F401
        from mesomath import Bvol as bv  # noqa: F401
        from mesomath import Bcap as bc  # noqa: F401
        from mesomath import Bwei as bw  # noqa: F401
        from mesomath import BsyG as bG  # noqa: F401
        from mesomath import BsyS as bS  # noqa: F401
        from mesomath import BsyC as bC  # noqa: F401
        from mesomath import BsyK as bK  # noqa: F401
        from mesomath import Bbri as bb  # noqa: F401

        from mesomath.metrology_presets import CAPACITY_PROUST_81 as clist
        from mesomath.metrology_presets import WEIGHT_PROUST_82 as wlist
        from mesomath.metrology_presets import SURFACE_PROUST_83 as slist
        from mesomath.metrology_presets import LENGTH_PROUST_84 as llist

        # Welcome message
        message = f"\n--- MesoMath Interactive Scribal Console {VERSION} ---\n\n"
        message += """Use: bn(number) for sexagesimal calculations
    Metrological classes: bl, bs, bv, bc, bw, bb, bG, bS, bC and bK loaded.
    Metrological presets: clist, wlist, slist, llist loaded.
    Use exit() or Ctrl-D (i.e. EOF) to exit
        """

        # Here we define what we want the user to already have loaded
        namespace = {
            "bn": bn,
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
