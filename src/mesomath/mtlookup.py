"""Lookups in metrological tables"""

# import's section
import argparse
from mesomath.babn import BabN as bn
from mesomath.npvs import Blen as bl
from mesomath.npvs import Bsur as bs
from mesomath.npvs import Bvol as bv
from mesomath.npvs import Bcap as bc
from mesomath.npvs import Bwei as bw
from mesomath.npvs import BsyG as bG
from mesomath.npvs import BsyS as bS

# Mapping of types to classes and specific ubase
METROLOGY_MAP = {
    "L": (bl, None),  # Class, ubase (None uses the class one)
    "Lh": (bl, 1),  # Length using 'kus' as a base
    "S": (bs, None),
    "V": (bv, None),
    "C": (bc, None),
    "W": (bw, None),
    "SysG": (bG, None),
    "SysS": (bS, None),
}


def gen_parser() -> argparse.ArgumentParser:
    """User interface parser"""
    # Option definitions

    DESC = """Prints abstract number corresponding to a meassure or lists 
    measures having an abstract number."""
    EPIL = "jccsvq fecit, 2025. Public domain."

    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPIL,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--type",
        help="Metrology to use",
        choices=["L", "Lh", "S", "V", "C", "W", "SysG", "SysS"],
        default=None,
    )
    parser.add_argument("VALUE", type=str, help="Value ")
    parser.add_argument(
        "-r",
        "--reverse",
        help="Reverse lookup ,lists measures having an abstract number",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f", "--force", help="Force base unit to number FORCE", default=-1
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Prints more information",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-F",
        "--fractions",
        help="Use fractions, -F 1 to include 1/6",
        type=int,
        choices=[0, 1],
        default=-1,
    )
    parser.add_argument(
        "-p",
        "--pedantic",
        help=(
            "Write the coefficients of the units in the measurements "
            "using the S and G Systems"
        ),
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--strict",
        help="Suppress partial matches in reverse lookup.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-a",
        "--academic",
        help="With [-F|--fractions] or [-r|--remainder] uses the academic names of units.",
        action="store_true",
        default=False,
    )

    return parser


def main():
    """Entry point to mtlookup"""
    # Options parsing
    parser = gen_parser()
    args = parser.parse_args()

    selection = METROLOGY_MAP.get(args.type)
    if not selection:
        exit("Error: Tipo de metrología no reconocido.")

    met, ubase_override = selection
    ubase = ubase_override if ubase_override is not None else met.ubase
    if args.pedantic and not any([met == bG, met == bS]):
        met.prtsex = True
    
    
    # executing

    if args.reverse:
        aa = bn(args.VALUE)
        x = aa.dec * met.cfact[ubase]

        print(f"\nLooking for {met.title} with Abstract = {aa}")
        print(f"Base reference unit: {met.uname[ubase]}")
        print("-" * 50)

        for i in range(-3, 5):
            val_dec = int(x // 60**i)
            if val_dec < 1:
                break

            obj = met(val_dec)
            # Measurement formatting
            medida_str = (
                obj.prtf(args.fractions, args.academic)
                if args.fractions >= 0
                else str(obj)
            )
            abstracto = obj.sex(ubase)

            # Strict filter
            if args.strict and str(aa) != str(abstracto):
                continue

            if args.verbose:
                print(f"Medida:   {medida_str}")
                print(f"Equiv.:   {obj.SI()}")
                print(f"Abstract: {abstracto}\n")
            else:
                print(f"{medida_str:<25} <- {abstracto}")
        exit()

    m = args.VALUE
    try:
        m = int(m)
    except Exception:
        pass
    finally:
        aa = met(m)
    if args.fractions < 0:
        y = aa
    else:
        y = aa.prtf(args.fractions, args.academic)

    pp = aa.sex(ubase)
    if args.verbose:
        print("\nAbstract number for ", met.title)
        print("    Base unit: ", met.uname[ubase])
        print("========================================================")
        if pp.isreg:
            print(y, " -> ", pp, "Reciprocal: ", pp.rec())
        else:
            print(y, " -> ", pp, "Reciprocal: ", "--igi nu--")
    else:
        print(y, " -> ", pp)


if __name__ == "__main__":
    main()
