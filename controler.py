
import os
import numpy as np
from subcode.main import generateDravesIFS, read_data


class controleur:

    def __init__(self):
        self.folder_path = 'ifs_files'
        self.available_files = os.listdir(self.folder_path)
        self.compile_generator()  # Compile the generator function before the main loop

    def compile_generator(self):  # Compile the gen. func before the main loop
        '''
        Compiles the generator function for the first time,
        to avoid the delay when the button is first pressed
        '''
        coeffs_sample = np.random.rand(10, 2, 2)
        sums_sample = np.random.rand(10, 2)
        probabilities_sample = np.random.rand(10)
        generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, 0)

    def lecture_data(self, file):
        return read_data(file)

    def genereatepoints(self, coeffs, sums, probs):
        return (generateDravesIFS(coeffs, sums, probs, 250000))  # generate points
