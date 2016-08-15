#!/usr/bin/python

import numpy as np
import math
import itertools
from interpol import interpol
from geodesic3D import geodesic3D

def geodesic3D_hybrid(A, B, C, D, m, n, mask):

	A2C = tuple(geodesic3D(A, C, mask))
	B2D = tuple(geodesic3D(B, D, mask))

	# Divide up sides into n electrodes.
	sides = [A2C, B2D]
	d = {}
	for x in sides:
		dist = len(x)
		l = dist-1
		k = l/float(m-1) # Distance between electrodes
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
		grid.append(pairs[1:-1])
	grid.append(d[B2D])
	grid = list(itertools.chain(*grid))

	return grid