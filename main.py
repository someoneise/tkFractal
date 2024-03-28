import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    #NavigationToolbar2Tk
)
from subcode.data_process import generateDravesIFS

folder_path = 'ifs_files'
available_files = os.listdir(folder_path)
available_fractals = [f[:-4] for f in available_files]
colormaps = ['summer','Pastel1','Pastel2','flag','prism','tab10',]

class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Fractal Designer')

        # example data
        # x, y = generateDravesIFS(file_path,50000)

        # create a figure
        self.figure, self.ax = self.draw_scatter_top(0, 0)

        #create tk widgets
        self.draw_widgets()


    def draw_scatter_top(self, x_points:list, y_points:list, col:str='white'):
        figure = plt.Figure(figsize=(6, 4), dpi=100)
        
        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        ax = plt.Axes(figure,[0., 0., 1., 1.]) # Set the border size to 0
        ax.set_facecolor('black') # Black graph
        ax.autoscale() # Make the ax scale adjust itself

        figure.set_facecolor("black") # All black (can be changed to custom color later)

        figure.add_axes(ax)
        
        scatter = ax.scatter(x_points,y_points) # may be removed later

        ax.set_axis_off() # to remove the axis ticks

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) # make it into tkinter

        return figure, ax # ,scatter
    
    def replot(self,event):
        self.ax.clear() # Clear the figure

        file_path = os.path.join(folder_path, available_files[self.frac_entry.curselection()[0]])# Select the file
        if not os.path.isfile(file_path):
            raise FileNotFoundError
        
        x, y, c = generateDravesIFS(file_path,10000) # Generate the points 

        self.cmap = matplotlib.colormaps[colormaps[self.colormap_entry.curselection()[0]]] # Choose the colormap
        self.ax.scatter(x, y, c=c, s=0.5, linewidths=0, cmap=self.cmap) # Plot the points
        self.figure.canvas.draw() # Update the figure (v too)
        self.figure.canvas.flush_events()

    def draw_widgets(self):
        self.params = tk.Variable(value=available_fractals) # List of available fractals
        self.cmaps = tk.Variable(value=colormaps) # List of available fractals
        
        self.frac_entry = tk.Listbox(self, listvariable=self.params,height=6,selectmode=tk.SINGLE,exportselection=0)
        self.frac_entry.pack(side=tk.LEFT)

        self.colormap_entry = tk.Listbox(self, listvariable=self.cmaps,height=6,selectmode=tk.SINGLE,exportselection=0)
        self.colormap_entry.pack(side=tk.LEFT)

        self.btn_replot = tk.Button(self,text="Generate") # generate button
        self.btn_replot.bind("<Button-1>",func=self.replot) 
        self.btn_replot.pack(side=tk.RIGHT)
        
        self.scale = tk.Scale(orient='horizontal') # Non-functional, just a placeholder
        self.scale.pack()


if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()
    