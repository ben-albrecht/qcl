#!/usr/bin/env python3
# encoding: utf-8

from qcl.ccdata_xyz import ccData_xyz
from cclib.parser import ccopen
import numpy as np


class NodeAtom(object):

    def __init__(self, ccdata_xyz, index=0, parent=None, visited=None):
        """Create connectivity tree of ccdata_xyz starting at index"""

        if visited is None:
            visited = []

        self.index = index
        self.parent = parent
        self.element = ccdata_xyz.elements[index]
        self.children = []
        conn = ccdata_xyz.connectivity

        neighbors = [idx for idx in range(len(conn)) if conn[idx] == self.index]
        neighbors.append(conn[self.index])

        visited.append(index)

        neighbors = [x for x in neighbors if x not in visited]

        for i in neighbors:
            self.children.append(NodeAtom(ccdata_xyz, index=i, parent=self, visited=visited))

    def nodeprint(self):
        print('Node:', self)
        if self.children:
            print('Children:')
            for child in self.children:
                child.nodeprint()

    def __str__(self):
        return ' '.join([str(self.index), self.element])


class AdjacencyMatrix(object):
    """ Stores self.matrix which is a list of dictionaries which notates the
        number of each element for a given number of nodes away."""

    def __init__(self, node, elements, dmax, ignores=None):

        self.node = node
        self.elements = elements
        self.dmax = dmax

        # ignores nodes of indices in ignores list
        if ignores:
            self.ignores = ignores
        else:
            self.ignores = []

        # Build self.matrix
        self.build_matrix()

    def build_matrix(self):
        self.matrix = []
        for N in range(self.dmax):
            self.matrix.append(self._countnodes(N, visited=self.ignores))

    def _countnodes(self, N, node=None, visited=None):
        """Generate dictionary counting number of each element N nodes away from node"""
        adjmat = {key: 0 for key in self.elements}

        if not node:
            node = self.node

        if N == 0:
            adjmat[node.element] = 1
            return adjmat
        else:
            if visited is None:
                visited = []

            visited.append(node.index)

            if node.parent:
                if node.parent.index not in visited:
                    tmp = self._countnodes(N-1, node=node.parent, visited=visited)
                    adjmat = {key: tmp[key]+adjmat[key] for key in self.elements}
            for child in node.children:
                if child.index not in visited:
                    tmp = self._countnodes(N-1, node=child, visited=visited)
                    adjmat = {key: tmp[key]+adjmat[key] for key in self.elements}
            return adjmat

    def identifyatom(self, ccdata, matched=None):
        """ Identify this atom in a ccdata object"""

        if matched == None:
            matched = []

        for i in [x for x in range(len(ccdata.atomnos)) if x not in matched]:
            atomtree = NodeAtom(ccdata, index=i)
            adjmat = AdjacencyMatrix(atomtree, self.elements, 3)
            if self._adjmat_equal(adjmat):
                return atomtree.index
        return None

    def _adjmat_equal(self, adjmat):
        """Check if another distance matrix is equal to this one"""
        alldistances = [self._dict_equal(self.matrix[i], adjmat.matrix[i]) for i in range(len(self.matrix))]
        return all(alldistances)

    def _dict_equal(self, dict1, dict2):
        """Check if 2 dictionaries are equal"""
        return len(dict1) == len(dict2) == len(dict1.items() & dict2.items())


def indexmatch(ccproduct, productindex, ccreactant, ignores=None, matched=None):
    """Find the index of an atom from product in reactant"""

    ccproduct.build_zmatrix()
    ccreactant.build_zmatrix()
    # Build atom tree for atom at productindex
    atomgraph = NodeAtom(ccproduct, index=productindex)

    # Assume ignores is atom 0 if we start with atom 1 and vice versa
    if ignores == None:
        ignores = []

    if matched == None:
        matched = []

    # Build AdjacencyMatrix for atom 1
    adjmat = AdjacencyMatrix(atomgraph, set(ccproduct.elements), 3, ignores=ignores)

    # DEBUG
    #for adj in adjmat.matrix:
    #    print(adj)

    # Identify atom 1 from product in reactant
    reactantindex = adjmat.identifyatom(ccreactant, matched=matched)

    return reactantindex


def reactantinproduct(reactant, product, P2Ridx):
    """Update reactant internal coordinates within product structure"""

    coords = product.atomcoords[-1]
    atomnos = product.atomnos
    elements = product.elements
    newcoords = np.array([])
    newatomnos = []
    newelements = []

    # First: Sort product atoms in relation to reactant atoms:
    for i in P2Ridx:
        newcoords = np.append(newcoords, coords[i])
        newatomnos.append(atomnos[i])
        newelements.append(elements[i])

    for i in [x for x in range(len(coords)) if x not in P2Ridx]:
        newcoords = np.append(newcoords, coords[i])
        newatomnos.append(atomnos[i])
        newelements.append(elements[i])

    newcoords = newcoords.reshape(len(coords), 3)

    product.atomcoords = [newcoords]
    product.atomnos = newatomnos
    product.elements = newelements
    #product.build_xyz()
    #product.print_xyz()

    product.build_zmatrix()
    # FIXME: Currently a hack, and orientation / bond angle is incorrect
    product.distances[8] += 2.0
    reactant.build_zmatrix()

    for i in range(len(reactant.atomnos)):
        product.distances[i] =  reactant.distances[i]
        product.angles[i] = reactant.angles[i]
        product.dihedrals[i] = reactant.dihedrals[i]

    product.print_gzmat()
    #product.build_xyz()
    #reactant.build_xyz()
    #product.print_xyz()
    return

def main():
    """Goal: Identify first atom in product.out based on connectivity"""

    # Parse product output and generate z-matrix
    product = ccopen('product.out').parse()
    ccproduct = ccData_xyz(product.getattributes())
    ccproduct.build_zmatrix()
    shift = 2.0
    ccproduct.distances[1] += shift
    ccproduct.build_xyz()
    #ccproduct.print_xyz()

    reactant = ccopen('r1.out').parse()
    ccreactant = ccData_xyz(reactant.getattributes())

    # Shitty design here, but not sure what else to do yet...
    P2Ridx = [None]*len(ccreactant.atomnos)
    matched = []

    for i in range(len(ccproduct.atomnos)):
        match = indexmatch(ccproduct, i, ccreactant, ignores=[1], matched=matched)
        if match is not None:
            P2Ridx[match] = i
            matched.append(match)


    reactantinproduct(ccreactant, ccproduct, P2Ridx)


if __name__ == '__main__':
    main()
