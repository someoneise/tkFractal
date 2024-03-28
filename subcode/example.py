import matplotlib.pyplot as plt
import numpy as np

# Define the affine transformations for the Barnsley Fern
functions = [
    [[0, 0],[0, 0.16], 0, 0],
    [[0.85, 0.04],[-0.04, 0.85], 0, 1.6],
    [[0.2, -0.26], [0.23, 0.22], 0, 1.6],
    [[-0.15, 0.28], [0.26, 0.24], 0, 0.44]
]
a=[[0, 0],[0, 0.16], 0, 0]
x = np.array(a)
# Initialize the starting point
x, y = 0, 0

# Initialize lists to store the x and y coordinates
x_points = [x]
y_points = [y]

# Perform the iterations
for _ in range(50000):
    # Choose a random transformation
    function = np.random.choice([0,1,2,3], p=[0.01, 0.85, 0.07, 0.07])
    # Apply the transformation
    x, y = np.dot(functions[function][:2], [x, y]) + functions[function][2:]

    x_points.append(x)
    y_points.append(y)

# Plot the Barnsley Fern
plt.scatter(x_points, y_points, color='green', s=0.2)
plt.show()
