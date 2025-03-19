from simulation import CanvaFrame
import tkinter as tk
import time
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Mettre en plein écran
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))  # Sortie plein écran avec Échap

        # Récupérer dimensions écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Taille de CanvaFrame
        self.window_width = 1280
        self.window_height = 960

        # Centrer CanvaFrame
        offset_x = (screen_width - self.window_width) // 2
        offset_y = (screen_height - self.window_height) // 2
        self.canvas_frame = CanvaFrame(root)
        self.canvas_frame.canvas.place(x=offset_x, y=offset_y)

        # Barre de boutons en bas
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="bottom", fill="x")

        buttons = [
            ("Start", self.start_simulation),
            ("Stop", self.stop_simulation),
            ("Resume", self.resume_simulation),
            ("x1.5", lambda: self.set_speed(1.5)),
            ("x2", lambda: self.set_speed(2)),
            ("x3", lambda: self.set_speed(3)),
            ("x4", lambda: self.set_speed(4))
        ]

        for text, command in buttons:
            btn = tk.Button(self.button_frame, text=text, command=command)
            btn.pack(side="left", expand=True)

        self.info_frame = tk.Frame(root, bg="black")
        self.info_frame.pack(side="top", anchor="ne", padx=10, pady=10)
        
        self.fps_label = tk.Label(self.info_frame, text="FPS: 0", font=("Arial", 14), fg="white", bg="black")
        self.fps_label.pack(anchor="ne", pady=5)  # Label FPS
        self.entities_label = tk.Label(self.info_frame, text="Entities: 0", font=("Arial", 14), fg="white", bg="black")
        self.entities_label.pack(anchor="ne", pady=5)  # Label Entities

        # Graphique à gauche
        # Mise à jour FPS
        self.update()

    def update(self):
        self.fps_label.config(text=f"FPS: {int(self.canvas_frame.get_fps())}")
        self.entities_label.config(text=f"Entities: {int(self.canvas_frame.get_number_entity())}")
        self.root.after(1000, self.update)

    def start_simulation(self):
        print("Simulation Start")

    def stop_simulation(self):
        print("Simulation Stopped")

    def resume_simulation(self):
        print("Simulation Resumed")

    def set_speed(self, speed):
        print(f"Speed set to x{speed}")
