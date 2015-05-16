#!/usr/bin/env python
# encoding: utf-8
"""Compute RMSD between 2 xyz files"""

import sys

import numpy as np
from numpy.linalg import norm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from qcl import parse, write, zmatrix


def rmsd(xyzfile1, xyzfile2, thresh = 2.0):
    """Main function of script"""
    ccdata1 = zmatrix.internalize(xyzfile1)
    ccdata2 = zmatrix.internalize(xyzfile2)

    if ccdata1.natom != ccdata2.natom:
        print("Not same number of atoms")
        sys.exit(1)

    translatetoCOM(ccdata1)
    translatetoCOM(ccdata2)

    alignmolecules(ccdata1, ccdata2)

    rmsd, maxdiff = compute_rmsd(ccdata1, ccdata2)

    print('rmsd = ', rmsd)
    print('maxdiff = ', maxdiff)

    return maxdiff < thresh


def compute_rmsd(ccdata1, ccdata2):
    """Compute RMSD between two molecules
       :returns: (rmsd, maxdisplacement)
    """
    natom = ccdata1.natom
    rmsd = 0.0
    maxdiff = 0.0
    for i in range(natom):
        diff = norm(ccdata1.atomcoords[i] - ccdata2.atomcoords[i])
        rmsd += diff
        if diff > maxdiff:
            maxdiff = diff

    rmsd /= natom

    return rmsd, maxdiff


def translatetoCOM(ccdata):
    """Translate molecule to center-of-mass coordinates"""
    natoms = ccdata.natom
    com = np.zeros(3, dtype=np.float)
    totalmass = 0
    for i in range(natoms):
        com += ccdata.atommasses[i] * ccdata.atomcoords[i]
        totalmass += ccdata.atommasses[i]

    com /= totalmass

    for i in range(natoms):
        ccdata.atomcoords[i] -= com


def alignmolecules(ccdata1, ccdata2):
    """Align two molecules to minimize RMSD"""

    rotationmatrix = _findrotationmatrix(ccdata1, ccdata2)

    for i in range(ccdata2.natom):
        ccdata2.atomcoords[i] = np.transpose(
            np.dot(rotationmatrix, np.transpose(ccdata2.atomcoords[i])))


def _findrotationmatrix(ccdata1, ccdata2):
    """Find rotation matrix that aligns two molecules"""
    natoms = ccdata1.natom
    J = np.zeros((3, 3), dtype=np.float)

    for i in range(natoms):
        J += np.outer(ccdata1.atomcoords[i], ccdata2.atomcoords[i])

    U, s, V = np.linalg.svd(J)

    R = np.transpose(np.dot(V, np.transpose(U)))

    return R


def printcoords(ccdata):
    """Quick print"""
    print(ccdata.natom, '\n')
    atomcoords = ccdata.atomcoords.tolist()
    atomnos = ccdata.atomnos.tolist()

    #atomgeoms = zip(atomnos, atomcoords)
    for i in range(len(atomcoords)):
        atomcoords[i].insert(0, atomnos[i])

    for atom in atomcoords:
        print("%s %10.8f %10.8f %10.8f" % tuple(atom))

def main(opts):
    rmsd(opts.xyzfile1, opts.xyzfile2)
