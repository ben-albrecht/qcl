""" Submodule for finding minima among input files """

from __future__ import print_function

import sys

"""
# Currently cannot use cclib due to conversion (eV to Eh) errors
try:
    from cclib.parser import ccopen
    from cclib.parser.utils import convertor
except ImportError:
    print("cclib not found!")
    sys.exit()
"""


def scfenergy(outputfile):
    """ Temp fix for Q-Chem outputs (need to fix cclib upstream)"""

    scfenergies = []

    with open(outputfile, 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            if 'Total energy in the final basis set' in line:
                scfenergies.append(float(line.split()[-1]))
    if not scfenergies:
        print(outputfile, "incomplete")
        scfenergies.append(0)
    return scfenergies[-1]


def minima(outputfiles=None, returnfile=False):
    # Assume all outputs in current directory, if no args
    if not outputfiles:
        #TODO
        pass
    if not type(outputfiles) is list:
        outputfiles = [outputfiles]

    # TODO Error checks

    #Emin = ccopen(outputfiles[0]).parse().scfenergies[-1]
    Emin = scfenergy(outputfiles[0])
    Filemin = outputfiles[0]

    for outputfile in outputfiles:
        #E = convertor(ccopen(outputfile).parse().scfenergies[-1], "eV", "hartree")
        E = scfenergy(outputfile)
        if E < Emin:
            Emin = E
            Filemin = outputfile

    print(Filemin, Emin)

    if returnfile:
        return Filemin
    else:
        return E


def main(opts):
    """ Main function to be called as an entry point """

    minima(opts.outputfiles)
