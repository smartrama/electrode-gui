#!/usr/bin/python
''' This script tests geodesic2D.py utility function that returns the optimal path from one point to another on a 2D cost mask (e.g. brain mask). Note
    that this is a path and not an interpolation of electrodes along a path.

It takes as inputs two sample voxel coordinates representing the starting and ending points on a mask surface as well as the mask itself used to determine the path on which to traverse. It outputs the path as determined
    by graph traversal using Djikstra's algorithm.
'''

from os import path
import sys
sys.path.append(path.abspath('../../util'))
import cProfile

import unittest
import time

import numpy as np
import scipy.io as sio
import nibabel as nib
import matplotlib.pyplot as plt
import json

from geodesic2D import geodesic2D

__version__ = '0.0'
__author__ = 'Lohith Kini'
__email__ = 'lkini@mail.med.upenn.edu'
__copyright__ = "Copyright 2016, University of Pennsylvania"
__credits__ = ["Xavier Islam","Sandhitsu Das", "Joel Stein",
                "Kathryn Davis"]
__license__ = "MIT"
__status__ = "Development"

DATA_DIR = 'data/'

class TestGeodesicDistance(unittest.TestCase):
    """Unit test for measuring the geodesic distance between two points
        on the mask.

    Tests different forms of masks (binary) and sample points on the masks
    """

    def load_data(self):
        """returns the JSON data as a dictionary

        Takes in coordinates from 3 sample test cases saved in
            geodesic2D_examples.json file located in the same folder as this
            unit test.
        """
        with open('geodesic2D_examples.json') as data_file:
            data = json.load(data_file)
        # Set filepath to data
        global DATA_DIR
        DATA_DIR = str(data['DATA_DIR'])
        return data

    def test_cases(self,case_id):
        """returns True or False depending on the success of creating a
            synthetic path on a 2D mask.

        @param case_id: Sample test case ID
        @type case_id: string
        @rtype: bool
        """
        try:
            preprocess_start = time.clock()
            # Load the test coordinates
            data = self.load_data()

            # Load the mask MAT file
            mask = sio.loadmat(DATA_DIR + case_id + '.mat')

            # Initialize the result 2d path matrix
            res = mask['mask']

            # Set the output file name
            out_filename = DATA_DIR + '%s_geodesic2D_path.mat'%case_id

            # Interpolate on the 2-3 corners
            start = tuple(data[case_id]["1"]["A"])
            end = tuple(data[case_id]["1"]["B"])

            print 'Preprocessing took: %s ms'%(
                (time.clock()-preprocess_start)*1000
                )

            path_traversal_start = time.clock()

            path_traversal = geodesic2D(start,
                            end,
                            mask['mask']
                            )

            print 'Geodesic 2D path computation took: %s ms'%(
                (time.clock()-path_traversal_start)*1000
                )

            mat_start = time.clock()
            # Create spheres of radius
            for point in path_traversal:
                res[point] = 2

            # Save res as new output result file
            sio.savemat(
                path.expanduser(out_filename),
                {
                    'res':res
                }
                )

            print 'Postprocessing took: %s ms'%(
                (time.clock()-mat_start)*1000
                )

            # Plot resulting image
            plt.imshow(res)
            plt.show()

            return True
        except Exception, e:
            print str(e)
            return False

    def test_geodesic2D_test_1(self):
        """Unit test for patient geodesic2D_test_1."""
        case_id = 'geodesic2D_test_1'
        return self.test_cases(case_id)

    def test_geodesic2D_test_2(self):
        """Unit test for patient geodesic2D_test_2."""
        case_id = 'geodesic2D_test_2'
        return self.test_cases(case_id)

    def test_geodesic2D_test_3(self):
        """Unit test for patient geodesic2D_test_3."""
        case_id = 'geodesic2D_test_3'
        return self.test_cases(case_id)

    def runTest(self):
        """Required method for running a unit test."""
        return self.test_geodesic2D_test_1()


if __name__ == '__main__':
    ti = TestGeodesicDistance()
    ti.test_geodesic2D_test_3()
