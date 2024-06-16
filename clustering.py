import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib.pyplot as plt
import display as dsp


def single_linkage_clustering(points, threshold):
    """
    Perform single linkage clustering on a set of points.

    Parameters:
    points (ndarray): An array of points, where each point is represented as (x, y, z).
    threshold (float): The distance threshold for forming clusters.

    Returns:
    ndarray: An array of cluster labels.
    """
    # Compute the linkage matrix using single linkage
    Z = linkage(points, method='single')

    # Form clusters based on the distance threshold
    clusters = fcluster(Z, t=threshold, criterion='distance')

    return clusters
def partialCluster(pointsSet, coveringSet, threshold, clusterVertices, edgeList, coveringToCluster):
    n = len(pointsSet)  # number of points
    l = len(coveringSet)
    baseIndex = 0
    newBaseIndex = 0

    # clusterVertices = set()
    # coveringToCluster = list of clusters at a given index is induced by an element of the cover at the same index

    completeClusterIndexing = {tuple(pt): [] for pt in pointsSet}  # Convert ndarray to tuple

    for U in coveringSet:
        partialClusterIndexing = single_linkage_clustering(U, threshold)
        i = 0
        temp = []  # list of clusters belonging to the elements of cover U
        for pt in U:
            completeClusterIndexing[tuple(pt)].append(baseIndex + partialClusterIndexing[i])
            clusterVertices.add(baseIndex + partialClusterIndexing[i])
            temp.append(baseIndex + partialClusterIndexing[i])
            newBaseIndex = max(newBaseIndex, baseIndex + partialClusterIndexing[i])
            i += 1
        baseIndex = newBaseIndex
        coveringToCluster.append(temp)

    #for point, cluster_indices in completeClusterIndexing.items():
    #    print(f"Point: {point}, Cluster Indices: {cluster_indices}")
    # for e in clusterVertices:
    #      print(e)

    #edgeList = []
    for key, value in completeClusterIndexing.items():  # Add .items() to iterate over key-value pairs
        if len(value) > 1:
            edgeList.append(value)

    # self.clusterVertices=clusterVertices
    # return dsp.create_undirected_graph(pointsSet, clusterVertices, edgeList)


"""
# Example usage
points = np.array([
    [1,1,1],
    [1,1,10],
    [1,1,17],
    [1,1,20],
    [1,1,21],
    [1,1,30],
    [1,1,37],
    [1,1,39],
    [1,1,42],
    [1,1,45]

])
cover=[
    [[1,1,1],
    [1,1,10],
    [1,1,17],
    [1,1,20],],

    [[1,1,17],
    [1,1,20],
    [1,1,21],
    [1,1,30],],

    [[1,1,21],
    [1,1,30],
    [1,1,37],
    [1,1,39]],

    [[1,1,37],
    [1,1,39],
    [1,1,42],
    [1,1,45]]


]


threshold = 5.0
clusters = single_linkage_clustering(points, threshold)
print(clusters, end="\n")  # Output: Cluster labels for each point
partialCluster(points, cover, threshold)

# Plotting the original points
fig = plt.figure(figsize=(12, 7))

# Original points plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(points[:, 0], points[:, 1], points[:, 2], c='blue', marker='o')
ax1.set_title('Original Points')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

# Plotting the clustered points
ax2 = fig.add_subplot(122, projection='3d')
sc = ax2.scatter(points[:, 0], points[:, 1], points[:, 2], c=clusters, cmap='viridis')
plt.colorbar(sc, ax=ax2, label='Cluster Label')
ax2.set_title('Clustered Points')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')

plt.show()
"""
