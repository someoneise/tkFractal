import os  # Pour interagir avec le système de fichiers, comme lister les fichiers dans un répertoire
import numpy as np  # Pour manipuler des tableaux et matrices de manière efficace
from subcode.modèle import generateDravesIFS, read_data  # Importe les fonctions écrites dans le code modèle qui se trouve dans le sous-répertoire subcode


class controleur:

    def __init__(self):
        '''
        Le constructeur de la classe controleur.Il initialise le chemin du
        dossiercontenant les fichiers IFS (self.folder_path), liste les
        fichiers disponibles dans ce dossier (self.available_files) et compile
        la fonction de générateur pour la première fois en appelant
        self.compile_generator().
        '''
        self.folder_path = 'ifs_files'
        self.available_files = os.listdir(self.folder_path)
        self.compile_generator()  # Compile the generator function before the main loop

    def compile_generator(self):
        '''
        Méthode pour compiler la fonction de générateur avec des données 
        échantillons aléatoires. Cette étape est effectuée pour éviter un 
        délai lors de la première utilisation réelle du générateur

        '''
        coeffs_sample = np.random.rand(10, 2, 2)
        sums_sample = np.random.rand(10, 2)
        probabilities_sample = np.random.rand(10)
        generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, 0)

    def lecture_data(self, file):
        '''
        Méthode pour lire les données d'un fichier spécifié en utilisant la
        fonction read_data. Le fichier à lire est passé en argument (file).
        '''
        return read_data(file)

    def genereatepoints(self, coeffs, sums, probs):
        '''
        Méthode pour générer des points à partir de coefficients (coeffs), de
        sommes (sums) et de probabilités (probs) spécifiés. La fonction 
        generateDravesIFS est appelée avec ces paramètres et un nombre fixe de
        points à générer (250000).
        '''
        return (generateDravesIFS(coeffs, sums, probs, 250000))  # generate points
