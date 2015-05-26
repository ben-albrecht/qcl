""" Submodule for setting up TS searches"""
from __future__ import print_function

import os
import sys
import copy

from qcl import parse, write, templates
from qcl.ccdata_xyz import ccData_xyz

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

    ccdata = ccopen(outputfile).parse()

    fname, _ = os.path.splitext(outputfile)
    #xyzfile = fname+'.xyz'
    #write.xyzfile(outputccdata, xyzfile)

    product = ccData_xyz(ccdata.getattributes(), ccdataconvert=True)
    ccdatas = []
    #product = parse.xyzfile(xyzfile, ccxyz=True)
    product.build_zmatrix()
    reactant = copy.deepcopy(product)
    reactant.distances[1] += shift

    # TODO:If reactants provided, use their geometry internal coords
    # and modify internalcoords of reactant

    # FIXME hardcoded paths instead of cli args
    #rpaths = ['../../initiators/MeO/0.omegab97x-d_opt.out', '../../ketenes/TMS/0.omegab97x-d_opt.out']

    #reactants = []
    #for rpath in rpaths:
    #    reactants.append(parse.xyzfile(rpath, ccdata_xyz=True))

    #for r in reactants:
    #    r.build_zmatrix()

    # TODO Determine which reactant is which
    # Some ways to do this:
        # numatom, atomnos
    # TODO How to deal with symmetrical reactants?
        # Just guess (1/2 chance) - possibly cli to swap if wrong

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
    else:
        #reactant.print_xyz()
        reactant.print_gzmat()


def main(opts):
    """ Main function to be called as an entry point """


    stretch(opts.outputfile, opts.length, opts.templatefiles)
