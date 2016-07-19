import numpy as np
import networkx as nx
import math

def geodesic(start, end, mask):
# This function returns a geodesic path when given a brain mask, a start point, and an end point.
# NOTE: the coordinates given and returned are in (i, j, k) notation, NOT (x, y, z).
#       This means that rows increase downward, columns increase to the right, and layers increase to the back.

    # Load mask and initialize graph.
    mag_path = int(math.ceil(0.1*np.linalg.norm(np.subtract(end, start))))
    if start[0] <= end[0]:
        zero_i = start[0]-mag_path
        nrow = end[0]+mag_path
    else:
        zero_i = end[0]-mag_path
        nrow = start[0]+mag_path
    if start[1] <= end[1]:
        zero_j = start[1]-1
        ncol = end[1]+1
    else:
        zero_j = end[1]-1
        ncol = start[1]+1
    if start[2] <= end[2]:
        zero_k = start[2]-mag_path
        nlay = end[2]+mag_path
    else:
        zero_k = end[2]-mag_path
        nlay = start[2]+mag_path
    zero_i = int(zero_i)
    zero_j = int(zero_j)
    zero_k = int(zero_k)
    nrow = int(nrow)
    ncol = int(ncol)
    nlay = int(nlay)
    G = nx.Graph()
    # Populate graph with nodes, with i being the row number and j being the column number.
    for i in range(zero_i, nrow):
        for j in range(zero_j, ncol):
            for k in range(zero_k, nlay):
                G.add_node((i, j, k), val=int(mask[i][j][k]))
    # Make edges for adjacent nodes (diagonal is also considered adjacent) and set default edge weight to infinity.
    for i in range(zero_i, nrow):
        for j in range(zero_j, ncol):
            for k in range(zero_k, nlay):
                if i == zero_i and j == zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                elif i == zero_i and j == zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                elif i == zero_i and j == zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                elif i == zero_i and j == ncol-1 and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                elif i == zero_i and j == ncol-1 and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                elif i == zero_i and j == ncol-1 and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                elif i == zero_i and j != zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                elif i == zero_i and j != zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                elif i == zero_i and j != zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                elif i == nrow-1 and j == zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                elif i == nrow-1 and j == zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                elif i == nrow-1 and j == zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                elif i == nrow-1 and j == ncol-1 and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                elif i == nrow-1 and j == ncol-1 and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i == nrow-1 and j == ncol-1 and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i == nrow-1 and j != zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                elif i == nrow-1 and j != zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i == nrow-1 and j != zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i != zero_i and j == zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                elif i != zero_i and j == zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                elif i != zero_i and j == zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                elif i != zero_i and j == ncol-1 and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                elif i != zero_i and j == ncol-1 and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i != zero_i and j == ncol-1 and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i != zero_i and j != zero_j and k == zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                elif i != zero_i and j != zero_j and k == nlay-1:
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
                elif i != zero_i and j != zero_j and k != zero_k:
                    G.add_edge((i, j, k), (i, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i+1, j-1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j+1, k-1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k+1), weight=float('inf'))
                    G.add_edge((i, j, k), (i-1, j-1, k-1), weight=float('inf'))
    # Check neighbors to obtain zero count and assign edge weights accordingly.
    for i in range(zero_i, nrow):
        for j in range(zero_j, ncol):
            for k in range(zero_k, nlay):
            # Only care about nodes with value of 1.
                if G.node[(i, j, k)]['val'] == 1:
                    G.node[(i, j, k)]['zc'] = 0
                    # Obtain zero count (number of neighbors with val of zero) of current node.
                    for x in G.neighbors((i, j, k)):
                        if G.node[x]['val'] == 0:
                            G.node[(i, j, k)]['zc'] += 1
                    # Change value of nodes with different zero counts to different values.
                    if G.node[(i, j, k)]['zc'] == 0:
                        G.node[(i, j, k)]['val'] = 6
                    if G.node[(i, j, k)]['zc'] == 1:
                        G.node[(i, j, k)]['val'] = 5
                    if G.node[(i, j, k)]['zc'] == 3:
                        G.node[(i, j, k)]['val'] = 4
                    if G.node[(i, j, k)]['zc'] >= 5:
                        G.node[(i, j, k)]['val'] = 3
    # Assign edge weights according to value.
    for i in range(zero_i, nrow):
        for j in range(zero_j, ncol):
            for k in range(zero_k, nlay):
                if G.node[(i, j, k)]['val'] >= 3:
                    for x in G.neighbors((i, j, k)):
                        if G.node[x]['val'] == 1:
                            G.edge[(i, j, k)][x]['weight'] = 1
                        if G.node[x]['val'] == 3:
                            G.edge[(i, j, k)][x]['weight'] = 2
                        if G.node[x]['val'] == 4:
                            G.edge[(i, j, k)][x]['weight'] = 4
                        if G.node[x]['val'] == 5:
                            G.edge[(i, j, k)][x]['weight'] = 5
                        if G.node[x]['val'] == 6:
                            G.edge[(i, j, k)][x]['weight'] = 6
    # Return Dijkstra's shortest path.
    return nx.dijkstra_path(G, start, end)
