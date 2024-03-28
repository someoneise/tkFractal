import csv
import numpy as np

def generateDravesIFS(param_file:str,iterations:int=50000) -> tuple:
    l2 = []
    with open(param_file, 'r',newline="") as csvfile:
        matrixreader = csv.reader(csvfile, delimiter=' ')
        for row in matrixreader:
            l2.append(row)
        
    rawcoeffs = [i[:4] for i in l2]

    coeffs = [np.asarray([i[:2],i[2:4]]).astype(float) for i in rawcoeffs]

    sums = [np.array([i[4:6]]).astype(float).flatten() for i in l2]

    probabilites = [np.array(i[6]).astype(float) for i in l2]

    pnorm = np.array(probabilites)
    pnorm /= pnorm.sum()  # normalize

    # Initialize lists to store the x and y coordinates
    xy = np.array([ 0.0, 0.0 ])

    c= np.random.random_sample()

    ci = np.linspace(0.0,1.0,len(coeffs),)

    x_points = [xy[0]]
    y_points = [xy[1]]
    c_points = [c]

    # Perform the iterations
    for _ in range(iterations):
        # Choose a random transformation
        function = np.random.choice(range(len(coeffs)), p=pnorm,)

        # Apply the transformation

        xy = np.add(coeffs[function].dot(xy) ,sums[function])

        # Change the color according to Drave's paper

        c = (c+ci[function])/2

        x_points.append(xy[0])
        y_points.append(xy[1])
        c_points.append(c)

    return (x_points,y_points,c_points)