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

from polymer import utils
from polymer.ccdata_xyz import ccData_xyz


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

        if len(lines[1].split()) == 2:
            charge, multiplicity = lines[1].split()
            if utils.is_type(int, charge):
                attributes['charge'] = int(charge)
            if utils.is_type(int, multiplicity) and int(multiplicity) > 0:
                attributes['mult'] = int(multiplicity)

        geometry = [x.split() for x in lines[2:]]
        coordinates = [x[1:] for x in geometry]
        atomnos = [ptable.number[x[0]] for x in geometry]
        attributes['atomcoords'] = np.array(coordinates)
        attributes['atomnos'] = np.array(atomnos)

        if ccxyz:
            # Custom ccData_xyz attributes
            elements = [x[0] for x in geometry]
            attributes['elements'] = elements
            attributes['comment'] = lines[1]
            attributes['filename'] = xyzfile.rstrip()
            ccObject = ccData_xyz(attributes=attributes)
        else:
            ccObject = ccData(attributes=attributes)

    return ccObject


def multixyzfile(multixyzfile):
    """ Parse multixyzfile to ccData object """
    assert type(multixyzfile) == str

    attributeslist = []

    ptable = PeriodicTable()

    # Check that the file is not empty, if it is not, parse away!
    if os.stat(multixyzfile).st_size == 0:
        raise EOFError(multixyzfile+" is empty")
    else:
        with open(multixyzfile, 'r') as handle:
            lines = handle.readlines()

            # An xyz file has number of lines = number of atoms + 2
            lengthgeom = int(lines[0])+2
            numgeoms = len(lines) // lengthgeom
            print(numgeoms)

            for j in range(0, numgeoms):
                coordinates = []
                atomnos = []
                attributes = {}

                # TODO - smarter error msg if charge and multiplicity not in comment line
                charge, multiplicity = lines[1 + lengthgeom*j].split()
                # Check if charge and/or multiplicity is given in xyz comments
                if utils.is_type(int, charge):
                    attributes['charge'] = int(charge)
                if utils.is_type(int, multiplicity) and int(multiplicity) > 0:
                    attributes['mult'] = int(multiplicity)

                for i in range(2 + lengthgeom*j, lengthgeom + lengthgeom*j):
                    atomgeometry = [x for x in lines[i].split()]
                    atomnos.append(ptable.number[atomgeometry[0]])
                    coordinates.append([float(x) for x in atomgeometry[1:]])

                attributes['atomcoords'] = np.array(coordinates)
                attributes['atomnos'] = np.array(atomnos)
                attributeslist.append(attributes)

        print('Number of conformers parsed:', len(attributeslist))

        return [ccData(attributes=attrs) for attrs in attributeslist]


def mopacoutputfile(mopacoutputfile, nogeometry=True):
    """Parse MOPAC output file"""
    if not nogeometry:
        print("MOPAC geometry parsing not yet implemented - cclib TODO")
        raise

    with open(mopacoutputfile, 'r') as handle:
        lines = handle.readlines()
        attributes = {}
        for line in lines:
            if "TOTAL ENERGY" in line:
                scf = float(line.split()[3])
                scfEh = convertor(scf, 'eV', 'kcal')
                attributes['scfenergies'] = [scfEh]
                ccdata = ccData(attributes=attributes)
                setattr(ccdata, 'filename', mopacoutputfile)
                setattr(ccdata, 'index', mopacoutputfile.split('.')[0])
                # Placeholder for later
                setattr(ccdata, 'relenergies', None)
                return ccdata
