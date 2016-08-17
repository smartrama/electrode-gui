import numpy as np
import scipy.ndimage.interpolation as sci
import time
import matplotlib.pyplot as plt
import math

# Takes in MIP coordinates and returns 3D voxel coordinates.

def mip2vox(x, y, theta, phi, ct):
	start = time.clock()
	ct = sci.rotate(ct, -theta, axes=(0,1), reshape=False)
	ct = sci.rotate(ct, -phi, axes=(0,2), reshape=False)
	print 'Rotating took: %s s' % ((time.clock()-start))
	start_2 = time.clock()
	y_lim = ct.shape[2]	
	z_lim = ct.shape[0]
	x_lim = ct.shape[1]
	y = y_lim-y
	ray = list(ct[::,x,y])
	z = ray.index(max(ray))
	print 'Finding max took: %s s' % ((time.clock()-start_2))

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