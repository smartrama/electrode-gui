import numpy as np
import scipy.ndimage.interpolation as sci
import time

# Takes in CT image data (as a numpy array), a downsampling factor, and camera angles of theta and phi.

def ct2mip(ct, dsf, theta, phi):
	ct = ct[::dsf,::dsf,::dsf]
	ct = sci.rotate(ct, -theta, axes=(0,1), reshape=False)
	ct = sci.rotate(ct, -phi, axes=(0,2), reshape=False)
	mip = np.amax(ct, axis=0)
	mip = np.rot90(mip)
	return mip