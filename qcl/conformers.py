""" Conformer generation submodule"""
from __future__ import print_function

import itertools
from copy import deepcopy

# Local imports
from qcl import find, parse, write, zmatrix, obconformers

def generateconformers(ccdata_xyz, interval=60):
    """Generate conformers using in-house conformer code"""

    ccdata = ccdata_xyz

    rotatelists = []
    # Loop over atoms with dihedral angles
    for i in range(3, len(ccdata.atomnos)):
        j = ccdata.connectivity[i]
        k = ccdata.angleconnectivity[i]
        l = ccdata.dihedralconnectivity[i]

        # Prevent duplicates
        if k == l and i > 0:
            for idx in range(1, len(ccdata.connectivity[:i])):
                if ccdata.connectivity[idx] in [i,j,k] and not idx in [i,j,k]:
                    l = idx
                    break

        # Atoms involved in dihedral
        atoms = [i, j, k, l]

        # Exclude any dihedrals involving hydrogens
        if 'H' in (ccdata.elements[x] for x in atoms):
            continue

        # Gather all atoms attached to atom j to with atom i
        rotatelist = [i]
        rotatelist.extend([x for x in range(j,len(ccdata.atomnos)) if ccdata.connectivity[x] == j and not x == i and not x == j])
        rotatelists.append(rotatelist)

    # Get number of rotations (+1 for rotation of 0.0) and 359.999 because 360=0
    numrotations = int(359.9999999 / interval)+1
    intervals = [x*interval for x in range(numrotations)]

    # Printout information
    numrotatablebonds = len(rotatelists)
    numconformers = pow(numrotations, numrotatablebonds)
    print("Total number of rotatable bonds          :", numrotatablebonds)
    print("interval (degrees) of dihedral rotation :", interval)
    print("Total intervals per rotatable bond      :", numrotations)
    print("Total number of systematical conformers  :", numconformers)

    # Cartesian product of each rotatable bond and the intervals to rotate
    combinations = []
    for rotatelist in rotatelists:
        combinations.append(tuple(itertools.product([rotatelist], intervals)))

    # Cartesian product of between all intervals of all rotatable bonds
    newcombinations = tuple(itertools.product(*combinations))

    # Generate conformers by copying original ccdata_xyz and rotating dihedrals
    newconformers = []
    for combo in newcombinations:
        newconformer = deepcopy(ccdata_xyz)
        for rotation in combo:
            for atom in rotation[0]:
                newconformer.dihedrals[atom] += rotation[1]
                if newconformer.dihedrals[atom] > 360:
                    newconformer.dihedrals[atom] += -360
        newconformers.append(newconformer)

    return newconformers


def main(opts):
    """ Main function to be called as an entry point """

    ccdata_xyz = parse.xyzfile(opts.xyzfile, ccxyz=True)

    ccdata_xyz.build_zmatrix()

    newconformers = generateconformers(ccdata_xyz, interval=opts.interval)

    print(len(newconformers), "conformers generated")
    idx = 0
    for newconformer in newconformers:
        newconformer.build_xyz()
        write.xyzfile(newconformer, 'all.xyz', append=True)
        idx += 1
