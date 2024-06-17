import scipy.spatial.distance as dst
import numpy as np

def z_extract(points):
    """
    Extracts the z-coordinates from an array of 3D points.

    Parameters:
    points (list of tuples/lists): Array of points, where each point is represented as (x, y, z).

    Returns:
    list: A list containing the z-coordinates of each point.
    """
    # Extract the z-coordinates using a list comprehension
    z_coords = [point[1] for point in points]
    return z_coords

def y_extract(points):
    y_coords=[pt[1] for pt in points]
    return y_coords

def eccentricity_p(distMatrix, points, pt = -1, p = -1):
    print("distMatrix received:")
    #print(distMatrix)

    if pt == -1:
        # Raise the distance matrix to the power of p
        distMatrix_p = distMatrix ** p
        # Compute the sum of each row (i.e., sum of distances from each point to all other points)
        sum_distances = np.sum(distMatrix_p, axis=1)
        # Calculate the mean of the distances
        mean_distances = sum_distances / (len(points)-1)
        # Compute the p-th root of the mean distances
        eccentricities = mean_distances ** (1 / p)
        return eccentricities
    else:
        idx = points.index(pt)
        sum_distances = 0
        for d in distMatrix[idx]:
            sum_distances += d
        mean_distances = sum_distances / len(points)
        # Compute the p-th root of the mean distances
        eccentricity = mean_distances ** (1 / p)
        return eccentricity


def ecc_p(dataPts, p):
    # Calculate variance vector, replace 0 variance with 1
    var_vec = np.var(dataPts, axis=0)
    var_vec = np.where(var_vec > 0, var_vec, 1.0)

    def finite_ecc(x, data):
        num = np.sum(dst.cdist([x], data, metric='seuclidean', V=var_vec)[0])
        result = np.power(num, p) / len(data)
        return np.power(result, 1.0 / p)

    # Compute the eccentricity for each point in dataPts
    eccentricities = [finite_ecc(x, dataPts) for x in dataPts]

    return eccentricities
