#!/usr/bin/env python
''' 

'''

from os import path
import sys
sys.path.append(path.abspath('../../util'))

import unittest
import time

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from mip2vox import mip2vox

__version__ = '0.0'
__author__ = 'Lohith Kini'
__email__ = 'lkini@mail.med.upenn.edu'
__copyright__ = "Copyright 2016, University of Pennsylvania"
__credits__ = ["Xavier Islam","Sandhitsu Das", "Joel Stein",
                "Kathryn Davis"]
__license__ = "MIT"
__status__ = "Development"

DATA_DIR = 'data/'

class TestCT2MIP(unittest.TestCase):
    """

    """

    def test_patients(self,patient_id,theta,phi):
        """

        """
        try:
            # Load the segmentation file
         	seg_filename = '%s/%s_unburied_electrode_seg.nii.gz'%(DATA_DIR, patient_id)
           	img = nib.load(path.expanduser(seg_filename))
           	ct_data = img.get_data()

           	vox = mip2vox(96, 93, theta, phi, ct_data)

           	print vox
    		
        	return True
       	except Exception, e:
           	print str(e)
           	return False

    def test_ct2mip_test_1(self):
        """Unit test for patient HUP64."""
        patient_id = 'HUP64'
        theta = 135
        phi = 45
        return self.test_patients(patient_id, theta, phi)

    def test_ct2mip_test_2(self):
        """Unit test for patient HUP65."""
        patient_id = 'HUP65'
        theta = 30
        phi = 60
        return self.test_patients(patient_id)

    def test_ct2mip_test_3(self):
        """Unit test for patient geodesic2D_test_3."""
        patient_id = 'HUP86'
        theta = 30
        phi = 60
        return self.test_patients(patient_id)

    def test_ct2mip_test_4(self):
        """Unit test for patient geodesic2D_test_3."""
        patient_id = 'HUP87'
        theta = 30
        phi = 60
        return self.test_patients(patient_id)

    def runTest(self):
        """Required method for running a unit test."""
        return self.test_ct2mip_test_1()


if __name__ == '__main__':
    ti = TestCT2MIP()
    ti.test_ct2mip_test_1()
