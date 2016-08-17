import numpy as np
import time
from PIL import Image

# Takes in CT image data (as a numpy array), a downsampling factor, and camera angles of theta and phi.

def ct2mip(ct, dsf, theta, phi):
	ct = ct[::dsf,::dsf,::dsf]
	for i in xrange(ct.shape[2]):
	    layer = ct[::,::,i]
	    ct[::,::,i] = (Image.fromarray(layer).rotate(-theta, resample=Image.NEAREST))
	for j in xrange(ct.shape[1]):
		layer = ct[::,j,::]
		ct[::,j,::] = (Image.fromarray(layer).rotate(-phi, resample=Image.NEAREST))
	mip = np.amax(ct, axis=0)
	mip = np.rot90(mip)
	return mip