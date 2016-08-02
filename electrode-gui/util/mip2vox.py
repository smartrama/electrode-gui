import numpy as np
import scipy.ndimage.interpolation as sci
import time
import matplotlib.pyplot as plt
import pdb

# Takes in MIP coordinates and returns 3D voxel coordinates.

def mip2vox(x, y, theta, phi, ct):
	start = time.clock()
	ct = sci.rotate(ct, -theta, axes=(0,1), reshape=False)
	ct = sci.rotate(ct, -phi, axes=(0,2), reshape=False)
	print 'Rotating took: %s s' % ((time.clock()-start))
	start_2 = time.clock()
	y_lim = ct.shape[2]
	ray = list(ct[::,x,y_lim-y])
	z = ray.index(max(ray))
	print 'Finding max took: %s s' % ((time.clock()-start_2))
	plt.imshow(np.rot90(ct[z,::,::]))
	plt.show()
	vox = (z, x, y_lim-y)
	return vox