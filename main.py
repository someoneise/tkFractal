import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    #NavigationToolbar2Tk
)
from subcode.data_process import generateIFS

file_path = 'sierpinski.txt'
available_params = ['sierpinski','leaf','barnsley']

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
        
        scatter = ax.scatter(0,0)
        ax.set_axis_off()

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        return figure, ax # ,scatter
    
    def replot(self,event):
        print("replotting")
        self.ax.clear()
        x, y = generateIFS(available_params[self.entry.curselection()[0]]+".txt",10000)
        self.ax.scatter(x, y, color='white', s=0.5, linewidths=0)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def draw_widgets(self):
        self.params = tk.Variable(value=available_params)
        
        self.entry = tk.Listbox(self, listvariable=self.params,height=6,selectmode=tk.SINGLE)
        self.btn_replot = tk.Button(self,text="generate")

        self.btn_replot.bind("<Button-1>",func=self.replot)
        self.btn_replot.pack(side=tk.RIGHT)
        self.entry.pack(side=tk.LEFT)
        self.scale = tk.Scale(orient='horizontal')
        self.scale.pack()


if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()
    