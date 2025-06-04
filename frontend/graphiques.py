import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
import csv
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

        self.x_data = [] # liste avec le temps
        self.y_data_1 = [] # liste avec toutes les valeurs de population
        self.y_data_2 = [] # liste avec les valeurs de nourriture

        self.frame_count = 0
        self.running = False

        # Graphique Évolution de la population, tous les _1
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
        self.canvas_widget_1.grid(row=1, column=0,columnspan=2, sticky="nsew", pady=(0, 0))

        self.canvas_2 = FigureCanvasTkAgg(self.fig_2, master=root)
        self.canvas_widget_2 = self.canvas_2.get_tk_widget()
        self.canvas_widget_2.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 20))

        self.save_button_graph = ttk.Button(root, text="Télécharger les graphiques", command=self.save_graph)
        self.save_button_graph.grid(row=3, column=0, padx=0, pady=0)

        self.save_button_donnees = ttk.Button(root, text="Télécharger les données", command=self.save_data_csv)
        self.save_button_donnees.grid(row=3, column=1, padx=0, pady=0)

    def initialisation_graphique(self): # appelé quand on appuie sur démarrer à intégrer dans app.py
        self.ax_1.set_ylim(0, self.simulation.get_number_entity()) # réajuste les échelles
        self.ax_2.set_ylim(0, self.simulation.get_number_nourriture())

    def update_graph(self): # ajout de nouvelles valeurs dans le graphique
        
        t = self.simulation.get_time()
        self.x_data.append(t)

        self.y_data_1.append(self.simulation.get_number_entity())
        self.y_data_2.append(self.simulation.get_number_nourriture())

        if t > 10: # l'échelle du graphique s'allonge si on est supérieur à 10 secondes
            self.ax_1.set_xlim(0, t) 
            self.ax_2.set_xlim(0, t)

        self.line_1.set_data(self.x_data, self.y_data_1) # mise à jour des datas des graphiques
        self.canvas_1.draw()

        self.line_2.set_data(self.x_data, self.y_data_2)
        self.canvas_2.draw()

    def save_graph(self): # permet l'enregistrement des 2 graphiques depuis un seul bouton
        self.save_graph_1()
        self.save_graph_2()

    def save_graph_1(self): # enregistrement du graphique de population
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
            initialfile="graphique_nourriture.png", 
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Enregistrer le graphique"
        )
        if file_path:
            self.fig_2.savefig(file_path)
            print(f"Graphique sauvegardé sous : {file_path}")
    
    def save_data_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="donnees_simulation.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Enregistrer les données"
        )
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file, delimiter = ';') # delimiteur ; pour l'ouverture sous excel
                    writer.writerow(["Temps", "Population", "Nourriture"])
                    for temps, population, nourriture in zip(self.x_data, self.y_data_1, self.y_data_2):
                        writer.writerow([temps, population, nourriture])
                print(f"Données sauvegardées dans : {file_path}")
                print(self.x_data)
            except Exception as e:
                print(f"Erreur lors de l'enregistrement du fichier CSV : {e}")


    def clear_graphique(self): # appelé lors du reeset
        self.x_data = [] 
        self.y_data_1 = []
        self.y_data_2 = []

        self.update_graph()

        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simulation Graphique")

    # Création d'une simulation factice pour l'exemple
    simulation = Simulation(fps=30)

    app = Graphiques(tk.Frame(), simulation)
    app.update_graph()  # Démarre la mise à jour du graphique
    root.mainloop() 


