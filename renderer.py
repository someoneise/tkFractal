import matplotlib.pyplot as plt
import numpy as np
import csv

param_file = 'leaf.txt'

# Define the affine transformations
l2 = []
with open(param_file, 'r', newline="") as csvfile:
    matrixreader = csv.reader(csvfile, delimiter=' ')
    for row in matrixreader:
        l2.append(row)

rawcoeffs = [i[:4] for i in l2]  # Extraire les 4 premiers éléments de chaque ligne de l2

coeffs = [np.asarray([i[:2], i[2:4]]).astype(float) for i in rawcoeffs]  # Convertir les 2 premiers éléments et les 2 derniers éléments de chaque ligne de rawcoeffs en un tableau numpy de type float

sums = [np.array([i[4:6]]).astype(float).flatten() for i in l2]  # Convertir les éléments 5 et 6 de chaque ligne de l2 en un tableau numpy de type float et le mettre à plat

probabilites = [np.array(i[6]).astype(float) for i in l2]  # Convertir le 7ème élément de chaque ligne de l2 en un tableau numpy de type float

# Initialize lists to store the x and y coordinates
xy = np.array([0.0, 0.0])

x_points = [xy[0]]
y_points = [xy[1]]

# Perform the iterations
for _ in range(100000):
    # Choose a random transformation
    function = np.random.choice(range(len(coeffs)), p=probabilites)

    # Apply the transformation

    xy = np.add(coeffs[function].dot(xy), sums[function])

    x_points.append(xy[0])
    y_points.append(xy[1])

# Plot the Barnsley Fern
plt.scatter(x_points, y_points, color='green', s=0.2, marker=',', linewidths=0)
plt.autoscale()
ax = plt.gca()
ax.set_facecolor("black")
plt.show()
