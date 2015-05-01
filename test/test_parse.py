"""Tests for parse.py"""

import unittest
#from ddt import ddt, data

from qcl import parse

import numpy as np


class ParseTest(unittest.TestCase):
    """Tests for parse.py"""

    def test_xyzfile(self):
        """Test for parse.xyzfile()"""
        ccdata = parse.xyzfile('../data/xyz/water.xyz')

        self.assertEqual(ccdata.charge, 0)
        self.assertEqual(ccdata.mult, 1)
        self.assertEqual(len(ccdata.atomnos), 3)

        atomnos = np.array([8, 1, 1])
        self.assertTrue(np.array_equal(ccdata.atomnos, atomnos))

        atomcoords = np.array([
            [-5.35740, 2.09256, 0.00000],
            [-4.38740, 2.09256, 0.00000],
            [-5.68073, 1.66625, -0.80909]])
        self.assertTrue(np.array_equal(ccdata.atomcoords, atomcoords))

    def test_xyzfile_ccdata_xyz(self):
        """Test for parse.xyzfile()"""
        ccdata = parse.xyzfile('../data/xyz/S+MeO.xyz', ccxyz=True)

        self.assertEqual(ccdata.charge, 0)
        self.assertEqual(ccdata.mult, 2)
        self.assertEqual(len(ccdata.atomnos), 13)

        atomnos = np.array([6, 8, 8, 6, 14, 1, 1, 1, 1, 6, 1, 1, 1])
        self.assertTrue(np.array_equal(ccdata.atomnos, atomnos))

        atomcoords = np.array([
            [-3.77578,  1.41262, -0.21447],
            [-2.58788,  2.06725, -0.31292],
            [-4.74823,  1.86911, -0.79440],
            [-3.94794,  0.18513,  0.64310],
            [-3.26032, -1.33907, -0.21050],
            [-1.82613, -1.25295, -0.50911],
            [-3.98211, -1.54172, -1.47550],
            [-3.48170, -2.50778,  0.65363],
            [-5.02928, -0.02357,  0.79011],
            [-1.46784,  1.77800,  0.43859],
            [-0.66178,  2.49212,  0.17276],
            [-1.10077,  0.75603,  0.23026],
            [-1.69461,  1.88618,  1.52073]])
        self.assertTrue(np.array_equal(ccdata.atomcoords, atomcoords))

        elements = ['C', 'O', 'O', 'C', 'Si', 'H', 'H',
                    'H', 'H', 'C', 'H', 'H', 'H']
        self.assertListEqual(ccdata.elements, elements)

        comment = '0 2\n'
        self.assertEqual(ccdata.comment, comment)

        filename = 'S+MeO.xyz'
        self.assertEqual(ccdata.filename, filename)

    def test_multixyzfile(self):
        """Test for parse.multixyzfile()"""
        ccdatas = parse.multixyzfile('../data/xyz/multi.xyz')

        self.assertEqual(ccdatas[0].charge, 1)
        self.assertEqual(ccdatas[0].mult, 2)
        self.assertEqual(len(ccdatas[0].atomnos), 13)

        atomnos = np.array([6, 8, 8, 6, 14, 1, 1, 1, 1, 6, 1, 1, 1])
        self.assertTrue(np.array_equal(ccdatas[0].atomnos, atomnos))

        atomcoords = np.array([
            [-3.77578,  1.41262, -0.21447],
            [-2.58788,  2.06725, -0.31292],
            [-4.74823,  1.86911, -0.79440],
            [-3.94794,  0.18513,  0.64310],
            [-3.26032, -1.33907, -0.21050],
            [-1.82613, -1.25295, -0.50911],
            [-3.98211, -1.54172, -1.47550],
            [-3.48170, -2.50778,  0.65363],
            [-5.02928, -0.02357,  0.79011],
            [-1.46784,  1.77800,  0.43859],
            [-0.66178,  2.49212,  0.17276],
            [-1.10077,  0.75603,  0.23026],
            [-1.69461,  1.88618,  1.52073]])
        self.assertTrue(np.array_equal(ccdatas[0].atomcoords, atomcoords))

        self.assertEqual(ccdatas[1].charge, 0)
        self.assertEqual(ccdatas[1].mult, 1)
        self.assertEqual(len(ccdatas[1].atomnos), 3)

        atomnos = np.array([8, 1, 1])
        self.assertTrue(np.array_equal(ccdatas[1].atomnos, atomnos))

        atomcoords = np.array([
            [-5.35740, 2.09256, 0.00000],
            [-4.38740, 2.09256, 0.00000],
            [-5.68073, 1.66625, -0.80909]])
        self.assertTrue(np.array_equal(ccdatas[1].atomcoords, atomcoords))

    def test_mopacoutputfile(self):
        """Test for prase.mopacoutputfile"""
        ccdata = parse.mopacoutputfile('../data/mop/mndo.out', nogeometry=True)

        # Calculated using 23.060548867 kcal/mol per eV (cclib conversion factor)
        scf_kcalmol = -44257.25147116261
        print(ccdata.scfenergies[0])
        print(scf_kcalmol)
        self.assertAlmostEqual(ccdata.scfenergies[0], scf_kcalmol, places=10)


if __name__ == '__main__':
    unittest.main()
