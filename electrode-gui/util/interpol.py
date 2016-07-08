import numpy as np

def normalize(v):
# This is a cheeky little subfunction to make unit vectors.
	    norm=np.linalg.norm(v)
	    if norm==0:
	       return v
	    return v/norm

def totuple(a):
# Yet another cheeky subfunction, this time to make numpy arrays in to tuples.
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

def interpol(coor1, coor2, coor3=[], delta=10):
	# This is the main function that interpolates the coordinates of each of the electrodes in a grid using the coordinates
	# of three of the grid corners.

	# Check if only two given
	if(not(coor3)):
		# This accomplishes the same as the above function, but for strips of electrodes rather than grids.
		coor1 = np.asarray(coor1)
		coor2 = np.asarray(coor2)
		A = coor1
		B = coor2
		A2B = np.subtract(coor2, coor1)
		unit_A2B = normalize(A2B)
		names = []
		elec_coor = []
		new_corr = A
		i = 1
		while np.all(np.less_equal(new_corr, B)):
			elec_coor.append(totuple(new_corr))
			names.append("STRIP %d" % i)
			new_corr = np.add(new_corr, delta*(unit_A2B))
			i += 1
		pairs = dict(zip(names, elec_coor))
		return pairs
	else:
		# Turn input coordinates (which are presumably lists) into numpy arrays.
		coor1 = np.asarray(coor1)
		coor2 = np.asarray(coor2)
		coor3 = np.asarray(coor3)
		# Figure out points A, B, and C of grid and respective vectors (A2B and B2C) that define grid.
		vec1 = np.subtract(coor1, coor2)
		vec2 = np.subtract(coor2, coor3)
		vec3 = np.subtract(coor1, coor3)
		mag_1 = np.linalg.norm(vec1)
		mag_2 = np.linalg.norm(vec2)
		mag_3 = np.linalg.norm(vec3)
		if (mag_1 >= mag_2) and (mag_1 >= mag_3):
			A = coor1
			B = coor3
			C = coor2
			A2B = -1 * vec3
			B2C = vec2
		if (mag_2 >= mag_1) and (mag_2 >= mag_3):
			A = coor2
			B = coor1
			C = coor3
			A2B = vec1
			B2C = -1 * vec3
		if (mag_3 >= mag_1) and (mag_3 >= mag_2):
			A = coor1
			B = coor2
			C = coor3
			A2B = -1 * vec1
			B2C = -1 * vec2
		unit_A2B = normalize(A2B)
		unit_B2C = normalize(B2C)
		# Use while loops to deduce locations of electrodes.
		names = []
		elec_coor = []
		i = 1
		j = 1
		new_corr = A
		if np.all(np.less(A[0:3:2], B[0:3:2])):
			while np.all(np.less_equal(new_corr, C)):
				while np.all(np.less_equal(new_corr[0:3:2], B[0:3:2])):
					elec_coor.append(totuple(new_corr))
					names.append("GRID %d" % i)
					new_corr = np.add(new_corr, delta*(unit_A2B))
					i += 1
				new_corr = np.add(A, delta*j*(unit_B2C))
				j += 1
		else:
			while np.all(np.less_equal(new_corr, C)):
				while np.all(np.less_equal(new_corr[1], B[1])):
					elec_coor.append(totuple(new_corr))
					names.append("GRID %d" % i)
					new_corr = np.add(new_corr, delta*(unit_A2B))
					i += 1
				new_corr = np.add(A, delta*j*(unit_B2C))
				j += 1
		pairs = dict(zip(names, elec_coor))
		return pairs

