import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    #NavigationToolbar2Tk
)
from data_process import generateIFS

file_path = 'sierpinski.txt'

class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Fractal Designer')

        # example data
        x, y = generateIFS(file_path,50000)

        # create a figure
        self.figure, self.ax = self.draw_scatter_top(x, y)

        #create tk widgets
        self.draw_widgets()

    def draw_scatter_top(self, x_points:list, y_points:list, col:str='white'):
        figure = plt.Figure(figsize=(6, 4), dpi=100)
        
        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        ax = plt.Axes(figure,[0., 0., 1., 1.])
        ax.set_facecolor('b')
        ax.autoscale()
        figure.set_facecolor("black")

        figure.add_axes(ax)
        
        ax.scatter(x_points, y_points, color=col, s=0.5, linewidths=0)
        
        ax.set_axis_off()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        return figure, ax

    def draw_widgets(self):
        self.scale = tk.Scale(orient='horizontal')
        self.scale.pack()


if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()
    