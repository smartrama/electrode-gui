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

def interpol(coor1, coor2, coor3, m, n):
	# This is the main function that interpolates the coordinates of each of the electrodes in a grid using the coordinates 
	# of three of the grid corners.

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
	mag_A2B = np.linalg.norm(A2B)
	mag_B2C = np.linalg.norm(B2C)
	# Use for loops to deduce locations of electrodes.
	names = []
	elec_coor = []
	new_corr = A
	elec_coor.append(totuple(new_corr))
	count = 1
	names.append("GRID %d" % count)
	for j in range(n):
		for i in range(m-1):
			new_corr = np.add(new_corr, (mag_A2B/(m-1))*(unit_A2B))
			elec_coor.append(totuple(new_corr))
			count += 1
			names.append("GRID %d" % count)
		new_corr = np.add(A, (mag_B2C/(n-1))*(j+1)*(unit_B2C))
		elec_coor.append(totuple(new_corr))
		count += 1
		names.append("GRID %d" % count)
	names = names[0:-1]
	elec_coor = elec_coor[0:-1]
	pairs = dict(zip(names, elec_coor))
	return pairs