import numpy as np
import scipy.ndimage.interpolation as sci
import time

# Takes in CT image data (as a numpy array), a downsampling factor, and camera angles of theta and phi.

def ct2mip(ct, dsf, theta, phi):
	ct = ct[::dsf,::dsf,::dsf]
	start = time.clock()
	ct = sci.rotate(ct, -theta, axes=(0,1))
	ct = sci.rotate(ct, -phi, axes=(0,2))
	print 'Rotating took: %s s' % ((time.clock()-start))
	start_2 = time.clock()
	mip = np.amax(ct, axis=0)
	mip = np.rot90(mip)
	print 'Making MIP took: %s s' % ((time.clock()-start_2))
	return mip