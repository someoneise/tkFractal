import csv
import numpy as np
from itertools import batched
from numpy import ndarray as NDarray
import scipy
from numba import jit
# from multiprocessing import Pool

def read_data(param_file:str):
    """
    :param l2: A 2D numpy array of the affine transformations.
    structure: 
    [
    [0, 0,0, 0.16, 0, 0, 0.01],
    [0.85, 0.04,-0.04, 0.85, 0, 1.6, 0.85],
    [0.2, -0.26, 0.23, 0.22, 0, 1.6, 0.07],
    [-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07]
    ]

    """
    tcoeffs = []
    sums = []
    probabilites = []
    with open(param_file, 'r',newline="") as csvfile:
        matrixreader = csv.reader(csvfile, delimiter=' ')
        for row in matrixreader:
            rawcoeffs = [float(i) for i in row[:4]]
            coeffs = itertools.batched(rawcoeffs,2)
            tcoeffs.append(list(coeffs))
            sums.append([float(i) for i in row[4:6]])
            probabilites.append(float(row[6]))

    return (np.array(tcoeffs), np.array(sums), np.array(probabilites).T)

@jit(nopython=True)
def weighted_rand_choice(prob):
    """
    :param arr: A 1D numpy array of values to sample from.
    :param prob: A 1D numpy array of probabilities for the given samples.
    :return: A random index from the given array with a given probability.
    """
    return np.searchsorted(np.cumsum(prob), np.random.random(), side="right")

@jit(nopython=True)
def generateDravesIFS(coeffs:NDarray,sums:NDarray,probabilities:NDarray,iterations:int=50000) -> tuple:
    """
    :param coeffs: A 3D numpy array of the affine transformations.
    :param sums: A 2D numpy array of the sums for the affine transformations.
    :param probabilities: A 1D numpy array of the probabilities for the given transformations.
    :param iterations: The number of iterations to perform.
    :return: A tuple of 3 numpy arrays containing the x and y coordinates and the color values.
    """

    probabilities /= probabilities.sum() # Normalize the probabilities

    # Initialize lists to store the x and y coordinates
    xy = np.array([ 0.0, 0.0 ])
    c= np.random.random_sample() # Random starting color
    ci = np.linspace(0.0,1.0,len(coeffs)) # Color i for each transformation

    x_points = np.zeros(iterations)
    y_points = np.zeros(iterations)
    c_points = np.zeros(iterations)

    # Perform the iterations (heavy part of the code)
    for i in range(iterations):
        
        function_index = weighted_rand_choice(probabilities) # Choose a random transformation

        xy = np.dot(coeffs[function_index],xy) + sums[function_index].T # Apply the transformation

        c = (c + ci[function_index]) / 2 # Change the color according to Drave's paper

        x_points[i] = xy[0]
        y_points[i] = xy[1]
        c_points[i] = float(c)

    return x_points,y_points,c_points

def generateAttractor():
    pass

'''
tried to parallelize the function but it is not working as expected :(

def parallel_generateDravesIFS(coeffs:NDarray, sums:NDarray, probabilities:NDarray, iterations:int=50000, num_processes:int=4) -> tuple:
    # Create a multiprocessing Pool
    with Pool(num_processes) as pool:
        # Run generateDravesIFS in parallel and collect the results
        results = pool.starmap(generateDravesIFS, [(coeffs, sums, probabilities, iterations) for _ in range(num_processes)])

    # Concatenate the results
    x_points_all = np.concatenate([result[0] for result in results])
    y_points_all = np.concatenate([result[1] for result in results])
    c_points_all = np.concatenate([result[2] for result in results])

    return x_points_all, y_points_all, c_points_all
    '''