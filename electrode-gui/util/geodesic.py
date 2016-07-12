import numpy as np
import networkx as nx
import string

def geodesic(start, end, mask_path):
# This function returns a geodesic path when given a brain mask, a start point, and an end point.
	# Load mask and initialize graph.
	mask = np.load(mask_path)
	nrow = mask.shape[0]
	ncol = mask.shape[1]
	asc = string.ascii_uppercase
	G = nx.Graph()
	# Populate graph with nodes, with letters as rows and numbers as columns.
	for i in range(nrow):
		for j in range(ncol):
			G.add_node(asc[i] + str(j), val=mask[i][j])
	# Make edges for adjacent nodes (diagonal is also considered adjacent) and set default edge weight to infinity.
	for i in range(nrow):
		for j in range(ncol):
			if j == ncol-1 and i != nrow-1:
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j-1)), weight=float('inf'))
			elif i == nrow-1 and j != ncol-1:
				G.add_edge((asc[i] + str(j)), (asc[i] + str(j+1)), weight=float('inf'))
			elif j == 0 and i != nrow-1:
				G.add_edge((asc[i] + str(j)), (asc[i] + str(j+1)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j+1)), weight=float('inf'))
			elif i == nrow-1 and j == ncol-1:
				break
			else:
				G.add_edge((asc[i] + str(j)), (asc[i] + str(j+1)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j+1)), weight=float('inf'))
				G.add_edge((asc[i] + str(j)), (asc[i+1] + str(j-1)), weight=float('inf'))
	# Check neighbors to obtain zero count and assign edge weights accordingly.
	for i in range(nrow):
		for j in range(ncol):
			# Only care about nodes with value of 1.
			if G.node[asc[i] + str(j)]['val'] == 1:
				G.node[asc[i] + str(j)]['zc'] = 0
				# Obtain zero count (number of neighbors with val of zero) of current node.
				for x in G.neighbors(asc[i] + str(j)):
					if G.node[x]['val'] == 0:
						G.node[asc[i] + str(j)]['zc'] += 1
				# Change value of nodes with different zero counts to different values.
				if G.node[asc[i] + str(j)]['zc'] == 0:
					G.node[asc[i] + str(j)]['val'] = 5
				if G.node[asc[i] + str(j)]['zc'] == 1:
					G.node[asc[i] + str(j)]['val'] = 4
				if G.node[asc[i] + str(j)]['zc'] == 2:
					G.node[asc[i] + str(j)]['val'] = 4
				if G.node[asc[i] + str(j)]['zc'] == 3:
					G.node[asc[i] + str(j)]['val'] = 3
	# Assign edge weights according to value.
	for i in range(nrow):
		for j in range(ncol):
			if G.node[asc[i] + str(j)]['val'] == 1 or G.node[asc[i] + str(j)]['val'] == 2 or G.node[asc[i] + str(j)]['val'] == 3:
				for x in G.neighbors(asc[i] + str(j)):
					if G.node[x]['val'] == 1:
						G.edge[asc[i] + str(j)][x]['weight'] = 1
					if G.node[x]['val'] == 2:
						G.edge[asc[i] + str(j)][x]['weight'] = 2
					if G.node[x]['val'] == 3:
						G.edge[asc[i] + str(j)][x]['weight'] = 3
					if G.node[x]['val'] == 4:
						G.edge[asc[i] + str(j)][x]['weight'] = 4
					if G.node[x]['val'] == 5:
						G.edge[asc[i] + str(j)][x]['weight'] = 5
	# Return Dijkstra's shortest path.
	return nx.dijkstra_path(G, start, end)