"""Customized Python REPL for babcalc-Kriger"""

import code
import os
import readline
import rlcompleter
import runpy
import sys

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

message = f"""\nWelcome to Babylonian Calculator {VERSION}
    ...the calculator that every scribe should have!

Use: bn(number) for sexagesimal calculations
Metrological classes: bl, bs, bv, bc, bw, bG, bS, bC, bK and bb loaded.
Use exit() or Ctrl-D (i.e. EOF) to exit
"""

sys.ps1 = "--> "


def main():
    """
    Entry point
    """
    args = sys.argv[1:]

    # Clean base context
    context = {
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
        "VERSION": VERSION,
        "exit": exit,
        "quit": quit,
    }

    # Case: Help
    if "--help" in args or "-h" in args:
        print(f"babcalc {VERSION} - Command Line Interface")
        print("\nUsage:")
        print("  babcalc                 Launch interactive REPL")
        print("  babcalc <script.py>     Execute a script")
        print("  babcalc -i <script.py>  Execute a script and stay in interactive mode")
        print(
            "  babcalc -m <module>     Run a library module (Reserved for future use)"
        )
        print("  babcalc --help          Show this message")
        return

    # Case 1: babcalc (pure REPL)
    if not args:
        start_interactive_repl(local_vars=context, banner=message)

    # Case 4: babcalc -m module
    elif args[0] == "-m" and len(args) > 1:
        module_name = args[1]
        sys.argv = args[1:]  # Ajustar para el módulo
        runpy.run_module(module_name, run_name="__main__", alter_sys=True)

    # Case 3: babcalc -i script.py
    elif args[0] == "-i" and len(args) > 1:
        script_path = args[1]
        if not os.path.exists(script_path):
            print(f"Error: File '{script_path}' not found.")
            sys.exit(1)

        # Adjust sys.argv so that the script sees its own arguments
        sys.argv = args[1:]
        script_globals = runpy.run_path(script_path, run_name="__main__")

        context.update(script_globals)
        start_interactive_repl(local_vars=context)

    # Case 2: babcalc script.py
    else:
        script_path = args[0]
        if not os.path.exists(script_path):
            print(f"Error: File '{script_path}' not found.")
            sys.exit(1)

        sys.argv = args[:]  # The script receives the complete list
        runpy.run_path(script_path, run_name="__main__")


def run_script(path: str):
    """
    Execute a .py file in the current context.

    :param path: path to the .py file
    :type path: str
    """
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found.")
        sys.exit(1)
    # Run the script as if it were the __main__ script
    runpy.run_path(path, run_name="__main__")


def start_interactive_repl(local_vars: dict = None, banner: str = ""):
    """
    babcalc interactive REPL


    :param local_vars: context variables dictionary , defaults to None
    :type local_vars: dict, optional
    :param banner: welcome banner, defaults to ""
    :type banner: str, optional
    """
    # 1. Configure the history file
    history_file = os.path.expanduser("~/.babcalc_history")
    if os.path.exists(history_file):
        readline.read_history_file(history_file)

    # 2. Configure autocomplete with TAB
    # The completer needs to know the local variable dictionary
    readline.set_completer(rlcompleter.Completer(local_vars).complete)
    # libedit/readline
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    # 3. Save history on exit
    import atexit

    atexit.register(readline.write_history_file, history_file)
    
    # 4. Launch the REPL
    if not sys.stdin.isatty() or len(sys.argv) > 1:
        # Silent mode
        code.interact(
            banner="",
            local=local_vars,
            exitmsg="",
        )
    else:
        # Interactive mode
        code.interact(
            banner=banner,
            local=local_vars,
            exitmsg="\n--- Exiting babcalc, Bye! ---\n",
        )


if __name__ == "__main__":
    """
    Entry point
    """
    main()
