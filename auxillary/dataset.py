import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def vertical_torus_point_cloud(R, r, n, noise_level=0.1):
    # Sample n points for theta and phi
    theta = np.linspace(0, 2 * np.pi, n)
    phi = np.linspace(0, 2 * np.pi, n)

    # Create a grid
    theta, phi = np.meshgrid(theta, phi)

    # Parametric equations of the torus (vertical orientation)
    x = (R + r * np.cos(phi)) * np.cos(theta)
    z = (R + r * np.cos(phi)) * np.sin(theta)
    y = r * np.sin(phi)

    # Flatten the arrays to create a list of points
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    # Combine x, y, z to form point cloud
    points = np.vstack((x, y, z)).T

    # Adding Gaussian noise to each coordinate
    noise = np.random.normal(scale=noise_level, size=points.shape)
    noisy_points = points + noise

    return noisy_points

def noisy_circle(radius, num_points, noise_level):
    """
    Generate a noisy point cloud for a circle.

    Parameters:
    radius (float): Radius of the circle.
    num_points (int): Number of points to generate.
    noise_level (float): Standard deviation of the Gaussian noise to be added.

    Returns:
    ndarray: Array of noisy points on the circle.
    """
    # Generate angles for the points
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

    # Generate points on the circle
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    # Combine x and y to form points
    points = np.vstack((x, y)).T

    # Add Gaussian noise to each coordinate
    noise = np.random.normal(scale=noise_level, size=points.shape)
    noisy_points = points + noise

    return noisy_points

def noisy_pairOf_InternallyTouchingCircles(circle1_radius, circle2_radius, num_points, noise_level):
    # Circle 1 (larger circle)
    theta1 = np.linspace(0, 2 * np.pi, num_points // 2)
    circle1_x = circle1_radius * np.cos(theta1)
    circle1_y = circle1_radius * np.sin(theta1)

    # Circle 2 (smaller circle, touching the larger circle internally)
    # The smaller circle's center is at (circle1_radius - circle2_radius, 0)
    theta2 = np.linspace(0, 2 * np.pi, num_points // 2)
    circle2_x = (circle1_radius - circle2_radius) + circle2_radius * np.cos(theta2)
    circle2_y = circle2_radius * np.sin(theta2)

    # Combine the points
    points_x = np.concatenate([circle1_x, circle2_x])
    points_y = np.concatenate([circle1_y, circle2_y])

    # Add noise
    noise_x = np.random.normal(0, noise_level, num_points)
    noise_y = np.random.normal(0, noise_level, num_points)
    noisy_points_x = points_x + noise_x
    noisy_points_y = points_y + noise_y

    noisy_points = np.column_stack((noisy_points_x, noisy_points_y))

    return noisy_points


def point_cloud_elephant(npy_filename="elephant1.npy", sample_fraction=0.5):
    vertices = np.load(npy_filename)
    print(f"Total points: {len(vertices)}")

    # Sample a subset of points because taking all 1000 points makes the figure too opaque to figure out structures
    sample_size = int(len(vertices) * sample_fraction)
    if sample_size > 0:
        sampled_indices = np.random.choice(len(vertices), size=sample_size, replace=False)
        sampled_vertices = vertices[sampled_indices]
    else:
        sampled_vertices = vertices
    # print(type(sampled_vertices))
    # sampled_vertices = sampled_vertices.tolist()
    print(f"Points sampled for consideration: {len(sampled_vertices)}")
    return sampled_vertices
    # print(f"points we take: {len(sampled_vertices)}")
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # # Plot the vertices
    # ax.scatter( sampled_vertices[:, 2], sampled_vertices[:, 0], sampled_vertices[:, 1], s=1)
    #
    # # Set plot labels
    # ax.set_title('3D Point Cloud')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    #
    # plt.show()