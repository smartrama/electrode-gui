#!/usr/bin/python

import numpy as np
import math
import itertools
from interpol import interpol
from geodesic3D import geodesic3D

def geodesic3D_hybrid(A, B, C, D, m, n, mask):

	A2C = tuple(geodesic3D(A, C, mask))
	B2D = interpol(B, D, [], 1, n)
	B2D = tuple(B2D)

	# Divide up sides into n electrodes.
	dist = len(A2C)
	l = dist-1
	k = l/float(m-1) # Distance between electrodes
	electrodes = []
	i = 0
	if k.is_integer():
		while i <= l:
			electrodes.append(A2C[int(i)])
			i += k
	else:
		while True:
			if i >= l:
				electrodes.append(A2C[-1])
				break
			else:
				e, f = math.modf(i)
				f = int(f)
				inc = tuple(np.add(A2C[f],np.multiply(e,(np.subtract(A2C[f+1],A2C[f])))))
				electrodes.append(inc)
				i += k

	# Interpolate linearly between each side.
	grid = []
	grid.append(electrodes)
	for i in xrange(0,n):
		start = electrodes[i]
		end = B2D[i]
		pairs = interpol(start, end, [], 1, n)
		grid.append(pairs[1:-1])
	grid.append(B2D)
	grid = list(itertools.chain(*grid))

	return grid