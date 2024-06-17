import struct
import pickle

def store_data_noisy_circle(filename, dataPts, radius, noise_level, num_points, sizeOfInterval, overlapRatio): # to store the generated point cloud data
    with open(filename, 'wb') as file:
        # Store radius, noise_level, num_points, sizeOfInterval, overlapRatio as binary data
        file.write(struct.pack('d', radius))
        file.write(struct.pack('d', noise_level))
        file.write(struct.pack('d', num_points))
        file.write(struct.pack('d', sizeOfInterval))
        file.write(struct.pack('d', overlapRatio))

        # Serialize and store dataPts using pickle
        pickle.dump(dataPts, file)

def retrieve_data_noisy_circle(filename): # to retrieve point cloud data from file
    with open(filename, 'rb') as file:
        # Read radius, noise_level, num_points, sizeOfInterval, overlapRatio from binary data
        radius = struct.unpack('d', file.read(8))[0]
        noise_level = struct.unpack('d', file.read(8))[0]
        num_points = struct.unpack('d', file.read(8))[0]
        sizeOfInterval = struct.unpack('d', file.read(8))[0]
        overlapRatio = struct.unpack('d', file.read(8))[0]

        # Deserialize dataPts using pickle
        dataPts = pickle.load(file)

    return dataPts, radius, noise_level, num_points, sizeOfInterval, overlapRatio

def store_data_noisy_pOITC(filename, dataPts, circle1_radius, circle2_radius, num_points, noise_level, sizeOfInterval,
                      overlapRatio):
    with open(filename, 'wb') as file:
        # Store circle1_radius, circle2_radius, num_points, noise_level, sizeOfInterval, overlapRatio as binary data
        file.write(struct.pack('d', circle1_radius))
        file.write(struct.pack('d', circle2_radius))
        file.write(struct.pack('d', num_points))
        file.write(struct.pack('d', noise_level))
        file.write(struct.pack('d', sizeOfInterval))
        file.write(struct.pack('d', overlapRatio))

        # Serialize and store dataPts using pickle
        pickle.dump(dataPts, file)


#### Function to Retrieve Data from a Binary File
def retrieve_data_noisy_pOITC(filename):
    with open(filename, 'rb') as file:
        # Read circle1_radius, circle2_radius, num_points, noise_level, sizeOfInterval, overlapRatio from binary data
        circle1_radius = struct.unpack('d', file.read(8))[0]
        circle2_radius = struct.unpack('d', file.read(8))[0]
        num_points = struct.unpack('d', file.read(8))[0]
        noise_level = struct.unpack('d', file.read(8))[0]
        sizeOfInterval = struct.unpack('d', file.read(8))[0]
        overlapRatio = struct.unpack('d', file.read(8))[0]

        # Deserialize dataPts using pickle
        dataPts = pickle.load(file)

    return dataPts, circle1_radius, circle2_radius, num_points, noise_level, sizeOfInterval, overlapRatio


