#!/usr/bin/env -S python3  
'''Looks back in metrological table'''

# Change the `sys.path.append` argument to the absolute path of the directory 
# containing the `mesomath` module ( your installation directory).
import sys, argparse
sys.path.append("/home/jesus/Nextcloud/MesoMath")  # <- change this

# import's section
from mesomath.babn import BabN as bn
from mesomath.npvs import Blen as bl
from mesomath.npvs import Bsur as bs
from mesomath.npvs import Bvol as bv
from mesomath.npvs import Bcap as bc
from mesomath.npvs import Bwei as bw
from mesomath.npvs import BsyG as bG
from mesomath.npvs import BsyS as bS


if __name__ == '__main__':

# Option definitions

    DESC = '''Prints abstract number corresponding to a meassure or lists 
    measures having an abstract number.'''
    EPIL = "jccsvq fecit, 2025. Public domain."

    parser = argparse.ArgumentParser(description=DESC,
        epilog=EPIL,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--type',
        help='Metrology to use',
        choices=['L','Lh','S','V','C','W','SysG','SysS'],
        default=None)
    parser.add_argument('VALUE',
        type=str,
        help='Value ')
    parser.add_argument('-r', '--reverse',
        help='Reverse lookup ,lists measures having an abstract number',
        action='store_true',
        default=False)
    parser.add_argument('-f', '--force',
        help='Force base unit to number FORCE',
        default=-1)
    parser.add_argument('-v', '--verbose',
        help='Prints more information',
        action='store_true',
        default=False)


# Options parsing
    args = parser.parse_args()



# Main section; selecting classes and defining default table ubase
    if args.type == 'L':
        met = bl
    elif args.type == 'Lh':
        met = bl
    elif args.type == 'S':
        met = bs
    elif args.type == 'V':
        met = bv
    elif args.type == 'C':
        met = bc
    elif args.type == 'W':
        met = bw
    elif args.type == 'SysG':
        met = bG
    elif args.type == 'SysS':
        met = bS
    else:
        exit()

    ubase = met.ubase
    if args.type == 'Lh':
        ubase = 1
    if int(args.force) >= 0:
        ubase = int(args.force)

# executing    

    if args.reverse:
        a = args.VALUE
        aa = bn(a)
        adec = aa.dec
        x = adec*met.cfact[ubase]
        print('\nLooking for ', met.title+'s with abstract = ',a)
        print('    Base unit: ', met.uname[ubase])
        print('========================================================')
        for i in range(-3,5):
            x1 = int(x//60**i) 
            if x1 >= 1:
                y = met(x1)
                pp = met(x1).sex(ubase)
                if args.verbose:
                    print(y, '\n    Equiv.: ', y.SI(), '\n    Abstract: ', pp)
                else:
                    print(y, ' <- ', pp)
            else:
                break
        exit()


    m = args.VALUE
    aa = met(m)
    pp = aa.sex(ubase)
    if args.verbose:
        print('\nAbstract number for ', met.title)
        print('    Base unit: ', met.uname[ubase])
        print('========================================================')
        if pp.isreg:
            print(m,' -> ', pp, 'Reciprocal: ',pp.rec())
        else:
            print(m,' -> ', pp, 'Reciprocal: ','--igi nu--')
    else:
        print(m,' -> ', pp)
    
