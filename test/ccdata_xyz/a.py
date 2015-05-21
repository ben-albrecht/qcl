#!/usr/bin/env python3
# encoding: utf-8

from qcl.ccdata_xyz import ccData_xyz
from qcl.stretch import stretch
from cclib.parser import ccopen


def main():

    stretch('product.out')

    rfiles = ['r1.out', 'r2.out']
    reactants = []
    for rfile in rfiles:
        tmp = ccopen(rfile).parse()
        reactants.append(ccData_xyz(tmp.getattributes(), ccdataconvert=True))

    for reactant in reactants:
        reactant.build_zmatrix()
        reactant.print_gzmat()

if __name__ == '__main__':
    main()
