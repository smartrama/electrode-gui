'''
This script tests interpol.py utility function that interpolates all electrode grids in a strip or grid configuration. It 
takes as inputs three sample voxel coordinates representing the oriented corners of the grid as well as the path to the 
electrode segmentation file to use to map the interpolation.
'''

from os import path
import sys
sys.path.append(path.abspath('../util'))

import unittest
import nibabel as nib

from util import interpol1

class TestInterpolation(unittest.TestCase):
	def test_HUP64(self):
		patient_id = 'HUP64'
		seg_filename = '~/gdrive/RAM_GUI/electrode-gui/data/%s_unburied_electrode_seg.nii.gz'%patient_id
		out_filename = seg_filename[:-35] + '%s_interpol.nii.gz'
		seg = nib.load(seg_filename)		
				
		pairs = interpol([],[],[],10)
		
		return True
