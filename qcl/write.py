""" Write ccData object to file """

from __future__ import print_function

from os.path import join

try:
    from cclib.parser.utils import PeriodicTable
except ImportError:
    raise ImportError("cclib not found!")

from qcl import templates


def inputfiles(ccdatas, templatefiles, path):
    """ Write multiple inpfiles for multiple templates and ccdatas"""
    for ccdata in ccdatas:
        for templatefile in templatefiles:
            inpfile = join(path, str(ccdatas.index(ccdata)))
            inpfile = inpfile + '.' + templatefile
            inputfile(ccdata, templatefile, inpfile)


def inputfile(ccdata, templatefile, inpfile):
    """Generic write ccdata + templatefile to inpfile"""
    if templates.exists(templatefile):
        if type(ccdata) is list \
            and 'fsm' in templatefile \
                and '.qcm' in templatefile:
            qchemfsminputfile(ccdata, templatefile, inpfile)
        elif '.mop' in templatefile:
            mopacinputfile(ccdata, templatefile, inpfile)
        elif '.qcm' in templatefile:
            qcheminputfile(ccdata, templatefile, inpfile)
        else:
            print(templatefile, "failed -not a valid extension")


def qcheminputfile(ccdata, templatefile, inpfile):
    """
    Generate input file from geometry (list of lines) depending on job type

    :ccdata:        ccData object
    :templatefile:  templatefile - tells us which template file to use
    :inpfile:     OUTPUT - expects a path/to/inputfile to write inpfile
    """
    assert type(inpfile) is str

    with open(inpfile, 'w') as handle:

        if ccdata.charge:
            charge = ccdata.charge
        else:
            charge = 0
        if ccdata.mult:
            mult = ccdata.mult
        else:
            print("Multiplicity not found, set to 1 by default")
            mult = 1

        # $molecule
        handle.write("$molecule\n")
        handle.write("%s %s\n" % (charge, mult))

        # Geometry (Maybe a cleaner way to do this..)
        atomnos = [PeriodicTable().element[x] for x in ccdata.atomnos]
        if not type(ccdata.atomcoords) is list:
            atomcoords = ccdata.atomcoords.tolist()

        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, atomnos[i])

        for atom in atomcoords:
            handle.write("  %s %10.8f %10.8f %10.8f\n" % tuple(atom))

        handle.write("$end\n\n")
        # $end

        # $rem
        with open(templates.get(templatefile), 'r') as templatehandle:
            templatelines = [x for x in templatehandle.readlines()]

        for line in templatelines:
            handle.write(line)
        # $end


def qchemfsminputfile(ccdatas, templatefile, inpfile):
    """
    Temporary fix for the need of a different input format for
    frozen string method
    """
    # fsm assertions
    assert len(ccdatas) == 2
    assert type(inpfile) is str

    with open(inpfile, 'w') as handle:

        ccdata = ccdatas[0]

        if ccdata.charge:
            charge = ccdata.charge
        else:
            print("Charge not found, set to 0 by default")
            charge = 0
        if ccdata.mult:
            mult = ccdata.mult
        else:
            print("Multiplicity not found, set to 1 by default")
            mult = 1

        # $molecule
        handle.write("$molecule\n")
        handle.write("%s %s\n" % (charge, mult))

        # Geometry (Maybe a cleaner way to do this..)
        atomnos = [PeriodicTable().element[x] for x in ccdata.atomnos]
        if not type(ccdata.atomcoords[0]) is list:
            atomcoords = [x.tolist() for x in ccdata.atomcoords]
        else:
            atomcoords = ccdata.atomcoords

        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, atomnos[i])

        for atom in atomcoords:
            handle.write("  %s %10.8f %10.8f %10.8f\n" % tuple(atom))

        handle.write("******\n")

        ccdata = ccdatas[1]

        # Geometry (Maybe a cleaner way to do this..)
        atomnos = [PeriodicTable().element[x] for x in ccdata.atomnos]
        if not type(ccdata.atomcoords[0]) is list:
            atomcoords = [x.tolist() for x in ccdata.atomcoords]
        else:
            atomcoords = ccdata.atomcoords

        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, atomnos[i])

        for atom in atomcoords:
            handle.write("  %s %10.8f %10.8f %10.8f\n" % tuple(atom))

        handle.write("$end\n\n")
        # $end

        # $rem
        with open(templates.get(templatefile), 'r') as templatehandle:
            template = [x for x in templatehandle.readlines()]

        for line in template:
            handle.write(line)
        # $end


def mopacinputfile(ccdata, templatefile, inpfile):
    """
    Generate input file from geometry (list of lines) depending on job type

    :ccdata:        ccData object
    :templatefile:  templatefile- tells us which template file to use
    :inputfile:     OUTPUT - expects a path/to/inputfile to write inpfile
    """
    assert type(inpfile) is str
    attributes = ccdata.getattributes()
    assert len(attributes['atomnos']) == len(attributes['atomcoords'])

    with open(templates.get(templatefile), 'r') as templatehandle:
        template = [x for x in templatehandle.readlines()]

    with open(inpfile, 'w') as handle:

        for line in template:
            handle.write(line)

        # Maybe some day I will write something meaningful here
        handle.write("comment line 1\n")
        handle.write("comment line 2\n")

        # The MOPAC input is basically an xyz file

        # Geometry (Maybe a cleaner way to do this..)
        atomnos = [PeriodicTable().element[x] for x in attributes['atomnos']]
        if not type(atomcoords) is list:
            atomcoords = attributes['atomcoords'].tolist()
        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, atomnos[i])

        for atom in atomcoords:
            handle.write("%s %10.8f %10.8f %10.8f\n" % tuple(atom))


def xyzfile(ccdata, fname, append=False):
    if append:
        permission = 'a'
    else:
        permission = 'w'

    with open(fname, permission) as handle:
        handle.write(str(len(ccdata.atomnos)) + "\n")

        if hasattr(ccdata, 'comment'):
            handle.write(ccdata.comment)
        else:
            handle.write("\n")

        atomnos = [PeriodicTable().element[x] for x in ccdata.atomnos]
        atomcoords = ccdata.atomcoords
        if not type(atomcoords[0]) is list:
            atomcoords = [x.tolist() for x in atomcoords]

        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, atomnos[i])

        for atom in atomcoords:
            handle.write("%s %10.8f %10.8f %10.8f\n" % tuple(atom))


