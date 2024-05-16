import matplotlib
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import numpy as np
from subcode.data_process import generateDravesIFS, read_data
from matplotlib.figure import Figure


class controleur: 

    def __init__(self):
        self.folder_path = 'ifs_files'
        self.available_files = os.listdir(self.folder_path)
        self.compile_generator() # Compile the generator function before the main loop

    def compile_generator(self):
        '''
        Compiles the generator function for the first time,
        to avoid the delay when the button is first pressed
        '''
        coeffs_sample = np.random.rand(10, 2, 2)
        sums_sample = np.random.rand(10, 2)
        probabilities_sample = np.random.rand(10)
        generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, 0)

            
    def  path(self,frac_entry):    
        filePath = os.path.join(self.folder_path, self.available_files[frac_entry])# Select the file
        if not os.path.isfile(filePath): # Check if file_path is a file
            raise FileNotFoundError
        return filePath
    
    def fractal_possible (self):
        return [f[:-4] for f in self.available_files]
    
    def genereatepoints(self,coeffs,sums,probs):
        return(generateDravesIFS(coeffs,sums,probs,200000)) #generate points