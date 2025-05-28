import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from simulation.simulation import Simulation

matplotlib.use("TkAgg")

class Application:
    def __init__(self, root, simulation): # root c'est le parent, où on enregistre les graphiques
        super().__init__()
        self.simulation = simulation

        # Données
        self.x_data = []
        self.y_data = []
        self.frame_count = 0
        self.running = False

        # Configuration du layout principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frame principale
        main_frame = ttk.Frame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure((0, 1, 2), weight=1)  # Colonnes boutons
        main_frame.rowconfigure(0, weight=1)  # Ligne du graphique

        # Graphique matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Évolution de la population")
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Nombre d'individus")

        # Intégration du graphique dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=3, sticky="nsew", pady=(0, 10))

        self.save_button = ttk.Button(main_frame, text="Télécharger le graphique", command=self.save_graph)
        self.save_button.grid(row=1, column=2, padx=5, pady=5)

    def update_graph(self):

        # Simulation du temps et des données
        t = self.frame_count * 0.1  # Remplacer par self.simulation.get_time() dans ta version finale
        self.x_data.append(t)
        self.y_data.append(self.simulation.get_number_entity())

        if t > 10:
            self.ax.set_xlim(0, t)

        self.line.set_data(self.x_data, self.y_data)
        self.canvas.draw()

        self.frame_count += 1 #à enelver car récup le temps depuis la simulation
        self.after(50, self.update_graph)

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Enregistrer le graphique"
        )
        if file_path:
            self.fig.savefig(file_path)
            print(f"Graphique sauvegardé sous : {file_path}")


