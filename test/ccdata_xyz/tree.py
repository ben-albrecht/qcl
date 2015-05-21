#!/usr/bin/env python3
# encoding: utf-8

from qcl.ccdata_xyz import ccData_xyz
from cclib.parser import ccopen


class NodeAtom(object):

    def __init__(self, ccdata_xyz, index=0, parent=None, visited=[]):
        """Create connectivity tree of ccdata_xyz starting at index"""
        self.index = index
        self.parent = parent
        self.element = ccdata_xyz.elements[index]
        self.children = []
        conn = ccdata_xyz.connectivity

        neighbors = []
        if conn[index] not in visited:
            neighbors.append(conn[index])

        neighbors.extend([atm for atm in range(len(conn)) if not atm in visited and conn[atm] == index])

        visited.append(index)

        for i in neighbors:
            self.children.append(NodeAtom(ccdata_xyz, index=i, parent=self.index, visited=visited))

    def nodeprint(self):
        print('Node:', self.index)
        if self.children:
            print('Children:')
            for child in self.children:
                child.nodeprint()


def distance(node, N, elements):
    dstmat = {key: 0 for key in elements}
    if N == 0:
        dstmat[node.element] = 1
        return dstmat
    else:
        if node.parent:
            tmp = distance(node.parent, N-1, elements)
            dstmat = {key: tmp[key]+dstmat[key] for key in elements}
        for child in node.children:
            tmp = distance(child, N-1, elements)
            dstmat = {key: tmp[key]+dstmat[key] for key in elements}
        return dstmat


def build_distancematrix(node, elements, dmax):
    """Compute distance matrix up to dmax for a given Node"""
    # Create dictionary based on types of atoms present in molecule
    #distancematrix = {element: 0 for element in elements}
    distancematrix = []
    for dst in range(dmax):
        distancematrix.append(distance(node, dst, elements))
    return distancematrix


def dict_equal(dict1, dict2):
    """Check if 2 dictionaries are equal"""
    return len(dict1) == len(dict2) == len(dict1.items() & dict2.items())


def main():
    """Goal: Identify first atom in product.out based on connectivity"""
    ccproduct = ccopen('product.out').parse()
    product = ccData_xyz(ccproduct.getattributes(), ccdataconvert=True)
    product.build_zmatrix()

    elements = set(product.elements)

    atom0 = NodeAtom(product, index=0)
    atom0.children.pop(0)

    atom1 = NodeAtom(product, index=1)
    atom0.children.pop(0)

    D0 = build_distancematrix(atom0, elements, 3)
    D1 = build_distancematrix(atom1, elements, 3)

    ccr2 = ccopen('r2.out').parse()
    r2 = ccData_xyz(ccr2.getattributes(), ccdataconvert=True)
    r2.build_zmatrix()
    print(r2.connectivity)
    for i in range(len(r2.atomnos)):
        atomtree = NodeAtom(r2, index=i)
        distancematrix = build_distancematrix(atomtree, elements, 3)
        atomtree.nodeprint()

        print('D', i)
        for dst in distancematrix:
            print(dst)

    print('Product D1')
    for dst in D0:
        print(dst)

    print('Product D1')
    for dst in D1:
        print(dst)
if __name__ == '__main__':
    main()
