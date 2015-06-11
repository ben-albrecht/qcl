""" Write ccData object to file """

from __future__ import print_function

from os.path import join

from qcl import templates
from qcl import periodictable as pt


def xyzfile(ccdata, fname, append=False):
    """xyzfile"""
    if append:
        permission = 'a'
    else:
        permission = 'w'
    with open(fname, permission) as handle:
        handle.write(_xyzfile(ccdata))


def _xyzfile(ccdata):
    """xyzfile string"""
    string = ''

    string += str(len(ccdata.atomnos)) + '\n'

    if hasattr(ccdata, 'comment'):
        string += ccdata.comment
    else:
        string += '\n'

    atomnos = [pt.Element[x] for x in ccdata.atomnos]
    atomcoords = ccdata.atomcoords[-1]
    if not type(atomcoords) is list:
        atomcoords = [x.tolist() for x in atomcoords]

    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        string += '  {0} {1:10.8f} {2:10.8f} {3:10.8f}\n'.format(*atom)

    return string


def inputfiles(ccdatas, templatefiles, path='./', indexed=False):
    """ Write multiple inpfiles for multiple templates and ccdatas
        indexed assumed the ccdata object has filename and starts with number
    """
    for ccdata in ccdatas:
        if indexed:
            index = ccdata.filename.split('.')[0]
        else:
            index = str(ccdatas.index(ccdata))
        for templatefile in templatefiles:
            inpfile = join(path, index)
            inpfile = inpfile + '.' + templatefile
            inputfile(ccdata, templatefile, inpfile)


def inputfile(ccdata, templatefile, inpfile):
    """Generic write ccdata + templatefile to inpfile"""
    if templates.exists(templatefile):
        if type(ccdata) is list \
            and 'fsm' in templatefile \
                and '.qcm' in templatefile:
            string = _qchemfsminputfile(ccdata, templatefile, inpfile)
        elif '.mop' in templatefile:
            string = _mopacinputfile(ccdata, templatefile, inpfile)
        elif '.qcm' in templatefile:
            string = _qcheminputfile(ccdata, templatefile, inpfile)
        else:
            print(templatefile, "failed -not a valid extension")
            return

        with open(inpfile, 'w') as handle:
            handle.write(string)


def _qcheminputfile(ccdata, templatefile, inpfile):
    """
    Generate input file from geometry (list of lines) depending on job type

    :ccdata:        ccData object
    :templatefile:  templatefile - tells us which template file to use
    :inpfile:     OUTPUT - expects a path/to/inputfile to write inpfile
    """

    string = ''

    if hasattr(ccdata, 'charge'):
        charge = ccdata.charge
    else:
        charge = 0
    if hasattr(ccdata, 'mult'):
        mult = ccdata.mult
    else:
        print('Multiplicity not found, set to 1 by default')
        mult = 1

    # $molecule
    string += '$molecule\n'
    string += '{0} {1}\n'.format(charge, mult)

    # Geometry (Maybe a cleaner way to do this..)
    atomnos = [pt.Element[x] for x in ccdata.atomnos]
    atomcoords = ccdata.atomcoords[-1]
    if not type(atomcoords) is list:
        atomcoords = atomcoords.tolist()

    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        string += '  {0} {1:10.8f} {2:10.8f} {3:10.8f}\n'.format(*atom)

    string += '$end\n\n'
    # $end

    # $rem
    with open(templates.get(templatefile), 'r') as templatehandle:
        templatelines = [x for x in templatehandle.readlines()]

    for line in templatelines:
        string += line
    # $end

    return string


def _qchemfsminputfile(ccdatas, templatefile, inpfile):
    """
    Temporary fix for the need of a different input format for
    frozen string method
    """

    string = ''

    # fsm assertions
    if len(ccdatas) != 2:
        print('2 ccdata objects were not passed for a fsm method')
        raise StandardError

    ccdata = ccdatas[0]

    if hasattr(ccdata, 'charge'):
        charge = ccdata.charge
    else:
        print("Charge not found, set to 0 by default")
        charge = 0
    if hasattr(ccdata, 'mult'):
        mult = ccdata.mult
    else:
        print("Multiplicity not found, set to 1 by default")
        mult = 1

    # $molecule
    string += '$molecule\n'
    string += '{0} {1}\n'.format(charge, mult)

    # Geometry (Maybe a cleaner way to do this..)
    atomnos = [pt.Element[x] for x in ccdata.atomnos]

    atomcoords = ccdata.atomcoords[-1]
    if not type(atomcoords) is list:
        atomcoords = [x.tolist() for x in atomcoords]

    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        string += '  {0} {1:10.8f} {2:10.8f} {3:10.8f}\n'.format(*atom)

    string += '******\n'

    ccdata = ccdatas[1]

    # Geometry (Maybe a cleaner way to do this..)
    atomnos = [pt.Element[x] for x in ccdata.atomnos]
    atomcoords = ccdata.atomcoords[-1]
    if not type(atomcoords) is list:
        atomcoords = [x.tolist() for x in atomcoords]

    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        string += '  {0} {1:10.8f} {2:10.8f} {3:10.8f}\n'.format(*atom)

    string += '$end\n\n'
    # $end

    # $rem
    with open(templates.get(templatefile), 'r') as templatehandle:
        template = [x for x in templatehandle.readlines()]

    for line in template:
        string += line
    # $end
    return string


def _mopacinputfile(ccdata, templatefile, inpfile):
    """
    Generate input file from geometry (list of lines) depending on job type

    :ccdata:        ccData object
    :templatefile:  templatefile- tells us which template file to use
    :inputfile:     OUTPUT - expects a path/to/inputfile to write inpfile
    """
    mopacmult = {1: 'SINGLET',
                 2: 'DOUBLET',
                 3: 'TRIPLET',
                 4: 'QUARTET',
                 5: 'QUINTET',
                 6: 'SEXTET',
                 7: 'SEPTET',
                 8: 'OCTET',
                 9: 'NONET'
                 }

    string = ''

    attributes = ccdata.getattributes()

    with open(templates.get(templatefile), 'r') as templatehandle:
        template = [x for x in templatehandle.readlines()]

    # We assume first line is input commands
    template[0] = template[0].rstrip('\n')
    template[0] += ' CHARGE={0} {1}\n'.format(ccdata.charge,
                                              mopacmult[ccdata.mult])
    for line in template:
        string += line

    # Maybe some day I will write something meaningful here
    string += 'comment line 1\n'
    string += 'comment line 2\n'

    # The MOPAC input is basically an xyz file

    # Geometry (Maybe a cleaner way to do this..)
    atomnos = [pt.Element[x] for x in attributes['atomnos']]

    atomcoords = ccdata.atomcoords[-1]
    if not type(atomcoords) is list:
        atomcoords = [x.tolist() for x in atomcoords]

    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        string += '  {0} {1:10.8f} {2:10.8f} {3:10.8f}\n'.format(*atom)

    return string
