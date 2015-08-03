"""Handles setting up a new job from some parsed data using templates"""

from __future__ import print_function

from . import parse, write


def setupjob(inputfile, templatefile, filetype=None, multiplicity=1):
    """
    Parse inputfile into ccdata object,
    then generate new input with templatefile

    Currently for converting xyzfiles into inputs quickly

    :inputfile: TODO
    :filetype: TODO
    :templatefile: TODO
    :returns: TODO

    """

    if not filetype:
        # TODO - auto determine filetype
        print("Not yet implemented - please provide filetype")
        return

    if filetype == 'xyz':
        ccdata = parse.xyzfile(inputfile)

    if not hasattr(ccdata, 'mult'):
        ccdata.mult = multiplicity

    inputdata = write.inputfile(ccdata, templatefile)

    print(inputdata)


def main(opts):
    """ Main function to be called as an entry point """
    if opts.filetype:
        setupjob(opts.inputfile, opts.templatefile, filetype=opts.filetype, multiplicity=opts.multiplicity)
    else:
        setupjob(opts.inputfile, opts.templatefile, multiplicity=opts.multiplicity)
