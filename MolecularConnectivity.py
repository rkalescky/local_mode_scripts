import sys
import numpy     as np
import networkx  as nx
from   itertools import combinations, ifilter
from   scipy.spatial.distance import squareform, pdist, cdist

def cartesianCenter(cartesian_coords):
    return np.mean(cartesian_coords, axis=0)

def distanceMatrix(cartesian_coords):
    return squareform(pdist(cartesian_coords))

def bondLengths(bond_connectivity, distance_matrix):
    bond_lengths = []
    for i in bond_connectivity:
        bond_lengths.append(distance_matrix[i[0], i[1]])
    return np.array(bond_lengths)

def angleConnectivity(bond_connectivity):
    graph = nx.from_edgelist(bond_connectivity)
    iangles = []
    for i in graph.nodes():
        for (m, n) in combinations(graph.neighbors(i), 2):
            iangles.append((m, i, n))
    return np.array(iangles)

def dihedralConnectivity(bond_connectivity):
    graph = nx.from_edgelist(bond_connectivity)
    idihedrals = []
    for a in graph.nodes():
        for b in graph.neighbors(a):
            for c in ifilter(lambda c: c not in [a, b], graph.neighbors(b)):
                for d in ifilter(lambda d: d not in [a, b, c], graph.neighbors(c)):
                    idihedrals.append((a, b, c, d))
    return np.array(idihedrals)

def averageDistance(connectivity, cartesian_coords, center):
    avg_dist = []
    for i in connectivity:
        points = []
        for j in range(0, len(connectivity[i][:])):
            points.append(pdist([center, cartesian_coords[i[j]][:]]))
        avg_dist.append(np.around(np.mean(points), decimals=5))
    avg_dist = np.array(avg_dist)
    return np.unique(avg_dist, return_index=True, return_inverse=True)

def printUniqueConnectivity(connectivity, unique):
    for i in range(0, len(unique[1])):
        print(connectivity[unique[1][i]] + 1)

atom_connectivity = np.loadtxt(sys.argv[1], dtype=int)
if atom_connectivity.min() == 1:
    atom_connectivity -= 1

cartesian_coords      = np.loadtxt(sys.argv[2], dtype=float)
distance_matrix       = distanceMatrix(cartesian_coords)
center                = cartesianCenter(cartesian_coords)
angle_connectivity    = angleConnectivity(atom_connectivity)
dihedral_connectivity = dihedralConnectivity(atom_connectivity)
unique_bonds          = averageDistance(atom_connectivity, cartesian_coords, center)
unique_angles         = averageDistance(angle_connectivity, cartesian_coords, center)
unique_dihedrals      = averageDistance(dihedral_connectivity, cartesian_coords, center)

print("All Connectivity:")
print(atom_connectivity + 1)
print(angle_connectivity + 1)
print(dihedral_connectivity + 1)
# print(unique_bonds)
# print(unique_angles)
# print(unique_dihedrals)

print("Unique Connectivity:")
printUniqueConnectivity(atom_connectivity,     unique_bonds)
printUniqueConnectivity(angle_connectivity,    unique_angles)
printUniqueConnectivity(dihedral_connectivity, unique_dihedrals)



