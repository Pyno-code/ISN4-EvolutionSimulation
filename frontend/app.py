import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from backend.simulation import Simulation
from backend.entity import Entity
from backend.nourriture import Nourriture
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SimulationInterface(ttk.Window):
    def __init__(self, simulation):
        super().__init__(themename="flatly")  # Choisis ton thème ici : 'flatly', 'darkly', etc.

        self.title("Simulation Évolutive (Bootstrap-style theme)")
        self.state("zoomed")

        self.simulation = simulation

        # Tu peux accéder au style via self.style
        self.style.configure("Graph.TFrame", background="black", borderwidth=1, relief="solid")

        self.couleur_bande = "#e1e1e1"

        self.simulation = Simulation(fps=60)
        self.simulation.update_map_dimensions(width=800, height=600)

        self.creer_interfaces()


    def creer_interfaces(self):
        # Configuration des poids des colonnes
        self.grid_columnconfigure(0, weight=1)  # Colonne gauche (1/5)
        self.grid_columnconfigure(1, weight=3)  # Colonne centrale (3/5)
        self.grid_columnconfigure(2, weight=1)  # Colonne droite (1/5)
        self.grid_rowconfigure(0, weight=1)     # Ligne principale
        self.grid_rowconfigure(1, weight=0)     # Ligne du bas (pour les contrôles)

        self.creer_bande_gauche()
        self.creer_zone_centrale()
        self.creer_bande_droite()
        self.creer_bande_bas()

    def creer_bande_gauche(self):
        self.interf_gauche = ttk.Frame(self, style="Card.TFrame")
        self.interf_gauche.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.interf_gauche.grid_propagate(False)

        ttk.Label(
            self.interf_gauche, 
            text="Contrôles", 
            font=("Segoe UI", 12, "bold"),  
            style="Card.TLabel"
        ).grid(row=0, column=0, pady=10, sticky="ew", padx=10)

        self.btn_demarrer = ttk.Button(
            self.interf_gauche, 
            text="Démarrer", 
            command=self.simulation.resume,
            bootstyle="success"
        )
        self.btn_demarrer.grid(row=1, column=0, pady=5, sticky="ew", padx=10)

        self.btn_redemarrer = ttk.Button(
            self.interf_gauche, 
            text="Redémarrer", 
            command=self.simulation.initialize
        )
        self.btn_redemarrer.grid(row=2, column=0, pady=5, sticky="ew", padx=10)

        ttk.Label(self.interf_gauche, text="Vitesse :").grid(row=3, column=0, pady=(10, 0), sticky="w", padx=10)
        
        frame_vitesse = ttk.Frame(self.interf_gauche)
        frame_vitesse.grid(row=4, column=0, pady=5, sticky="ew", padx=10)
        
        self.label_vitesse_value = ttk.Label(frame_vitesse, text="100", width=5)
        self.label_vitesse_value.pack(side="right")
        
        self.slider_vitesse = ttk.Scale(
            frame_vitesse, 
            from_=10, 
            to=500, 
            command=lambda v: [
                self.simulation.update_fps(float(v)),
                self.label_vitesse_value.config(text=str(int(float(v))))
            ]
        )
        self.slider_vitesse.set(100)
        self.slider_vitesse.pack(side="left", fill="x", expand=True)

        self.bouton_pause_play = ttk.Button(
            self.interf_gauche, 
            text="Pause", 
            command=self.simulation.pause,
            bootstyle="secondary"
        )
        self.bouton_pause_play.grid(row=5, column=0, pady=10, sticky="ew", padx=10)

        ttk.Separator(self.interf_gauche, orient='horizontal').grid(row=6, column=0, sticky="ew", pady=10, padx=10)

        self.info_label = ttk.Label(
            self.interf_gauche, 
            text="Informations sur la simulation",
            font=("Segoe UI", 10, "bold")
        )
        self.info_label.grid(row=7, column=0, pady=5, sticky="w", padx=10)

        self.info_content = ttk.Label(
            self.interf_gauche,
            text="Prêt à démarrer",
            font=("Segoe UI", 9)
        )
        self.info_content.grid(row=8, column=0, pady=5, sticky="w", padx=10)

        self.bouton_quitter = ttk.Button(
            self.interf_gauche, 
            text="Quitter", 
            command=self.quit,
            bootstyle="danger"
        )
        self.bouton_quitter.grid(row=9, column=0, pady=10, sticky="ew", padx=10)

    def creer_zone_centrale(self):
        self.zone_centrale = ttk.Frame(self, style="Card.TFrame")
        self.zone_centrale.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.canvas = ttk.tk.Canvas(
            self.zone_centrale, 
            bg="white", 
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")

    def creer_bande_droite(self):
        self.interf_droite = ttk.Frame(self, style="Card.TFrame")
        self.interf_droite.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        self.interf_droite.grid_propagate(False)

        ttk.Label(
            self.interf_droite,
            text="Graphiques en temps réel",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, pady=10, sticky="ew")

        self.graph_frame1 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame1.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.graph_frame2 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame2.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        self.graph_frame3 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame3.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    def creer_bande_bas(self):
        self.interf_bas = ttk.Frame(self, style="Card.TFrame")
        self.interf_bas.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # Déplacer les contrôles vers la gauche (colonne 0)
        frame_nb = ttk.Frame(self.interf_bas)
        frame_nb.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Label(frame_nb, text="Nb entités:").pack(side="left")
        self.label_nb_value = ttk.Label(frame_nb, text="20", width=5)
        self.label_nb_value.pack(side="left")
        self.slider_nb = ttk.Scale(
            frame_nb,
            from_=1,
            to=100,
            orient="horizontal",
            command=lambda val: [
                self.simulation.update_number_entity(int(float(val))),
                self.label_nb_value.config(text=str(int(float(val))))
            ]
        )
        self.slider_nb.set(20)
        self.slider_nb.pack(side="left", fill="x", expand=True)

        frame_width = ttk.Frame(self.interf_bas)
        frame_width.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Label(frame_width, text="Largeur:").pack(side="left")
        self.label_width_value = ttk.Label(frame_width, text="800", width=5)
        self.label_width_value.pack(side="left")
        self.slider_largeur = ttk.Scale(
            frame_width,
            from_=100,
            to=1000,
            orient="horizontal",
            command=lambda val: [
                self.simulation.update_map_dimensions(int(float(val)), self.simulation.height),
                self.label_width_value.config(text=str(int(float(val))))
            ]
        )
        self.slider_largeur.set(800)
        self.slider_largeur.pack(side="left", fill="x", expand=True)

        frame_length = ttk.Frame(self.interf_bas)
        frame_length.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        ttk.Label(frame_length, text="Longueur:").pack(side="left")
        self.label_length_value = ttk.Label(frame_length, text="600", width=5)
        self.label_length_value.pack(side="left")
        self.slider_longueur = ttk.Scale(
            frame_length,
            from_=100,
            to=1000,
            orient="horizontal",
            command=lambda val: [
                self.simulation.update_map_dimensions(self.simulation.width, int(float(val))),
                self.label_length_value.config(text=str(int(float(val))))
            ]
        )
        self.slider_longueur.set(600)
        self.slider_longueur.pack(side="left", fill="x", expand=True)

        # Configurer le poids des colonnes dans interf_bas
        self.interf_bas.grid_columnconfigure(0, weight=1)
        self.interf_bas.grid_columnconfigure(1, weight=1)
        self.interf_bas.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    app = Interface()
    app.mainloop()