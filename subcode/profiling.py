import cProfile
import numpy as np
from data_process import generateDravesIFS

# Define some sample inputs
coeffs_sample = np.random.rand(10, 2, 2)
sums_sample = np.random.rand(10, 2)
probabilities_sample = np.random.rand(10)
iterations_sample = 50000

# Profile the generateDravesIFS function
cProfile.run('generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, iterations_sample)', 'output.pstats')