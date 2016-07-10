#!/usr/bin/python
''' This script tests interpol.py utility function that interpolates all electrode grids in a strip or grid configuration.

It takes as inputs three sample voxel coordinates representing the oriented corners of the grid as well as the path to the electrode segmentation file to use to map the interpolation.
'''

__version__ = '0.1'
__author__ = 'Lohith Kini'

from os import path
import sys
sys.path.append(path.abspath('../util'))

import unittest
import numpy as np
import nibabel as nib
import json

from interpol import interpol

# Set filepath to data
DATA_DIR = '~/Documents/Litt_Lab/HUP65'


class TestInterpolation(unittest.TestCase):
    """Unit test for interpolation on grids and strips.

    Tests different strips and grids for 5 different sample patients with both strips and grids using the util.interpol module.
    """

    def load_data(self):
        """returns the JSON data as a dictionary

        Takes in coordinates and grid size from 5 sample patients saved in test_coords.json file located in the same folder as this unit test.
        """
        with open('test_coords.json') as data_file:
            data = json.load(data_file)
        return data

    def test_patient(self,patient_id):
        """returns True or False depending on the success of creating a synthetic electrode interpolation NIfTI file.

        @param patient_id: Sample patient ID
        @type patiend_id: string
        @rtype: bool
        """
        try:
            # Load the test coordinates
            data = self.load_data()

            # Load the segmentation file
            seg_filename = '%s/%s_unburied_electrode_seg.nii.gz'%(DATA_DIR,patient_id)
            seg = nib.load(path.expanduser(seg_filename))
            seg_data = seg.get_data()

            # Initialize the result 3d image matrix
            res = np.zeros(seg_data.shape)

            # Set the output file name
            out_filename = seg_filename[:-35] + '%s_interpol.nii.gz'%patient_id

            # Interpolate on the 2-3 corners
            grid = data[patient_id]["1"]["grid_config"]
            M = int(grid.split('x')[0])
            N = int(grid.split('x')[1])
            radius = 0.2 * 10
            pairs = interpol(data[patient_id]["1"]["A"],
                            data[patient_id]["1"]["B"],
                            data[patient_id]["1"]["C"],
                            M,N)

            # Create spheres of radius
            for k,v in pairs.items():
                res[v[0]-radius:v[0]+radius,
                    v[1]-radius:v[1]+radius,
                    v[2]-radius:v[2]+radius] = 1

            # Save res as new output result file
            res_nifti = nib.Nifti1Image(res,seg.get_affine())
            nib.save(res_nifti,path.expanduser(out_filename))

            return True
        except Exception, e:
            print str(e)
            return False

    def test_HUP64(self):
        """Unit test for patient HUP64."""
        patient_id = 'HUP64'
        return self.test_patient(patient_id)

    def test_HUP65(self):
        """Unit test for patient HUP65."""
        patient_id = 'HUP65'
        return self.test_patient(patient_id)

    def runTest(self):
        """Required method for running a unit test."""
        return self.test_HUP64()


if __name__ == '__main__':
    ti = TestInterpolation()
    ti.test_HUP65()
