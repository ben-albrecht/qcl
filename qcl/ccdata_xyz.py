""" Class definition of ccData_xyz, a child class of cclib's ccData"""
from __future__ import print_function
from __future__ import division

import math
from numpy import sin, cos, pi
from numpy.linalg import norm
import numpy as np
# Suppress scientific notation printouts and change default precision
np.set_printoptions(precision=4)
np.set_printoptions(suppress=True)

try:
    from cclib.parser.data import ccData
    from cclib.parser.utils import PeriodicTable
except ImportError:
    print("Failed to load cclib!")
    raise


class ccData_xyz(ccData):
    """
    ccData subclass for xyzfiles
    TODO: Checks for previous steps before continuing,
    i.e. check for dist_matrix before building conn_vector

    Includes some hot new attributes and class methods
    """

    def __init__(self, attributes={}):
        """Adding some new attributes for xyzfiles"""

        self.newcoords = None
        self.distancematrix = None

        # Internal Coordinate Connectivity
        self.connectivity = None
        self.angleconnectivity = None
        self.dihedralconnectivity = None

        # Internal Coordinates
        self.distances = None
        self.angles = None
        self.dihedrals = None

        self._attrtypes['comment'] = str
        self._attrlist.append('comment')
        self._attrtypes['filename'] = str
        self._attrlist.append('filename')
        self._attrtypes['elements'] = list
        self._attrlist.append('elements')
        #self._attrtypes['distancematrix'] = np.ndarray
        #self._attrlist.append('distancematrix')
        #self._attrtypes['connectivity'] = list
        #self._attrlist.append('connectivity')

        super(ccData_xyz, self).__init__(attributes=attributes)

    def _build_distance_matrix(self):
        """Build distance matrix between all atoms
           TODO: calculate distances only as needed"""
        coords = self.atomcoords
        self.distancematrix = np.zeros((len(coords), len(coords)))
        for i in range(len(coords)):
            for j in [x for x in range(len(coords)) if x > i]:
                self.distancematrix[i][j] = norm(coords[i] - coords[j])
                self.distancematrix[j][i] = self.distancematrix[i][j]

    def print_distance_matrix(self):
        """Print distance matrix in formatted form"""

        # Title
        print("\nDistance Matrix")

        # Row Indices
        for i in range(len(self.distancematrix)):
            print("%3d" % i, end="  ")

        print("\n", end="")
        idx = 0
        for vector in self.distancematrix:

            # Column indices
            print(idx, end=" ")

            # Actual Values
            for element in vector:
                if not element == 0:
                    print("%1.2f" % element, end=" ")
                else:
                    print("%1s" % " ", end="    ")
            print("\n", end="")
            idx += 1

    def build_zmatrix(self):
        """
       'Z-Matrix Algorithm'
        Build main components of zmatrix:
        Connectivity vector
        Distances between connected atoms (atom >= 1)
        Angles between connected atoms (atom >= 2)
        Dihedral angles between connected atoms (atom >= 3)
        """
        self._build_distance_matrix()

        # self.connectivity[i] tells you the index of 2nd atom connected to atom i
        self.connectivity = np.zeros(len(self.atomnos)).astype(int)

        # self.angleconnectivity[i] tells you the index of
        #    3rd atom connected to atom i and atom self.connectivity[i]
        self.angleconnectivity = np.zeros(len(self.atomnos)).astype(int)

        # self.dihedralconnectivity tells you the index of 4th atom connected to
        #    atom i, atom self.connectivity[i], and atom self.angleconnectivity[i]
        self.dihedralconnectivity = np.zeros(len(self.atomnos)).astype(int)

        # Starts with r1
        self.distances = np.zeros(len(self.atomnos))
        # Starts with a2
        self.angles = np.zeros(len(self.atomnos))
        # Starts with d3
        self.dihedrals = np.zeros(len(self.atomnos))

        atoms = range(1, len(self.atomnos))
        for atom in atoms:
            # For current atom, find the nearest atom among previous atoms
            distvector = self.distancematrix[atom][:atom]
            distmin = np.array(distvector[np.nonzero(distvector)]).min()
            nearestindices = np.where(distvector == distmin)[0]
            nearestatom = nearestindices[0]

            self.connectivity[atom] = nearestatom
            self.distances[atom] = distmin

            # Compute Angles
            if atom >= 2:
                atms = [0, 0, 0]
                atms[0] = atom
                atms[1] = self.connectivity[atms[0]]
                atms[2] = self.connectivity[atms[1]]
                if atms[2] == atms[1]:
                    for idx in range(1, len(self.connectivity[:atom])):
                        if self.connectivity[idx] in atms and not idx in atms:
                            atms[2] = idx
                            break

                self.angleconnectivity[atom] = atms[2]

                self.angles[atom] = self.calc_angle(atms[0], atms[1], atms[2])

            # Compute Dihedral Angles
            if atom >= 3:
                atms = [0, 0, 0, 0]
                atms[0] = atom
                atms[1] = self.connectivity[atms[0]]
                atms[2] = self.angleconnectivity[atms[0]]
                atms[3] = self.angleconnectivity[atms[1]]
                if atms[3] in atms[:3]:
                    for idx in range(1, len(self.connectivity[:atom])):
                        if self.connectivity[idx] in atms and not idx in atms:
                            atms[3] = idx
                            break

                self.dihedrals[atom] =\
                    self.calc_dihedral(atms[0], atms[1], atms[2], atms[3])
                if math.isnan(self.dihedrals[atom]):
                    # TODO: Find explicit way to denote undefined dihedrals
                    self.dihedrals[atom] = 0.0

                self.dihedralconnectivity[atom] = atms[3]

    def calc_angle(self, atom1, atom2, atom3):
        """Calculate angle between 3 atoms"""
        vec1 = self.atomcoords[atom2] - self.atomcoords[atom1]
        uvec1 = vec1 / norm(vec1)
        vec2 = self.atomcoords[atom2] - self.atomcoords[atom3]
        uvec2 = vec2 / norm(vec2)
        return np.arccos(np.dot(uvec1, uvec2))*(180.0/pi)

    def calc_dihedral(self, atom1, atom2, atom3, atom4):
        """
           Calculate dihedral angle between 4 atoms
           For more information, see:
               http://math.stackexchange.com/a/47084
        """
        # Vectors between 4 atoms
        b1 = self.atomcoords[atom2] - self.atomcoords[atom1]
        b2 = self.atomcoords[atom2] - self.atomcoords[atom3]
        b3 = self.atomcoords[atom4] - self.atomcoords[atom3]

        # Normal vector of plane containing b1,b2
        n1 = np.cross(b1, b2)
        un1 = n1 / norm(n1)

        # Normal vector of plane containing b1,b2
        n2 = np.cross(b2, b3)
        un2 = n2 / norm(n2)

        # un1, ub2, and m1 form orthonormal frame
        ub2 = b2 / norm(b2)
        um1 = np.cross(un1, ub2)

        # dot(ub2, n2) is always zero
        x = np.dot(un1, un2)
        y = np.dot(um1, un2)

        dihedral = np.arctan2(y, x)*(180.0/pi)
        if dihedral < 0:
            dihedral = 360.0 + dihedral
        return dihedral

    def print_gzmat(self):
        """Print Guassian Z-Matrix Format
        e.g.

        0  3
        C
        O  1  r2
        C  1  r3  2  a3
        Si 3  r4  1  a4  2  d4
        ...
        Variables:
        r2= 1.1963
        r3= 1.3054
        a3= 179.97
        r4= 1.8426
        a4= 120.10
        d4=  96.84
        ...
        """

        print('#', self.filename, "\n")
        print(self.comment)
        t = PeriodicTable()

        print(self.comment, end='')
        for i in range(len(self.atomnos)):
            idx = str(i+1)+" "
            if i >= 3:
                print(t.element[self.atomnos[i]], "",
                      self.connectivity[i]+1, " r"+idx,
                      self.angleconnectivity[i]+1, " a"+idx,
                      self.dihedralconnectivity[i]+1, " d"+idx.rstrip())
            elif i == 2:
                print(t.element[self.atomnos[i]], "",
                      self.connectivity[i]+1, " r"+idx,
                      self.angleconnectivity[i]+1, " a"+idx.rstrip())
            elif i == 1:
                print(t.element[self.atomnos[i]], "",
                      self.connectivity[i]+1, " r"+idx.rstrip())
            elif i == 0:
                print(t.element[self.atomnos[i]])

        print("Variables:")

        for i in range(1, len(self.atomnos)):
            idx = str(i+1)+"="
            if i >= 3:
                print("%s" % "r"+idx, "%6.4f" % self.distances[i])
                print("%s" % "a"+idx, "%6.2f" % self.angles[i])
                print("%s" % "d"+idx, "%6.2f" % self.dihedrals[i])
            elif i == 2:
                print("%s" % "r"+idx, "%6.4f" % self.distances[i])
                print("%s" % "a"+idx, "%6.2f" % self.angles[i])
            elif i == 1:
                print("%s" % "r"+idx, "%6.4f" % self.distances[i])

    def print_zmat(self):
        """Print Standard Z-Matrix Format"""
        #TODO

        """
        0 1
        O
        O 1 1.5
        H 1 1.0 2 120.0
        H 2 1.0 1 120.0 3 180.0
        """

    def build_xyz(self):
        """ Build xyz representation from z-matrix"""
        self.newcoords = np.zeros((len(self.atomcoords), 3))
        for i in range(len(self.atomcoords)):
            self.newcoords[i] = self.calc_position(i)
        self.atomcoords = self.newcoords

    def calc_position(self, i):
        """Calculate position of another atom based on internal coordinates"""

        if i > 1:
            j = self.connectivity[i]
            k = self.angleconnectivity[i]
            l = self.dihedralconnectivity[i]

            # Prevent doubles
            if k == l and i > 0:
                for idx in range(1, len(self.connectivity[:i])):
                    if self.connectivity[idx] in [i, j, k] and not idx in [i, j, k]:
                        l = idx
                        break

            avec = self.newcoords[j]
            bvec = self.newcoords[k]

            dst = self.distances[i]
            ang = self.angles[i] * pi / 180.0

            if i == 2:
                # Third atom will be in same plane as first two
                tor = 90.0 * pi / 180.0
                cvec = np.array([0, 1, 0])
            else:
                # Fourth + atoms require dihedral (torsional) angle
                tor = self.dihedrals[i] * pi / 180.0
                cvec = self.newcoords[l]

            v1 = avec - bvec
            v2 = avec - cvec

            n = np.cross(v1, v2)
            nn = np.cross(v1, n)

            n /= norm(n)
            nn /= norm(nn)

            n *= -sin(tor)
            nn *= cos(tor)

            v3 = n + nn
            v3 /= norm(v3)
            v3 *= dst * sin(ang)

            v1 /= norm(v1)
            v1 *= dst * cos(ang)

            position = avec + v3 - v1

        elif i == 1:
            # Second atom dst away from origin along Z-axis
            j = self.connectivity[i]
            dst = self.distances[i]
            position = np.array([self.newcoords[j][0] + dst, self.newcoords[j][1], self.newcoords[j][2]])

        elif i == 0:
            # First atom at the origin
            position = np.array([0, 0, 0])

        return position

    def print_xyz(self):
        """Print Standard XYZ Format"""
        if not self.newcoords:
            self.build_xyz()

        print(len(self.newcoords))

        if self.comment:
            print(self.comment, end='')
        else:
            print(self.filename, end='')

        atomcoords = [x.tolist() for x in self.newcoords]
        for i in range(len(atomcoords)):
            atomcoords[i].insert(0, self.elements[i])

        for atom in atomcoords:
            print("  %s %10.5f %10.5f %10.5f" % tuple(atom))
