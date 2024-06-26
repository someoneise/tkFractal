import timeit
import numpy as np
from data_process import generateDravesIFS  # , parallel_generateDravesIFS

# Define some sample inputs
coeffs_sample = np.random.rand(10, 2, 2)
sums_sample = np.random.rand(10, 2)
probabilities_sample = np.random.rand(10)
iterations_sample = 800000
parallel_iterations_sample = 200000

generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, 1)


# Time the generateDravesIFS function
def time_funcs():
    run1 = 'generateDravesIFS(coeffs_sample, sums_sample, ' \
           ' probabilities_sample, iterations_sample)'
    run2 = 'parallel_generateDravesIFS(coeffs_sample, ' \
           ' sums_sample, probabilities_sample, parallel_iterations_sample, 4)'
    generateDravesIFS_time = timeit.timeit(run1,
                                           globals=globals(),
                                           number=3)

    # Time the parallel_generateDravesIFS function
    parallel_generateDravesIFS_time = timeit.timeit(run2,
                                                    globals=globals(),
                                                    number=3)

    print(f"generateDravesIFS t: {generateDravesIFS_time}")
    print(f"parallel_generateDravesIFS t: {parallel_generateDravesIFS_time}")


if __name__ == "__main__":
    time_funcs()
