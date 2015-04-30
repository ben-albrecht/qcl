"""Openbabel conformer generation wrapper - Maybe use Pybel someday"""

# TODO - sometimes obabel conformation generation bugs out
#        consider converting to zmatrix prior to conformer generation
from subprocess import check_output
import os
import shlex
try:
    import six
except ImportError:
    raise ImportError("Cannot import six")

from qcl import find, parse, write

def obconformer(xyzfile, conformerfile=None, nconf=1000):
    """ Python wrapper for openbabel call to conformer
    Using the genetic algorithm variation

    :xyzfile: xyzfile to use as start for conformer generation
    :returns: Nothing, but outputs to conformers/species-conformers
    """
    if not conformerfile:
        tag = find.tag(xyzfile)
        conformerfile = find.fromtag('obconformer', tag)

    obabelcommand = \
        "obabel --writeconformers --conformer --nconf " + str(nconf) +\
        " -i xyz " + xyzfile + " -o xyz -O " + conformerfile

    print(obabelcommand)

    check_output(shlex.split(obabelcommand))


def conformers(xyzinput, nconf=1000, force=False, templatefiles=None):
    """
    Generate inputs of top conformer candidates after conformer search
        and generate optimization inputs

    This script creates a subdirectory, 'conformers' in the directory of the
        xyzinput file and generates the inputs in this directory,
        using a template file, expected in $project_root/templates/

    :xyzfile: xyzfile
    """
    if not type(xyzinput) is str:
        raise Exception("XYZ Input file was not a string")
    if not os.path.isfile(xyzinput):
        raise Exception("XYZ Input file does not exist")

    tag = find.tag(xyzinput)

    # Create new subdirectory for conformers
    subdir = os.path.join(os.path.dirname(xyzinput), 'conformers')
    print("Conformer geometry optimization input files written in: ", subdir)
    if not os.path.exists(subdir):
        os.makedirs(subdir)

    # Run conformer search algorithm via openbabel wrapper
    conformerfile = find.fromtag('obconformer', tag)

    # Get user response for overwrite preference
    response = 'O'
    if os.path.isfile(conformerfile):
        if not force:
            print(conformerfile, "already exists. What would you like to do?")
            print("[O]verwrite existing ", conformerfile)
            print("[R]ead from existing ", conformerfile)
            print("[Any other key] to abort")
            response = six.moves.input()
    if response.upper() == 'O':
        obconformer(xyzinput, conformerfile=conformerfile, nconf=nconf)
    elif not response.upper() == 'R':
        print("Aborting")
        exit(1)

    if not templatefiles:
        raise RuntimeError("No templatefiles given")
    elif not type(templatefiles) is list:
        templatefiles = [templatefiles]

    ccdatas = parse.multixyzfile(find.fromtag('obconformer', tag))
    conformerspath = find.fromtag('conformers', tag)
    write.inputfiles(ccdatas, templatefiles, path=conformerspath)

def main(opts):
    """ Main function to be called as an entry point """
    print(""" Remember:\n
              * Put the charge multiplicity in comment line of xyz\n
              * (For Products) Put the bond-forming atoms as the first two atoms in xyz\n
              * Create a tag file (`touch tag`)\n
          """)
    conformers(opts.xyzfile,
               opts.nconf,
               opts.force,
               templatefiles=opts.templatefiles)
