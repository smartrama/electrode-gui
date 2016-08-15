import numpy as np
import time

def elec_snap(interpol_coords, segment):
	interpol_coords = np.asarray(interpol_coords)

	scan_start = time.clock()
	elec = np.argwhere(segment > 1)
	print 'Scan took: %s ms'%((time.clock()-scan_start)*1000)

	snap_coords = []
	for x in interpol_coords:
		dists = [np.linalg.norm(x-y) for y in elec]
		min_index = dists.index(min(dists))
		snap_coords.append(elec[min_index])
		
	return snap_coords