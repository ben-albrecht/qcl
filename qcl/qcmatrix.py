"""Currently unused"""
import numpy as np
import StringIO
import sys
import os
import re
import argparse
import math

class QCMatrix(object):
    """
    QCMatrix Class Constructors
    """
    def __init__(self, filename):
        """
        Initialize from filename -> no matrices loaded yet

        >>> qmat = QCMatrix('test.out')
        """
        with open(filename, 'r') as handle:
            self.lines = handle.readlines()
            self.NBasis = self._get_basis()
            self.matrix = []



    @classmethod
    def FromTitleOcc(cls, filename, title, occurrence):
        """
        Initialize from filename, title of matrix, and the Nth occurrence
        """
        c = cls(filename) # same as: c = QCMatrix(filename)
        cls.linenum = None
        cls.title = title
        cls.occurrence = occurrence
        c._get_next_matrix()
        return c


    @classmethod
    def FromTitleLineNum(cls, filename, title, linenum):
        """
        Initialize from filename, title of matrix, that occurs after line number

        >>> qmat = QCMatrix.FromTitleLineNum('test.out', 'Alpha Density Matrix', 1)
        """
        c = cls(filename) # same as: c = QCMatrix(filename)
        cls.linenum = linenum
        cls.title = title
        cls.occurrence = None
        c._get_next_matrix()
        return c
        pass


    @classmethod
    def FromLineNum(cls, filename, linenum):
        """
        Initialize from filename, and the next matrix after line number

        >>> qmat = QCMatrix.FromLineNum('test.out', 1)
        """
        c = cls(filename) # same as: c = QCMatrix(filename)
        cls.linenum = linenum
        c._get_next_matrix()
        return c


    """
    QCMatrix Class Methods
    """
    def _get_basis(self):
        """
        Find NBasis using regex in file
        """
        num = 0
        while num < len(self.lines):
            num += 1
            line = self.lines[num]
            if "basis functions" in line:
                bas_shls = [int(s) for s in line.split() if s.isdigit()]
                #print bas_shls
                print("NBasis = ", bas_shls[1])
                if int(bas_shls[1]) < 7:
                    print("Basis is too small for this script to work")
                    exit(1)
                return int(bas_shls[1])

    def _matlines(self, cols):
        """
        Calculate number of lines in file a matrix spans,
        depending on self.NBasis and columns of matrix
        """
        return int((math.ceil(float(NBasis)/cols))*(NBasis+1))


    def _get_next_matrix(self):
        # Regex for 7 column wide matrix index labels
        self.regex_column_ids = re.compile(r'\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)')
        # Regex for 7 column wide matrix in Q-Chem
        regex_row_values = re.compile(r'\s*(\d+)\s*([\+-]?\d+\.?\d+)\s*([\+-]?\d+\.?\d+)\s*([\+-]?\d+\.?\d+)\s*([\+-]?\d+\.?\d+)\s*([\+-]?\d+\.?\d+)\s*([\+-]?\d+\.?\d+)')

        found_matrix = False

        if self.title is None and self.occurrence is None:
            # Get next matrix after self.linenum
            print("Finding next matrix after line ", self.linenum)
            num = self.linenum
        elif self.linenum is None:
            # Get self.occurrence'th matrix named self.title
            print("Finding occurrence ", self.occurrence, "of matrix named ", self.title)
            num = 1
            occ = 0
            while num < len(self.lines):
                line = self.lines[num-1]
                if self.title in line:
                    occ += 1
                    if occ == self.occurrence:
                        break
                    elif num == (len(self.lines) - 1):
                        print("Error: only ", occ, " occurrences of ", self.title, " matrix found in file")
                        exit(1)
                else:
                    num += 1
        elif self.occurrence is None:
            # Get matrix named self.title after self.linenum
            print("Finding matrix named ", self.title, " after line ", self.linenum)
            # Start at line from input
            num = self.linenum
            # Skip to line right before matrix with name
            while num < len(self.lines):
                line = self.lines[num-1]
                if self.title in line:
                    break
                else:
                    num += 1
        else:
            # Crash
            print("Internal error with _get_next_matrix()")
            exit(1)

        # Main Loop of _get_next_matrix:
        while num < len(self.lines):
            line = self.lines[num-1]
            line = line.strip()

            # Lets find the matrix
            if self._test_if_col_header(line):
                column_ids = self._extract_column_ids(line)
                # The matrix has been found
                found_matrix = True
                print("Loading Matrix ", self.lines[num - 2], "from line ", num - 1)
                self.title = self.lines[num - 2]
                num += 1
                # Now lets extract the actual values from the matrix
                while num < len(self.lines):
                    line = self.lines[num-1]
                    row_values = regex_row_values.match(line)
                    if row_values:
                        row_index  = int(row_values.group(1))
                        row_values = [float(v) for v in row_values.groups()[1:]]
                        if len(self.matrix) >= row_index:
                            self.matrix[row_index - 1].extend(row_values)
                        else:
                            self.matrix.append(row_values)
                    else:
                        if self._test_if_col_header(line):
                            column_ids = self._extract_column_ids(line)
                        else:
                            break
                    num += 1
            elif found_matrix:
                break
            else:
                num += 1

        self.matrix = np.array(self.matrix)

    def _get_next_matrix_new(self):
        self.matrix = None

    def _test_if_col_header(self, line):
        match = self.regex_column_ids.match(line)
        if match:
            return True
        return False

    def _extract_column_ids(self, line):
        return [int(c) for c in line.strip().split()]

    def _test_if_row_line(self, line):
        return False

    def _extract_row_values(self, line):
        return []

    def __str__(self):
        """
        This magic symbol str overrides the string method so now I can straight up print my object
        Boom bitch

        >>> print(qmat)
        >>> s = str(qmat)
        """
        s = StringIO.StringIO()
        print >> s, self.matrix
        return s.getvalue()

    def plot(self, oname=None, **kwargs):
        import matplotlib
        matplotlib.use('Agg')  # Or any other X11 back-end
        import matplotlib.pyplot as plt
        self.plt = plt

        smap = plt.matshow(self.matrix, **kwargs)
        plt.colorbar(smap)
        plt.suptitle(self.title)
        if oname:
            plt.savefig(oname)

    def show(self, *args, **kwargs):
        print("*** Warning *** show() may not work remotely")
        self.plot(*args, **kwargs)
        self.plt.show()

"""

if __name__ == '__main__':
    opts = get_arguments()

    work = os.getcwd()
    oname = opts.ofile
    stub, ext  = os.path.splitext(oname)
    subdir = os.path.join(work, stub + '_plots')

    print "subdir: ", subdir
    if not os.path.exists(subdir): os.makedirs(subdir)

    fname = '%s/%s' % (work, opts.ofile)
    print "Q-Chem Output: ", fname

    with open(fname, 'r') as handle:

        lines = handle.readlines()
        NBasis = get_basis(lines)
        print "NBasis = ", NBasis

        num = 1
        while num < len(lines):
            line = lines[num-1]
            jump = line_jump(NBasis, lines, num)
            if jump > 0:
                print num-1
                #matrix = get_next_matrix(lines, num)
                num += jump
                print num-1
                break
            num += 1

        sys.exit()
        # need to feed get_next_matrix line_numbers and handle?

"""
