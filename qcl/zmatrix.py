"""
This is a xyz-to-zmatrix generation script that
I wrote due to some bugs in OpenBabel z-matrix generation
Obviously, OpenBabel is much faster, so this may not be feasible
for large systems
Also, it assumes a bonding interatomic distance will always
be shorter than a non-bonding interatomic distance
"""

from qcl import parse, write


def detectfiletype(inputfile):
    with open(inputfile, 'r') as handle:
        lines = list(handle.readlines())
        if len(lines) >= 6 and len(lines[5].split()) == 1:
            filetype = 'gzmat'
        elif len(lines[0].split()) == 1 and len(lines[2].split()) == 4:
            filetype = 'xyz'
        else:
            filetype = 'zmat'

        return filetype


def convert(inputfile, outfiletype='gzmat'):
    """Convert given inputfile to a given outputfile type"""

    filetype = detectfiletype(inputfile)

    # TODO: ....
    if filetype == 'xyz':
        ccdata_xyz = internalize(inputfile)
    else:
        print("Can only parse xyzfiles right now...")
        raise IOError

    if outfiletype == 'xyz':
        ccdata_xyz.print_xyz()
    elif outfiletype == 'gzmat':
        ccdata_xyz.print_gzmat()
    elif outfiletype == 'zmat':
        ccdata_xyz.print_zmat()
    else:
        print("Unknown outfiletype:", outfiletype)
    return


def internalize(xyzfile):
    """Convert xyzfile to internal coordinate then back to cartesian coords"""

    ccdata_xyz = parse.xyzfile(xyzfile, ccxyz=True)

    ccdata_xyz.build_zmatrix()

    ccdata_xyz.build_xyz()

    return ccdata_xyz



def main(opts):
    """Main function for xyz to zmatrix conversion"""
    convert(opts.inputfile, outfiletype=opts.outfiletype)
