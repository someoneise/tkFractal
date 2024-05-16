import tkinter as tk
import matplotlib
from matplotlib.axes import Axes
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
# from matplotlib.colors import Colormap
import os
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    # NavigationToolbar2Tk,
)
from subcode.data_process import generateDravesIFS, read_data

matplotlib.use('TkAgg')

folder_path = 'ifs_files'
available_files = os.listdir(folder_path)
available_fractals = [f[:-4] for f in available_files]

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

        self.controleur=controleur()  ##lance le controleur
        self.title('Fractal Designer')

        # example data
        # x, y = generateDravesIFS(file_path,50000)

        # create a figure
        self.figure, self.ax = self.draw_scatter_top([0], [0])

        self.compile_generator()  # Compile the gen. func before the main loop

        # create tk widgets
        self.draw_widgets()

    def compile_generator(self):
        '''
        Compiles the generator function for the first time,
        to avoid the delay when the button is first pressed
        '''
        coeffs_sample = np.random.rand(10, 2, 2)
        sums_sample = np.random.rand(10, 2)
        probabilities_sample = np.random.rand(10)
        generateDravesIFS(coeffs_sample, sums_sample, probabilities_sample, 0)

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
        figure = Figure(figsize=(10, 7), dpi=80)

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
        x, y, c = generateDravesIFS(coeffs, sums, probs, 250000)

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
        self.figure.savefig("images/" + available_fractals[selection]+".png")

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

        # grid(column=1,row=2,sticky='ns') vvvvvvvvv
        self.scroll1.pack(side=tk.RIGHT, fill='y')

        # Colormap selection widget
        self.colormap_entry = tk.Listbox(self,
                                         listvariable=self.cmaps,
                                         height=6,
                                         selectmode=tk.SINGLE,
                                         exportselection=0)

        self.colormap_entry.grid(column=2, row=2, rowspan=4, sticky='nsew')

        # Generate button
        self.btn_replot = tk.Button(self, text="(re)Generate")
        self.btn_replot.bind("<Button-1>", func=self.replot)
        self.btn_replot.grid(column=6, row=5)

        # Non-functional, just a placeholder
        self.scale = tk.Scale(orient='vertical')
        self.scale.grid(column=4, row=2)

        # Bouton qui enregistre les fractals en tant qu'image
        self.btn_3 = tk.Button(self, text="Enregistrement en tant qu'image")
        self.btn_3.bind("<Button-1>", self.savefigure)

        # Bouton qui permet de charger des fractals pour pouvoir les modifier
        self.btn_4 = tk.Button(self, text="Importer fractal")
        self.btn_4.grid(column=6, row=2, sticky='wn')
        # self.btn_4.bind("<Button-1>",self.modif)

        # Bouton qui permet de charger des fractals pour pouvoir les modifier
        self.btn_4 = tk.Button(self, text="Navigation")
        self.btn_4.grid(column=6, row=3, sticky='wns')
        # self.btn_4.bind("<Button-1>",self.modif)

        # Bouton qui permet de chrager les fractals
        self.btn_5 = tk.Button(self, text="Enregistrer le nouveau fractal")
        self.btn_5.grid(column=6, row=4, sticky='wns')
        # self.btn_5.bind("<Button-1>",self.save)


if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()
