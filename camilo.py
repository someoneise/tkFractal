import tkinter as tk


class ControlWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window # On cree une nouvelle fenetre pour le cotroleur
        self.master.title("Control Window")

        self.control_frame = tk.Frame(master) # On cree un frame pour mettre les boutons dedans
        self.control_frame.pack()

        self.btn_up = tk.Button(self.control_frame, text="⬆", command=self.main_window.move_up)
        self.btn_up.grid(row=0, column=1) # Bouton pour aller en haut

        self.btn_left = tk.Button(self.control_frame, text="⬅", command=self.main_window.move_left)
        self.btn_left.grid(row=1, column=0) # Bouton pour aller a gauche

        self.btn_right = tk.Button(self.control_frame, text="⮕", command=self.main_window.move_right)
        self.btn_right.grid(row=1, column=2) # Bouton pour aller en droite

        self.btn_down = tk.Button(self.control_frame, text="⬇", command=self.main_window.move_down)
        self.btn_down.grid(row=2, column=1) # Bouton pour aller en bas

        self.center_canvas = tk.Canvas(self.control_frame, width=50, height=50) # Canvas pour dessiner un cercle
        self.center_canvas.grid(row=1, column=1)
        self.draw_circle(25, 25, 20) # Cercle esthetique

        self.zoom_frame = tk.Frame(master)
        self.zoom_frame.pack() # Frame pour les boutons de zoom

        self.btn_zoom_in = tk.Button(self.zoom_frame, text="Zoom In", command=self.main_window.zoom_in)
        self.btn_zoom_in.pack(side=tk.LEFT) # bouton zoom in

        self.btn_zoom_out = tk.Button(self.zoom_frame, text="Zoom Out", command=self.main_window.zoom_out)
        self.btn_zoom_out.pack(side=tk.RIGHT) # bouton zoom out


    def draw_circle(self, x, y, radius):
        self.center_canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="white")
        # Fonction qui cree un cercle de rayon radius, centre (x,y)


def main():
    root = tk.Tk()
    app = ControlWindow(root, None)
    root.mainloop() # on demarre le mainloop du window


if __name__ == "__main__":
    main()
