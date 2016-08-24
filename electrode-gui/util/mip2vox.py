import numpy as np
from PIL import Image
import time
import matplotlib.pyplot as plt
import math

# Takes in MIP coordinates and returns 3D voxel coordinates.

def mip2vox(x, y, theta, phi, ct):
	y_lim = ct.shape[2]	
	z_lim = ct.shape[0]
	x_lim = ct.shape[1]
	start = time.clock()
	for i in xrange(ct.shape[2]):
	    layer = ct[::,::,i]
	    ct[::,::,i] = (Image.fromarray(layer).rotate(-theta, resample=Image.BILINEAR))
	for j in xrange(ct.shape[1]):
		layer = ct[::,j,::]
		ct[::,j,::] = (Image.fromarray(layer).rotate(-phi, resample=Image.BILINEAR))
	print 'Rotating took: %s ms' % ((time.clock()-start)*1000)
	start_2 = time.clock()
	y = y_lim-y
	ray = list(ct[::,x,y])
	z = ray.index(max(ray))
	print 'Finding max took: %s ms' % ((time.clock()-start_2)*1000)

	# plt.imshow(ct[z,::,::])
	# plt.show()

	def rotate(origin, point, angle):
		"""
		Rotate a point counterclockwise by a given angle around a given origin.

		The angle should be given in radians.
		"""
		ox, oy = origin
		px, py = point

		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
		return qx, qy

	center_phi = (z_lim/2.0, y_lim/2.0)
	new_phi = rotate(center_phi, (z, y), math.radians(phi))
	z = new_phi[0]
	y = new_phi[1]

	center_theta = (z_lim/2.0, x_lim/2.0)
	new_theta = rotate(center_theta, (z, x), math.radians(theta))
	z = new_theta[0]
	x = new_theta[1]

	vox = (z, x, y)

	return vox