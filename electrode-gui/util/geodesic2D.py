#!/usr/bin/python
''' This script tests geodesic.py utility function that returns the optimal path from one point to another on a 2D cost mask (e.g. brain mask). Note
    that this is a path and not an interpolation of electrodes along a path.
This 2D version was built to test a basic path traversal algorithm before
    being generalized to 3D.

It takes as inputs two sample voxel coordinates representing the starting and ending points on a mask surface as well as the mask itself used to determine the path on which to traverse. It outputs the path as determined
    by graph traversal using Djikstra's algorithm.
'''

import numpy as np
import networkx as nx

__version__ = '0.0'
__author__ = 'Xavier Islam'
__email__ = 'islamx@seas.upenn.edu'
__copyright__ = "Copyright 2016, University of Pennsylvania"
__credits__ = ["Lohith Kini","Sandhitsu Das", "Joel Stein",
                "Kathryn Davis"]
__license__ = "MIT"
__status__ = "Development"

def geodesic2D(start, end, mask):
	''' returns a geodesic path when given a brain mask, a start point, and
		an end point.

    It takes as inputs two sample voxel coordinates (as tuples) representing
        two points (say corners of a grid for e.g.) along with the brain
        mask on which to perform geodesic marching.

    NOTE: the coordinates given and returned are in (i, j) notation, NOT (
    	x, y). This means that rows increase downward, columns increase
		to the right, and layers increase to the back.

    @param start : Starting coordinate (voxel coordinates)
    @param end : Ending coordinate (voxel coordinates)
    @param mask : Brain mask
    @type start: tuple
    @type end: tuple
    @type mask: numpy array
    @rtype list of tuples

    Example:
    	>> mask_nib = nib.load('2D_brain_mask.nii.gz)
    	>> mask = mask_nib.get_data()
        >> geodesic3D((10,15),(33,34),mask)
    '''

	# Load mask and initialize graph.
	nrow = mask.shape[0]
	ncol = mask.shape[1]
	G = nx.Graph()

	# Populate graph with nodes, with i being the row number and j being the column number.
	for i in range(nrow):
		for j in range(ncol):
			G.add_node((i, j), val=mask[i][j])

	# Make edges for adjacent nodes (diagonal is also considered adjacent) and
	# set default edge weight to infinity.
	for i in range(nrow):
		for j in range(ncol):
			if j == ncol-1 and i != nrow-1:
				G.add_edge((i, j), (i+1, j), weight=float('inf'))
				G.add_edge((i, j), (i+1, j-1), weight=float('inf'))
			elif i == nrow-1 and j != ncol-1:
				G.add_edge((i, j), (i, j+1), weight=float('inf'))
			elif j == 0 and i != nrow-1:
				G.add_edge((i, j), (i, j+1), weight=float('inf'))
				G.add_edge((i, j), (i+1, j), weight=float('inf'))
				G.add_edge((i, j), (i+1, j+1), weight=float('inf'))
			elif i == nrow-1 and j == ncol-1:
				break
			else:
				G.add_edge((i, j), (i, j+1), weight=float('inf'))
				G.add_edge((i, j), (i+1, j), weight=float('inf'))
				G.add_edge((i, j), (i+1, j+1), weight=float('inf'))
				G.add_edge((i, j), (i+1, j-1), weight=float('inf'))

	# Check neighbors to obtain zero count and assign edge weights accordingly.
	for i in range(nrow):
		for j in range(ncol):
		# Only care about nodes with value of 1.
			if G.node[(i, j)]['val'] == 1:
				G.node[(i, j)]['zc'] = 0
				# Obtain zero count (number of neighbors with val of zero) of current node.
				for x in G.neighbors((i, j)):
					if G.node[x]['val'] == 0:
						G.node[(i, j)]['zc'] += 1
				# Change value of nodes with different zero counts to different values.
				if G.node[(i, j)]['zc'] == 0:
					G.node[(i, j)]['val'] = 5
				if G.node[(i, j)]['zc'] == 1:
					G.node[(i, j)]['val'] = 4
				if G.node[(i, j)]['zc'] == 2:
					G.node[(i, j)]['val'] = 4
				if G.node[(i, j)]['zc'] == 3:
					G.node[(i, j)]['val'] = 3

	# Assign edge weights according to value.
	for i in range(nrow):
		for j in range(ncol):
			if G.node[(i, j)]['val'] == 1 or G.node[(i, j)]['val'] == 2 or G.node[(i, j)]['val'] == 3:
				for x in G.neighbors((i, j)):
					if G.node[x]['val'] == 1:
						G.edge[(i, j)][x]['weight'] = 1
					if G.node[x]['val'] == 2:
						G.edge[(i, j)][x]['weight'] = 2
					if G.node[x]['val'] == 3:
						G.edge[(i, j)][x]['weight'] = 3
					if G.node[x]['val'] == 4:
						G.edge[(i, j)][x]['weight'] = 4
					if G.node[x]['val'] == 5:
						G.edge[(i, j)][x]['weight'] = 5

	# Return Dijkstra's shortest path.
	return nx.dijkstra_path(G, start, end)
