import numpy as np
import time
from PIL import Image

# Takes in CT image data (as a numpy array), a downsampling factor, and camera angles of theta and phi.

def ct2mip(ct, dsf, theta, phi):
	ct = ct[::dsf,::dsf,::dsf]
	for i in xrange(ct.shape[2]):
	    layer = ct[::,::,i]
	    try:
	    	im = Image.fromarray(layer)
	    except TypeError:
	    	im = Image.fromarray(layer.astype('uint8'))
	    ct[::,::,i] = im.rotate(-theta, resample=Image.BILINEAR)
	for j in xrange(ct.shape[1]):
		layer = ct[::,j,::]
		try:
			im = Image.fromarray(layer)
		except TypeError:
			im = Image.fromarray(layer.astype('uint8'))
		ct[::,j,::] = im.rotate(-phi, resample=Image.BILINEAR)
	mip = np.amax(ct, axis=0)
	mip = np.rot90(mip)
	return mip