import tkinter as tk

class ControlWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Control Window")

        # Frame para contener los botones de movimiento y el botón centro
        self.control_frame = tk.Frame(master)
        self.control_frame.pack()

        # Botón para mover arriba
        self.btn_up = tk.Button(self.control_frame, text="↑")
        self.btn_up.grid(row=0, column=1)

        # Botón para mover izquierda
        self.btn_left = tk.Button(self.control_frame, text="←")
        self.btn_left.grid(row=1, column=0)

        # Botón para mover derecha
        self.btn_right = tk.Button(self.control_frame, text="→")
        self.btn_right.grid(row=1, column=2)

        # Botón para mover abajo
        self.btn_down = tk.Button(self.control_frame, text="↓")
        self.btn_down.grid(row=2, column=1)

        # Botón en el centro (canvas para dibujar un círculo)
        self.center_canvas = tk.Canvas(self.control_frame, width=50, height=50)
        self.center_canvas.grid(row=1, column=1)
        self.draw_circle(25, 25, 20)

        # Frame para contener los botones de zoom
        self.zoom_frame = tk.Frame(master)
        self.zoom_frame.pack()

        # Botón para zoom in
        self.btn_zoom_in = tk.Button(self.zoom_frame, text="Zoom In")
        self.btn_zoom_in.pack(side=tk.LEFT)

        # Botón para zoom out
        self.btn_zoom_out = tk.Button(self.zoom_frame, text="Zoom Out")
        self.btn_zoom_out.pack(side=tk.RIGHT)

        #Boton para regenerar
        self.btn_regenerate = tk.Button(master, text="Regenerate", width=20)
        self.btn_regenerate.pack(pady=10)

    def draw_circle(self, x, y, radius):
        # Dibujar un círculo en el canvas
        self.center_canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white")

def main():
    root = tk.Tk()
    app = ControlWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
