import numpy as np
import scipy.ndimage.interpolation as sci

def ct2mip(ct, theta, phi):
	ct = sci.rotate(ct, -theta, axes=(0,1))
	ct = sci.rotate(ct, -phi, axes=(0,2))

	mip = np.amax(ct, axis=0)
	mip = np.rot90(mip)
	return mip