import tkinter as tk
import tkinter.filedialog
import matplotlib
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from tkinter import filedialog, messagebox
from pathlib import Path
import os
from controler import controleur
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from camilo import ControlWindow  # Importar la clase ControlWindow

matplotlib.use('TkAgg')

folder_path = 'ifs_files'
available_files = os.listdir(folder_path)
available_fractals = [f[:-4] for f in available_files]

dcolors = ["red", "white", "blue"]
drapeau = LinearSegmentedColormap.from_list("drapeau", dcolors)

colormaps = ['summer', 'autumn', 'winter', 'hsv', 'Set1', 'nipy_spectral', 'drapeau', 'prism', 'tab10',]


class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controleur = controleur()  
        self.title('Fractal Designer')
        self.figure, self.ax = self.draw_scatter_top([0], [0])
        self.zoom_level = 1.0  # Nivel de zoom inicial

        self.draw_widgets()

    def draw_scatter_top(self, x_points: list, y_points: list, col: str = 'white'):
        figure = Figure(figsize=(10, 7), dpi=60)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        ax = Axes(figure, (0., 0., 1., 1.))  
        ax.set_facecolor('black')  
        ax.autoscale()  
        figure.set_facecolor("black")
        figure.add_axes(ax)  
        ax.set_axis_off()  
        figure_canvas.get_tk_widget().grid(column=0, row=0, columnspan=7, sticky='nesw')
        return figure, ax  

    def replot(self, event):
        self.ax.clear()  
        selection = self.frac_entry.curselection()[0]
        file_path = os.path.join(folder_path, available_files[selection])
        if not os.path.isfile(file_path):  
            raise FileNotFoundError
        colmap = colormaps[self.colormap_entry.curselection()[0]]
        self.cmap = drapeau if colmap == 'drapeau' else matplotlib.colormaps[colmap]
        coeffs, sums, probs = self.controleur.lecture_data(file_path)
        x, y, c = self.controleur.genereatepoints(coeffs, sums, probs)
        self.ax.scatter(x, y, c=c, s=0.1, linewidths=0, cmap=self.cmap, alpha=1)
        self.apply_zoom_pan()  # Aplicar el zoom y el pan
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def savefigure(self, event):
        selection = self.frac_entry.curselection()[0]
        self.figure.savefig("images/" + available_fractals[selection]+".png")

    def Upload(self, event): 
        def create_directory(directory_name):
            directory_path = Path(directory_name)
            if not directory_path.exists():
                directory_path.mkdir(parents=True, exist_ok=True)
                print(f"Directory '{directory_name}' created.")
            else:
                print(f"Directory '{directory_name}' already exists.")

        def move_files_to_directory(file_list, directory_name):
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
        root = tk.Tk()
        root.title("File Mover")
        label = tk.Label(root, text="Enter new directory name:")
        label.pack(pady=5)
        entry = tk.Entry(root, width=50)
        entry.pack(pady=5)
        button = tk.Button(root, text="Move Files", command=move_files)
        button.pack(pady=20)
        root.mainloop()

    def open_control_window(self, event):
        control_window = tk.Toplevel(self)
        ControlWindow(control_window, self)  # Pasar la instancia de Fenetre a ControlWindow

    def draw_widgets(self):
        self.params = tk.Variable(value=available_fractals)
        self.cmaps = tk.Variable(value=colormaps)
        self.lbl_cmaps = tk.Label(text='Colormaps:')  
        self.lbl_cmaps.grid(column=2, row=1, sticky='w')
        self.lbl_fractals = tk.Label(text='Fractals:')  
        self.lbl_fractals.grid(column=0, row=1, sticky='w')
        self.frac_entry = tk.Listbox(self, listvariable=self.params, height=6, selectmode=tk.SINGLE, exportselection=0)
        self.frac_entry.grid(column=0, row=2, rowspan=4, columnspan=2, sticky='nsew')
        self.scroll1 = tk.Scrollbar(self.frac_entry, orient='vertical', command=self.frac_entry.yview)
        self.frac_entry.configure(yscrollcommand=self.scroll1.set)
        self.scroll1.pack(side=tk.RIGHT, fill='y')
        self.colormap_entry = tk.Listbox(self, listvariable=self.cmaps, height=6, selectmode=tk.SINGLE, exportselection=0)
        self.colormap_entry.grid(column=2, row=2, rowspan=4, sticky='nsew')
        self.btn_replot = tk.Button(self, text="(re)Generate")
        self.btn_replot.bind("<Button-1>", func=self.replot)
        self.btn_replot.grid(column=6, row=5)
        self.scale = tk.Scale(orient='vertical')
        self.scale.grid(column=4, row=2)
        self.btn_3 = tk.Button(self, text="Enregistrement en tant qu'image")
        self.btn_3.grid(column=6, row=1, sticky='wn')
        self.btn_3.bind("<Button-1>", self.savefigure)
        self.btn_4 = tk.Button(self, text="Importer le nouveau fractal")
        self.btn_4.grid(column=6, row=2, sticky='wn')
        self.btn_4.bind("<Button-1>", self.Upload)
        self.btn_4 = tk.Button(self, text="Navigation")
        self.btn_4.grid(column=6, row=3, sticky='wns')
        self.btn_4.bind("<Button-1>", self.open_control_window)


    def zoom_in(self):
        self.zoom_level -= 0.2  # Incrementa el nivel de zoom
        self.apply_zoom_pan()

    def zoom_out(self):
        self.zoom_level += 0.2  # Decrementa el nivel de zoom
        self.apply_zoom_pan()

    def apply_zoom_pan(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_range = ((xlim[1] - xlim[0]) / 2) * self.zoom_level
        y_range = ((ylim[1] - ylim[0]) / 2) * self.zoom_level
        self.ax.set_xlim([x_center - x_range, x_center + x_range])
        self.ax.set_ylim([y_center - y_range, y_center + y_range])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def move_up(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0],xlim[1]])
        self.ax.set_ylim([ylim[0]-ylim[0]*0.4,ylim[1]-ylim[0]*0.4])
        self.figure.canvas.draw()


    def move_down(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0],xlim[1]])
        self.ax.set_ylim([ylim[0]+ylim[0]*0.4,ylim[1]+ylim[0]*0.4])
        self.figure.canvas.draw()

    def move_left(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0]+xlim[0]*0.2,xlim[1]+xlim[0]*0.2])
        self.ax.set_ylim([ylim[0],ylim[1]])
        self.figure.canvas.draw()

    def move_right(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.set_xlim([xlim[0]-xlim[0]*0.2,xlim[1]-xlim[0]*0.2])
        self.ax.set_ylim([ylim[0],ylim[1]])
        self.figure.canvas.draw()


if __name__ == '__main__':
    app = Fenetre()
    app.mainloop()