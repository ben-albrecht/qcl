""" Submodule for setting up TS searches"""
from __future__ import print_function

import os
import sys
import copy

from qcl import parse, write, templates

try:
    from cclib.parser import ccopen
except ImportError:
    print("cclib not found!")
    raise


def stretch(outputfile, shift=2.0, templatefiles=None):
    """
    Generate transition state search for given xyzfile,
    assuming that the first 2 atoms are the bond forming atoms

    outputfile is assumed to be a geometry optimization Q-Chem output

    TODO: option to set fname, and default to the templatefilename + index?
    """
    savexyz = True

    # If templatefiles doesn't exist, we only save stretched xyz
    if templatefiles:

        # Always convert templatefiles into list
        if not type(templatefiles) is list:
            templatefiles = [templatefiles]

        # Only keep the templatefiles that exists
        templatefiles = [templatefile for templatefile in templatefiles
                         if templates.exists(templatefile)]

        # If at least one templatefile exists, we don't save xyz
        if templatefiles:
            savexyz = False

    outputccdata = ccopen(outputfile).parse()

    fname, _ = os.path.splitext(outputfile)
    xyzfile = fname+'.xyz'
    write.xyzfile(outputccdata, xyzfile)

    ccdatas = []
    product = parse.xyzfile(xyzfile, ccxyz=True)
    product.build_zmatrix()
    reactant = copy.deepcopy(product)
    reactant.distances[1] += shift

    product.build_xyz()
    reactant.build_xyz()

    ccdatas.append(reactant)
    ccdatas.append(product)

    if not savexyz:
        # Get correct charge/multiplicity
        for ccdata in ccdatas:
            ccdata.charge = outputccdata.charge
            ccdata.mult = outputccdata.mult

        for i in range(len(templatefiles)):
            if len(templatefiles) == 1:
                idx = ''
            else:
                idx = '-'+str(i)

            if 'opt' in fname:
                fname = fname.replace('opt', 'fsm')
            else:
                fname = fname + '_fsm'

            write.inputfile(ccdatas,
                            templatefiles[i],
                            fname+idx+'.qcm')

    os.remove(xyzfile)


def main(opts):
    """ Main function to be called as an entry point """


    stretch(opts.outputfile, opts.length, opts.templatefiles)
