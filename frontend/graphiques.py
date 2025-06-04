import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from backend.simulation import Simulation



class Graphiques():
    def __init__(self, root, simulation): # root c'est la frame parent, où on enregistre les graphiques
        super().__init__()
        matplotlib.use("TkAgg")
        self.simulation = simulation
        self.root = root
        # Données
        self.x_data = [] 
        self.y_data_1 = []
        self.y_data_2 = []


        self.frame_count = 0
        self.running = False

        # Graphique Évolution de la population, tout les _1
        self.fig_1, self.ax_1 = plt.subplots(figsize=(5, 3.7))
        self.line_1, = self.ax_1.plot([], [], lw=2)
        self.ax_1.set_xlim(0, 10)
        self.ax_1.set_ylim(0, 100)
        self.ax_1.set_title("Évolution de la population")
        self.ax_1.set_xlabel("Temps")
        self.ax_1.set_ylabel("Nombre d'individus")

        # Graphique Evolution de la nourriture, tous les _2
        self.fig_2, self.ax_2 = plt.subplots(figsize=(5, 3.7))
        self.line_2, = self.ax_2.plot([], [], lw=2)
        self.ax_2.set_xlim(0, 10)
        self.ax_2.set_ylim(0, 100)
        self.ax_2.set_title("Évolution de la Nourriture")
        self.ax_2.set_xlabel("Temps")
        self.ax_2.set_ylabel("Quantité de nourriture")

        # Intégration des graphiques dans Tkinter
        self.canvas_1 = FigureCanvasTkAgg(self.fig_1, master=root)
        self.canvas_widget_1 = self.canvas_1.get_tk_widget()
        self.canvas_widget_1.grid(row=1, column=0, sticky="nsew", pady=(0, 0))

        self.canvas_2 = FigureCanvasTkAgg(self.fig_2, master=root)
        self.canvas_widget_2 = self.canvas_2.get_tk_widget()
        self.canvas_widget_2.grid(row=2, column=0, sticky="nsew", pady=(0, 20))

        self.save_button_2 = ttk.Button(root, text="Télécharger le graphique", command=self.save_graph)
        self.save_button_2.grid(row=3, column=0, padx=0, pady=0)

    def save_graph(self):
        self.save_graph_1()
        self.save_graph_2()
    


    def update_graph(self):

        # Simulation du temps et des données
        t = self.simulation.get_time()  # Remplacer par self.simulation.get_time() dans ta version finale
        self.x_data.append(t)
        #self.x_data_2.append(t)
        self.y_data_1.append(self.simulation.get_number_entity())
        self.y_data_2.append(self.simulation.get_number_nourriture())

        if t > 10:
            self.ax_1.set_xlim(0, t) # l'échelle du graphique s'allonge si on est supérieur à 10 secondes
            self.ax_2.set_xlim(0, t)

        self.line_1.set_data(self.x_data, self.y_data_1)
        self.canvas_1.draw()

        self.line_2.set_data(self.x_data, self.y_data_2)
        self.canvas_2.draw()


        self.frame_count += 1 # à enelver car récup le temps depuis la simulation

    def save_graph_1(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="graphique_population.png",  # Nom par défaut
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Enregistrer le graphique"
        )
        if file_path:
            self.fig_1.savefig(file_path)
            print(f"Graphique sauvegardé sous : {file_path}")

    def save_graph_2(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile="graphique_nourriture.png",  # Nom par défaut
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Enregistrer le graphique"
        )
        if file_path:
            self.fig_2.savefig(file_path)
            print(f"Graphique sauvegardé sous : {file_path}")
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulation Graphique")

    # Création d'une simulation factice pour l'exemple
    simulation = Simulation(fps=30)

    app = Graphiques(tk.Frame(), simulation)
    app.update_graph()  # Démarre la mise à jour du graphique
    root.mainloop() 


