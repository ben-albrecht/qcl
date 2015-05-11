"""
This is a xyz-to-zmatrix generation script that
I wrote due to some bugs in OpenBabel z-matrix generation
Obviously, OpenBabel is much faster, so this may not be feasible
for large systems
Also, it assumes a bonding interatomic distance will always
be shorter than a non-bonding interatomic distance
"""

from qcl import parse


def internalize(xyzfile):
    """Convert xyzfile to internal coordinate then back to cartesian coords"""

    ccdata_xyz = parse.xyzfile(xyzfile, ccxyz=True)

    ccdata_xyz.build_zmatrix()

    ccdata_xyz.build_xyz()

    return ccdata_xyz


def main(opts):
    """Main function for xyz to zmatrix conversion"""
    internalize(opts.xyzfile)
