import csv

params = [
    [0, 0, 0, 0.16, 0, 0, 0.01],
    [0.85, 0.04, -0.04, 0.85, 0, 1.6, 0.85],
    [0.2, -0.26, 0.23, 0.22, 0, 1.6, 0.07],
    [-0.15, 0.28, 0.26, 0.24, 0, 0.44, 0.07]
]

with open('barnsley.txt', 'w', newline='') as csvfile:
    matrixwriter = csv.writer(csvfile, delimiter=' ')
    matrixwriter.writerows(params)
