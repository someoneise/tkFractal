import tkinter as tk
import tkinter.filedialog
import matplotlib
from matplotlib.axes import Axes
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
# from matplotlib.colors import Colormap
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import numpy as np
from controler import controleur
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    # NavigationToolbar2Tk,
)
from subcode.data_process import generateDravesIFS, read_data

matplotlib.use('TkAgg')

folder_path = 'ifs_files'
available_files = os.listdir(folder_path)
available_fractals = [f[:-4] for f in available_files]

folder_path_new = 'new_files'
available_files_new = os.listdir(folder_path_new)
available_fractals_new = [f[:-4] for f in available_files_new]



dcolors = ["red", "white", "blue"]
drapeau = LinearSegmentedColormap.from_list("drapeau", dcolors)

colormaps = ['summer',
             'autumn',
             'winter',
             'hsv',
             'Set1',
             'nipy_spectral',
             'drapeau',
             'prism',
             'tab10',]


class Fenetre(tk.Tk):
    """
    A class representing the main window of the Fractal Designer application.

    Methods:
    - __init__(): Initializes the main window.
    - compile_generator(): Compiles the generator function for the first time.
    - draw_scatter_top(): Draws the scatter plot on the top of the window.
    - replot(): Clears the figure and replots the scatter plot.
    - draw_widgets(): Draws the widgets on the window.
    """

    def __init__(self):
        """
        Initializes the main window of the Fractal Designer application.
        """
        super().__init__()

        self.controleur = controleur()  # lance le controleur
        self.title('Fractal Designer')

        # example data
        # x, y = generateDravesIFS(file_path,50000)

        # create a figure
        self.figure, self.ax = self.draw_scatter_top([0], [0])

        # create tk widgets
        self.draw_widgets()


    #Ce petit code permet de créer et nommer un nouveau repertoire 
    #(NB : pour nommer le repertoire, il est preferable de ne pas utiliser des majuscules ni d'espaces) 
    #Dans ce dossier / repertoire il est possible de rejouter des documents sous format json ou csv 
    #Ce document json ou csv va contenir 4 points , chaque points possede 3 coordonnée (x,y,couleur) 
    # Source du code : 

    # Source pour charger et sauvegarder le nouveau fractal : https://docs.python.org/fr/3/library/dialog.html
    # Source pour charger et sauvegarder le nouveau fractal : https://pythonbasics.org/tkinter-filedialog/
    # Source pour charger et sauvegarder le nouveau fracatl : https://likegeeks.com/tkinter-filedialog-asksaveasfilename/


    def draw_scatter_top(self,
                         x_points: list,
                         y_points: list,
                         col: str = 'white'):
        """
        Draws the scatter plot on the top of the window.

        Parameters:
        - x_points (list): The x-coordinates of the points.
        - y_points (list): The y-coordinates of the points.
        - col (str): The color of the scatter plot.

        Returns:
        - figure (Figure): The matplotlib figure object.
        - ax (Axes): The matplotlib axes object.
        """
        figure = Figure(figsize=(10, 7), dpi=60)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        ax = Axes(figure, (0., 0., 1., 1.))  # Set the border size to 0
        ax.set_facecolor('black')  # Black graph
        ax.autoscale()  # Make the ax scale adjust itself

        # All black (can be changed to custom color later)
        figure.set_facecolor("black")

        figure.add_axes(ax)  # Add the ax to the figure

        #  scatter = ax.scatter(x_points, y_points)   # removed for now

        ax.set_axis_off()  # to remove the axis ticks

        # make it into tkinter
        figure_canvas.get_tk_widget().grid(
            column=0, row=0, columnspan=7, sticky='nesw'
        )

        return figure, ax  # ,scatter

    def replot(self, event):
        """
        Clears the figure and replots the scatter plot.

        Parameters:
        - event: The event that triggered the replot.
        """
        self.ax.clear()  # Clear the figure

        # Select the file
        selection = self.frac_entry.curselection()[0]
        file_path = os.path.join(folder_path,
                                 available_files[selection])

        if not os.path.isfile(file_path):  # Check if file_path is a file
            raise FileNotFoundError

        # Choosing colormap
        colmap = colormaps[self.colormap_entry.curselection()[0]]

        if colmap == 'drapeau':  # Exception
            self.cmap = drapeau
        else:
            self.cmap = matplotlib.colormaps[colmap]

        # Read the data from the file
        coeffs, sums, probs = read_data(file_path)

        # Generate the points
        x, y, c = self.controleur.genereatepoints(coeffs, sums, probs)

        # Plot the points
        self.ax.scatter(x, y,
                        c=c,
                        s=0.1,
                        linewidths=0,
                        cmap=self.cmap,
                        alpha=1
                        )

        self.figure.canvas.draw()  # Update the figure
        self.figure.canvas.flush_events()

    def savefigure(self, event):
        selection = self.frac_entry.curselection()[0]
        self.figure.savefig("images/" + available_fractals[selection]+".png") # source à rajouter 
    

        
    def Upload(self,event) : 

        def create_directory(directory_name):
            """
            Create a new directory if it doesn't already exist.
            """
            directory_path = Path(directory_name)
            if not directory_path.exists():
                directory_path.mkdir(parents=True, exist_ok=True)
                print(f"Directory '{directory_name}' created.")
            else:
                print(f"Directory '{directory_name}' already exists.")

        def move_files_to_directory(file_list, directory_name):
            """
            Move specified files to the given directory.
            """
            directory_path = Path(directory_name)
            for file in file_list:
                file_path = Path(file)
                if file_path.exists():
                    destination = directory_path / file_path.name
                    file_path.rename(destination)
                    print(f"Moved file '{file_path.name}' to '{directory_name}'.")
                else:
                    print(f"File '{file_path.name}' does not exist.")

        def select_files():
            """
            Open a file dialog to select multiple files.
            """
            files = filedialog.askopenfilenames(title="Select Files")
            return files

        def move_files():
            files = select_files()
            if not files:
                messagebox.showwarning("No files selected", "Please select files to move.")
                return
            
            directory_name = entry.get()
            if not directory_name:
                messagebox.showwarning("No directory name", "Please enter a directory name.")
                return
            
            create_directory(directory_name)
            move_files_to_directory(files, directory_name)
            messagebox.showinfo("Success", "Files moved successfully.")

        # Create the main window
        root = tk.Tk()
        root.title("File Mover")

        # Create a label and entry for the new directory name
        label = tk.Label(root, text="Enter new directory name:")
        label.pack(pady=5)

        entry = tk.Entry(root, width=50)
        entry.pack(pady=5)

        # Create a button to move the files
        button = tk.Button(root, text="Move Files", command=move_files)
        button.pack(pady=20)

        # Run the application
        root.mainloop()

        
    def draw_widgets(self):
        """
        Draws the widgets on the window.

        """
        # List of available fractals
        self.params = tk.Variable(value=available_fractals)

        # List of available colormaps
        self.cmaps = tk.Variable(value=colormaps)

        self.lbl_cmaps = tk.Label(text='Colormaps:')  # Colormap label
        self.lbl_cmaps.grid(column=2, row=1, sticky='w')

        self.lbl_fractals = tk.Label(text='Fractals:')  # Fractal label
        self.lbl_fractals.grid(column=0, row=1, sticky='w')

        # Fractal selection widget
        self.frac_entry = tk.Listbox(self,
                                     listvariable=self.params,
                                     height=6,
                                     selectmode=tk.SINGLE,
                                     exportselection=0)

        self.frac_entry.grid(column=0,
                             row=2,
                             rowspan=4,
                             columnspan=2,
                             sticky='nsew')

        # Fractal scrollbar
        self.scroll1 = tk.Scrollbar(self.frac_entry,
                                    orient='vertical',
                                    command=self.frac_entry.yview)

        self.frac_entry.configure(yscrollcommand=self.scroll1.set)

        # grid(column=1,row=2,sticky='ns') 
        self.scroll1.pack(side=tk.RIGHT, fill='y')


        # List of personalised fractals
        self.params_new = tk.Variable(value=available_fractals_new)

        self.lbl_cmaps.grid(column=2, row=1, sticky='w')

        self.lbl_fractals = tk.Label(text='New_Fractals:')  # New Fractal label
        self.lbl_fractals.grid(column=0, row=1, sticky='w')

        # Fractal selection widget
        self.frac_entry_new = tk.Listbox(self,
                                     listvariable=self.params_new,
                                     height=6,
                                     selectmode=tk.SINGLE,
                                     exportselection=0)

        self.frac_entry_new.grid(column=0,
                             row=2,
                             rowspan=4,
                             columnspan=2,
                             sticky='nsew')

        # Fractal scrollbar
        self.scroll2 = tk.Scrollbar(self.frac_entry_new,
                                    orient='vertical',
                                    command=self.frac_entry_new.yview)

        self.frac_entry_new.configure(yscrollcommand=self.scroll2.set)

        # grid(column=1,row=2,sticky='ns') 
        self.scroll2.pack(side=tk.RIGHT, fill='y')



        # Génère le fractal final
        self.btn_replot = tk.Button(self, text="(re)Generate")
        self.btn_replot.bind("<Button-1>", func=self.replot)
        self.btn_replot.grid(column=6, row=5)

        # Non-functional, just a placeholder
        self.scale = tk.Scale(orient='vertical')
        self.scale.grid(column=4, row=2)

        # Bouton qui enregistre les fractals en tant qu'image
        self.btn_3 = tk.Button(self, text="Enregistrement en tant qu'image")
        self.btn_3.grid(column=6, row=1, sticky='wn')
        self.btn_3.bind("<Button-1>", self.savefigure)

        # Bouton qui permet de charger des fractals pour pouvoir les modifier
        self.btn_4 = tk.Button(self, text="Importer le nouveau fractal")
        self.btn_4.grid(column=6, row=2, sticky='wn')
        self.btn_4.bind("<Button-1>",self.Upload)
                
        #Bouton qui permet d'ouvrir le navigateur 
        self.btn_4 = tk.Button(self, text="Navigation")
        self.btn_4.grid(column=6, row=3,sticky='wns')
        #self.btn_4.bind("<Button-1>",self.modif)

        # Bouton qui permet de chrager les fractals
        self.btn_5 = tk.Button(self, text="Enregistrer le nouveau fractal")
        self.btn_5.grid(column=6, row=4, sticky='wns')

        #Scale 1 
        #self.s1 = tk.Scale(orient='vertical') 
        #self.s1.grid(column=3, row=2)
        
        #Scale 2 
        #self.s2 = tk.Scale(orient='vertical')
        #self.s2.grid(column=3, row=2)

if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()
