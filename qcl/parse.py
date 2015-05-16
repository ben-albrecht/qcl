""" Parsing module to convert a given file or datatype to a ccData object """

import os

import numpy as np
try:
    from cclib.parser.data import ccData
    from cclib.parser.utils import PeriodicTable
    from cclib.parser.utils import convertor
except ImportError:
    print("cclib not found!")
    raise

from qcl import utils
from qcl import periodictable as pt
from qcl.ccdata_xyz import ccData_xyz


def parse(source):
    """ Guess the identity of a particular file or data type and parse it.

        :source: Single file or data structure with some molecular data contained within

        :returns: ccData object with the molecular data parsed from source

        TODO
    """
    pass


def xyzfile(xyzfile, ccxyz=False):
    """ Parse xyzfile to ccData or ccData_xyz object"""
    if not type(xyzfile) == str:
        print(xzyfile, "is not a xyzfilename")
        raise

    attributes = {}
    ptable = PeriodicTable()

    with open(xyzfile, 'r') as handle:
        lines = handle.readlines()

        charge, mult = _chargemult(lines[1])

        geometry = [x.split() for x in lines[2:]]
        coordinates = [x[1:] for x in geometry]
        atomnos = [ptable.number[x[0]] for x in geometry]
        attributes['atomcoords'] = np.array(coordinates)
        attributes['atomnos'] = np.array(atomnos)
        attributes['natom'] = len(atomnos)
        elements = [pt.Element[x] for x in atomnos]
        attributes['atommasses'] = [pt.Mass[x] for x in elements]

        if ccxyz:
            # Custom ccData_xyz attributes
            elements = [x[0] for x in geometry]
            attributes['elements'] = elements
            attributes['comment'] = lines[1]
            attributes['filename'] = os.path.split(xyzfile.rstrip())[1]
            ccObject = ccData_xyz(attributes=attributes)
        else:
            ccObject = ccData(attributes=attributes)

    return ccObject


def multixyzfile(multixyzfile):
    """Parse multixyzfile to list of ccData objects"""
    assert type(multixyzfile) == str

    attributeslist = []

    ptable = PeriodicTable()

    # Check that the file is not empty, if it is not, parse away!
    if os.stat(multixyzfile).st_size == 0:
        raise EOFError(multixyzfile+" is empty")
    else:
        with open(multixyzfile, 'r') as handle:
            attributeslist = []
            lines = handle.readlines()
            filelength = len(lines)
            idx = 0
            while True:
                attributes = {}
                atomcoords = []
                atomnos = []

                # Get number of atoms and charge/mult from comment line
                numatoms = int(lines[idx])
                charge, mult = _chargemult(lines[idx+1])

                for line in lines[idx+2:numatoms+idx+2]:
                    atomgeometry = [x for x in line.split()]
                    atomnos.append(ptable.number[atomgeometry[0]])
                    atomcoords.append([float(x) for x in atomgeometry[1:]])
                idx = numatoms+idx+2
                attributes['charge'] = charge
                attributes['mult'] = mult
                attributes['atomcoords'] = np.array(atomcoords)
                attributes['atomnos'] = np.array(atomnos)
                attributeslist.append(attributes)

                # Break at EOF
                if idx >= filelength:
                    break

        print('Number of conformers parsed:', len(attributeslist))

        ccdatas = [ccData(attributes=attrs) for attrs in attributeslist]
        return ccdatas


def mopacoutputfile(mopacoutputfile, nogeometry=True):
    """Parse MOPAC output file"""
    if not nogeometry:
        print("MOPAC geometry parsing not yet implemented - cclib TODO")
        raise

    with open(mopacoutputfile, 'r') as handle:
        lines = handle.readlines()
        attributes = {}
        ccdata = None
        for line in lines:
            if "TOTAL ENERGY" in line:
                scf = float(line.split()[3])
                scfkcal = convertor(scf, 'eV', 'kcal')
                attributes['scfenergies'] = [scfkcal]
                ccdata = ccData(attributes=attributes)
                break

        if not ccdata:
            print(mopacoutputfile, " - no TOTAL ENERGY found")
            raise
        else:
            return ccdata


def _chargemult(line):
    """Get charge/mult from line. Default to 0,1 if no charge/mult found"""
    line = line.split()
    charge = 0
    mult = 1
    if len(line) == 2:
        if utils.is_type(int, line[0]):
            charge = int(line[0])
        if utils.is_type(int, line[1]) and int(line[1]) > 0:
            mult = int(line[1])
    return charge, mult


