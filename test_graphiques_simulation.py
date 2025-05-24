
# inspiré de https://es.stackoverflow.com/questions/348847/gr%C3%A1ficos-en-tiempo-real-con-matplotlib-y-tkinter

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import simulation as simulation

matplotlib.use("TkAgg")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Evolution de population")
        self.geometry("800x600")

        # Données
        self.x_data = []
        self.y_data = []
        self.frame_count = 0
        self.running = False

        # Figure matplotlib
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_title("Évolution sinusoïdale")
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Amplitude")

        # Intégration dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Frame des boutons
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10)

        self.start_button = ttk.Button(control_frame, text="Démarrer", command=self.start_animation)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Arrêter", command=self.stop_animation)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(control_frame, text="Télécharger le graphique", command=self.save_graph)
        self.save_button.pack(side=tk.LEFT, padx=5)

    def start_animation(self):
        if not self.running:
            self.running = True
            self.update_graph()

    def stop_animation(self):
        self.running = False

    def update_graph(self):
        if not self.running:
            return

        t = self.frame_count * 0.1
        self.x_data.append(t)
        self.y_data.append(simulation.number_entity)

        if t > 10:
            self.ax.set_xlim(t - 10, t)

        self.line.set_data(self.x_data, self.y_data)
        self.canvas.draw()

        self.frame_count += 1
        self.after(50, self.update_graph) # remplacer 50 par le temps récupérer dans la classe simulation

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Enregistrer le graphique"
        )
        if file_path:
            self.fig.savefig(file_path)
            print(f"Graphique sauvegardé sous : {file_path}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
