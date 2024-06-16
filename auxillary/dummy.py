

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_colored_subsets(dataPts, colors, dataPtsCov, covToclus):
    dataPts = np.array(dataPts)  # Ensure dataPts is a numpy array for indexing
    colors = np.array(colors)  # Convert colors to a numpy array for indexing

    # Check if the points are 2D or 3D
    is3D = dataPts.shape[1] == 3

    # Ensure that dataPtsCov and covToclus have the same length
    assert len(dataPtsCov) == len(covToclus), "dataPtsCov and covToclus must have the same length"

    for i, (subset, cluster_indices) in enumerate(zip(dataPtsCov, covToclus)):
        fig = plt.figure()
        if is3D:
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = fig.add_subplot(111)
        ax.set_aspect('equal', 'box')
        if cluster_indices:
            legend_labels = [f'Cluster {idx}' for idx in set(cluster_indices)]
            legend_label = '\n'.join(legend_labels)
            mask = np.isin(dataPts, subset).all(axis=1)
            scatter = ax.scatter(dataPts[mask, 0], dataPts[mask, 1], c=colors[mask], marker='o', label=legend_label, s=5)

        # Plot the rest of the points in grey
        mask = np.ones(len(dataPts), dtype=bool)
        mask &= ~np.isin(dataPts, subset).all(axis=1)
        ax.scatter(dataPts[mask, 0], dataPts[mask, 1], c='grey', marker='o', alpha=0.5, s=5)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        if is3D:
            ax.set_zlabel('Z')

        if cluster_indices:
            ax.legend()

        plt.show()




# Example usage:
# dataPts_3D = [
#     [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]
# ]
# colors_3D = ['red', 'green', 'blue', 'yellow', 'purple']
# dataPtsCov_3D = [
#     [[1, 2, 3], [4, 5, 6]],
#     [[7, 8, 9], [10, 11, 12]]
# ]
#
# dataPts_2D = [
#     [1, 2], [4, 5], [7, 8], [10, 11], [13, 14]
# ]
# colors_2D = ['red', 'green', 'blue', 'yellow', 'purple']
# dataPtsCov_2D = [
#     [[1, 2], [4, 5]],
#     [[7, 8], [10, 11]]
# ]

# Uncomment the appropriate lines to test
# plot_colored_subsets(dataPts_3D, colors_3D, dataPtsCov_3D)
# plot_colored_subsets(dataPts_2D, colors_2D, dataPtsCov_2D)
