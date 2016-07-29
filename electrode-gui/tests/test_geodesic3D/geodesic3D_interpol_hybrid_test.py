import os
import numpy as np
import nibabel as nib
import math
import itertools
import time
import json
import sys
sys.path.append('/home/islamx/Documents/Litt_Lab/electrode-gui/electrode-gui/util')
from interpol import interpol
from geodesic3D import geodesic3D

### SET PATIENT ID ###
patient_id = 'HUP64'

preprocess_start = time.clock()
DATA_DIR = '/home/islamx/Documents/Litt_Lab/' + patient_id
mask = os.path.join('/home/islamx/Documents/Litt_Lab/' + patient_id, patient_id + '_brain_mask.nii.gz')
img = nib.load(mask)
mask = img.get_data()

with open('/home/islamx/Documents/Litt_Lab/electrode-gui/electrode-gui/tests/test_geodesic3D/geodesic3D_examples.json') as data_file:
	data = json.load(data_file)
A = tuple(data[patient_id]["1"]["A"])
B = tuple(data[patient_id]["1"]["B"])
C = tuple(data[patient_id]["1"]["C"])
D = tuple(data[patient_id]["1"]["D"])
print 'Preprocessing took: %s s'%((time.clock()-preprocess_start))

interpol_start = time.clock()
A2C = tuple(geodesic3D(A, C, mask))
B2D = tuple(geodesic3D(B, D, mask))

# Divide up sides into n electrodes.
sides = [A2C, B2D]
n = 8 # Number of electrodes
d = {}
for x in sides:
	dist = len(x)
	l = dist-1
	k = l/float(n-1) # Distance between electrodes
	electrodes = []
	i = 0
	if k.is_integer():
		while i <= l:
			electrodes.append(x[int(i)])
			i += k
	else:
		while True:
			if i >= l:
				electrodes.append(x[-1])
				break
			else:
				e, f = math.modf(i)
				f = int(f)
				inc = tuple(np.add(x[f],np.multiply(e,(np.subtract(x[f+1],x[f])))))
				electrodes.append(inc)
				i += k
	d[x] = electrodes

# Interpolate linearly between each side.
grid = []
grid.append(d[A2C])
for i in range(0,n):
	start = d[A2C][i]
	end = d[B2D][i]
	pairs = interpol(start, end, [], 1, n)
	j = 0
	while j < len(pairs.values()) - 3:
		grid.append((pairs.values()[j], pairs.values()[j+1], pairs.values()[j+2]))
		j += 3
grid.append(d[B2D])
grid = list(itertools.chain(*grid))
print 'Interpolation took: %s s'%((time.clock()-interpol_start))

# Begin post-processing (creating Nifti).
nib_start = time.clock()
radius = 2
seg_filename = '%s/%s_unburied_electrode_seg.nii.gz'%(DATA_DIR,patient_id)
seg = nib.load(os.path.expanduser(seg_filename))
seg_data = seg.get_data()

# Initialize the result 3D image matrix
res = np.zeros(seg_data.shape)

## -17 when mask, -35 when unburied
# Set the output file name
out_filename = seg_filename[:-35] + '%s_interpol.nii.gz'%patient_id
for v in grid:
	res[v[0]-radius:v[0]+radius,
		v[1]-radius:v[1]+radius,
		v[2]-radius:v[2]+radius] = 1
# Save res as new output result file
res_nifti = nib.Nifti1Image(res,seg.get_affine())
nib.save(res_nifti,os.path.expanduser(out_filename))
print 'Postprocessing (which includes creating the final NIfTI file) took: %s s'%((time.clock()-nib_start))