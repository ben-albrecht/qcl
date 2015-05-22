#!/usr/bin/env python3
# encoding: utf-8

from qcl.ccdata_xyz import ccData_xyz
from cclib.parser import ccopen


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


def distance(node, N, elements, visited=None):
    #TODO we need to track what has been visited and ability to disable certain paths
    dstmat = {key: 0 for key in elements}


    if N == 0:
        dstmat[node.element] = 1
        return dstmat
    else:
        if visited is None:
            visited = []

        visited.append(node.index)

        if node.parent:
            if node.parent.index not in visited:
                tmp = distance(node.parent, N-1, elements, visited=visited)
                dstmat = {key: tmp[key]+dstmat[key] for key in elements}
        for child in node.children:
            if child.index not in visited:
                tmp = distance(child, N-1, elements, visited=visited)
                dstmat = {key: tmp[key]+dstmat[key] for key in elements}
        return dstmat


def build_distancematrix(node, elements, dmax, ignore=None):
    """Compute distance matrix up to dmax for a given Node"""
    # Create dictionary based on types of atoms present in molecule
    #distancematrix = {element: 0 for element in elements}
    distancematrix = []
    for dst in range(dmax):
        distancematrix.append(distance(node, dst, elements, visited=ignore))
    return distancematrix


def dict_equal(dict1, dict2):
    """Check if 2 dictionaries are equal"""
    return len(dict1) == len(dict2) == len(dict1.items() & dict2.items())


def dstmat_equal(dstmat1, dstmat2):
    """Check if 2 distance matrices are equal"""
    alldistances = [dict_equal(dstmat1[i], dstmat2[i]) for i in range(len(dstmat1))]
    return all(alldistances)


def main():
    """Goal: Identify first atom in product.out based on connectivity"""
    ccproduct = ccopen('product.out').parse()
    product = ccData_xyz(ccproduct.getattributes(), ccdataconvert=True)
    product.build_zmatrix()

    elements = set(product.elements)

    atom0 = NodeAtom(product, index=0)
    #atom0.children.pop(0)

    atom1 = NodeAtom(product, index=1)
    for child in [x for x in atom0.children if x.index == 0]:
        atom0.children.remove(child)

    #D0 = build_distancematrix(atom0, elements, 3, ignore=[1])
    D1 = build_distancematrix(atom1, elements, 3, ignore=[0])

    ccr2 = ccopen('r2.out').parse()
    r2 = ccData_xyz(ccr2.getattributes(), ccdataconvert=True)
    r2.build_zmatrix()

    print(r2.connectivity)
    print(product.connectivity)
    atom1.nodeprint()

    for i in range(len(r2.atomnos)):
        atomtree = NodeAtom(r2, index=i)
        distancematrix = build_distancematrix(atomtree, elements, 3)

        if dstmat_equal(distancematrix, D1):
            print('Atom 1 found')
            break

    print('Atom 1 in reactant:')
    for dst in distancematrix:
        print(dst)

    print('Atom 1 in product:')
    for dst in D1:
        print(dst)

if __name__ == '__main__':
    main()
