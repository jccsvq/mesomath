"""Prints Babylonian/sexagesimal multiplication tables"""

# import's section

import argparse

from mesomath.babn import BabN as bn
from mesomath.glyphs import TIMES_LABEL as TIMES
from mesomath.glyphs import pad_cuneiform_right


# Functions
def multable(
    n: int | str,
    pral: bool = True,
    sep: str = ":",
    fill: bool = False,
    cuneiform: bool = False,
    stroke: bool = False,
    float: bool = False,
) -> None:
    """Returns the n multiplication table for principal numbers or for all

    :n: decimal integer < 60
    :pral: if True writes the table for principal numbers:
          [i+1 for i in range(20)]+[30,40,50]
          if False writes the table for:
          [i+1 for i in range(59)]
          (default: True)
    :type pral: bool, (default: True)
    :sep: sexagesimal digits separator (default: ":")
    :type sep: str, (default: ":")
    :fill: add left zero to sexagesimal digits <= 9 (default: False)
    :type fill: bool, (default: False)
    :cuneiform: output is in cuneiform (default: False)
    :type cuneiform: bool, (default: False)
    :stroke: strike out empty space (sexagesimal digit zero), default: False
    :type stroke: bool, (default: False)
    :float: results are floating point (default: False)
    :type float: bool, (default: False)
    :return: None

    """
    # Normalization: we accept int, str, or even BabN
    nn = bn(str(n)).dec if not isinstance(n, bn) else n.dec

    # Backup of BabN's global state
    oldsep, oldfill = bn.sep, bn.fill
    bn.sep, bn.fill = sep, fill

    try:
        # The 'principal' numbers of the Babylonian tradition
        pnum = [i + 1 for i in range(20)] + [30, 40, 50] if pral else range(1, 60)

        if cuneiform:
            val = bn(n).to_cunei(stroke=stroke, alter=True)
            hh = pad_cuneiform_right(f" {val} {TIMES}  𒐕  ", 15)
            lh = len(hh)
            hh2 = pad_cuneiform_right(f"{val}", len(val) + 4)
            lh2 = len(hh2)
            header = f"|{hh}|{hh2}|"
            print(f"\n{header}")
            print("|" + "-" * lh + "|" + "-" * lh2 + "|")
        else:
            ll = f" i *  {str(n)}"
            lh = len(ll)
            header = "|  i  |" + ll + "|"
            print(f"\n{header}")
            print("|-----|" + "-" * lh + "|")

        for i in pnum:
            # Dynamic alignment so that the table doesn't break with large numbers
            t2 = (bn(nn * i)).f() if float else bn(nn * i)
            if cuneiform:
                if i > 1:
                    a1 = bn(i).to_cunei(stroke=stroke, alter=True)
                    a2 = t2.to_cunei(stroke=True, alter=True)
                    b1 = pad_cuneiform_right(TIMES + "  " + a1, lh)
                    b2 = pad_cuneiform_right(a2, lh2)
                    print("|" + b1 + "|" + b2 + "|")
            else:
                print(f"| {i:2d}  |  {str(t2).rjust(lh - 2)}|")
    finally:
        # Guaranteed state restoration
        bn.sep, bn.fill = oldsep, oldfill


def listtables() -> None:
    """Lists multipliers traditionally used by Babylonian scribes."""
    multipliers = (
        "50 45 44:26:40 40 36 30 25 24 22:30 20 18 16:40 16 15 12:30 12 "
        "10 9 8:20 8 7:30 7:12 7 6:40 6 5 4:30 4 3:45 3:20 3 2:30 2:24 2 1:40 "
        "1:30 1:20 1:15"
    ).split()

    print("\nSTANDARD MULTIPLIERS TABLE")
    print(f"{'Value':<12} | {'Reciprocal':>10}")
    print("-" * 25)

    for m in multipliers:
        val = bn(m)
        try:
            # We try to calculate the reciprocal
            rec = str(val.rec())
        except Exception as e:
            # For "irregular" numbers like 7
            rec = "irreg."
            print(e)

        print(f"{str(val):<12} | {rec:>10}")


def gen_parser() -> argparse.ArgumentParser:
    """User interface parser"""
    DESC = """Prints Babylonian multiplication tables."""
    EPIL = "jccsvq dub-sar fecit, 2025. Public domain."

    # Option definitions
    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPIL,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "mult",
        type=str,
        help="Multiplier, use 0 for a list of multiplication tables used in\
         scribal learning",
        default="1",
    )
    parser.add_argument(
        "-s", "--separator", type=str, help="Sexagesimal digit separator", default=":"
    )
    parser.add_argument(
        "-p",
        "--principal",
        help="Use only principal numbers",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--cuneiform",
        help="Output is cuneiform",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-z",
        "--zeros",
        help="strike out empty spaces",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f", "--fill", help="Pad with zeros", action="store_true", default=False
    )
    parser.add_argument(
        "--float", help="floating results", action="store_true", default=False
    )

    return parser


def main():
    """Module entry point"""
    # Option parsing
    parser = gen_parser()
    args = parser.parse_args()

    # executing
    if args.mult == "0":
        listtables()
    else:
        multable(
            args.mult,
            pral=args.principal,
            sep=args.separator,
            fill=args.fill,
            cuneiform=args.cuneiform,
            stroke=args.zeros,
            float=args.float,
        )


if __name__ == "__main__":
    main()
