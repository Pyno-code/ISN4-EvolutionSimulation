import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from backend.simulation import Simulation
import tkinter as tk
from frontend.display import Display
from frontend.graphiques import Graphiques



class SimulationInterface(ttk.Window):
    def __init__(self, simulation):
        super().__init__(themename ="flatly")
        self.title("Simulation Évolutive")
        self.state("zoomed")

        self.simulation = simulation
        self.etat_start = False  # démarrage

        self.style.configure("Graph.TFrame", background="black", borderwidth=1, relief="solid")
        self.couleur_bande = "#e1e1e1"

        self.simulation.update_map_dimensions(width=800, height=600)  

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.creer_interfaces()
        self.update_info_labels()


        self.running = True

        # self.after(0, self.init_taille_zone_centrale) # pour avoir la taille en pixel de la zone centrale

    
    def update(self):
        if self.running:
            super().update()
            self.update_info_labels()
            self.display.update()
            self.graphiques.update_graph()

    def on_close(self):
        print("Fermeture propre")
        self.running = False
        self.destroy()

    def start_simulation(self):
        self.etat_start = True
        self.simulation.initialize()
        self.simulation.resume()
        self.info_content.config(text="Simulation démarrée.")
        self.update_info_labels()

    def update_info_labels(self):
        nb_survivants = self.simulation.get_number_entity()
        nb_nourriture = self.simulation.get_number_nourriture()
        
        # if hasattr(self, 'label_survivants'):
        #     self.label_survivants.config(text=f"Nb survivants: {nb_survivants}")
        #     self.label_nourriture.config(text=f"Nb nourriture: {nb_nourriture}")
        

    def reset_simulation(self):
        self.etat_start = False
        
        self.bouton_pause_play.config(text = "Pause")
        self.simulation.update_number_entity(20)
        self.simulation.update_number_nourriture(20)
        self.slider_nb.set(20)
        self.info_content.config(text="Simulation réinitialisée. Prêt à démarrer.")
        self.update_info_labels()
        self.graphiques.clear_graphique()

    def toggle_pause_play(self):
        if not self.etat_start:
            Messagebox.show_warning(
                "Vous devez d'abord cliquer sur Démarrer.", 
                "Erreur !", 
                parent=self
            )
            return

        if self.bouton_pause_play["text"] == "Pause":
            self.bouton_pause_play.config(text="Reprendre")
            self.simulation.pause()
            self.info_content.config(text="Simulation en pause.")
        else:
            self.bouton_pause_play.config(text="Pause")
            self.simulation.resume()
            self.info_content.config(text="Simulation reprise.")
        self.update_info_labels()

    def creer_interfaces(self):
        self.creer_bande_gauche()
        self.creer_bande_droite()
        self.creer_zone_centrale()
        self.creer_bande_bas()



    def creer_bande_gauche(self):
        self.interf_gauche = ttk.Frame(self, style="Card.TFrame", borderwidth=1, relief="solid")
        self.interf_gauche.place(relx=0, rely=0, relwidth=0.15, relheight=1.0)

        ttk.Label(
            self.interf_gauche, 
            text="Contrôles", 
            font=("Segoe UI", 12, "bold"),  
            style="Card.TLabel"
        ).grid(row=0, column=0, pady=10, sticky="nswe", padx=10)

        # Modification des commandes des boutons
        self.btn_demarrer = ttk.Button(
            self.interf_gauche, 
            text="Démarrer", 
            command=self.start_simulation,
            bootstyle="success"
        )
        self.btn_demarrer.grid(row=1, column=0, pady=5, sticky="nswe", padx=10)

        self.btn_redemarrer = ttk.Button(
            self.interf_gauche, 
            text="Reset", 
            command=self.reset_simulation,
            bootstyle="warning"
        )
        self.btn_redemarrer.grid(row=2, column=0, pady=5, sticky="nswe", padx=10)

        ttk.Label(self.interf_gauche, text="Vitesse :").grid(row=3, column=0, pady=(10, 0), sticky="w", padx=10)
        
        frame_vitesse = ttk.Frame(self.interf_gauche)
        frame_vitesse.grid(row=4, column=0, pady=5, sticky="nswe", padx=10)
        
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

        # Modification du bouton pause/play
        self.bouton_pause_play = ttk.Button(
            self.interf_gauche, 
            text="Pause", 
            command=self.toggle_pause_play,
            bootstyle="secondary"
        )
        self.bouton_pause_play.grid(row=5, column=0, pady=10, sticky="nswe", padx=10)

        ttk.Separator(self.interf_gauche, orient='horizontal').grid(row=6, column=0, sticky="nswe", pady=10, padx=10)

        self.info_label = ttk.Label(
            self.interf_gauche, 
            text="Informations sur la simulation",
            font=("Segoe UI", 10, "bold")
        )
        self.info_label.grid(row=7, column=0, pady=5, sticky="nswe", padx=10)

        # Ajout des labels d'information
        self.label_survivants = ttk.Label(
            self.interf_gauche,
            text="Nb survivants: 0",
            font=("Segoe UI", 9)
        )
        self.label_survivants.grid(row=8, column=0, pady=2, sticky="nswe", padx=10)

        self.label_nourriture = ttk.Label(
            self.interf_gauche,
            text="Nb nourriture: 0",
            font=("Segoe UI", 9)
        )
        self.label_nourriture.grid(row=9, column=0, pady=2, sticky="nswe", padx=10)

        self.info_content = ttk.Label(
            self.interf_gauche,
            text="Prêt à démarrer",
            font=("Segoe UI", 9)
        )
        self.info_content.grid(row=10, column=0, pady=5, sticky="nswe", padx=10)

        self.bouton_quitter = ttk.Button(
            self.interf_gauche, 
            text="Quitter", 
            command=self.on_close,
            bootstyle="danger"
        )
        self.bouton_quitter.grid(row=11, column=0, pady=10, sticky="nswe", padx=10)
    # rajout  de   creer_zone_centrale, creer_bande_droite, creer_bande_bas
    def creer_zone_centrale(self):
        self.zone_centrale = ttk.Frame(self, style="Card.TFrame", borderwidth=1, relief="solid")
        self.zone_centrale.place(relx=0.15, rely=0.0, relwidth=0.55, relheight=0.92)

        self.canvas = ttk.tk.Canvas(
            self.zone_centrale,
            bg="white",
            highlightthickness=0
        )
        self.display = Display(self.zone_centrale, self.simulation)


    def creer_bande_droite(self):
        self.interf_droite = ttk.Frame(self, style="Card.TFrame", borderwidth=1, relief="solid")
        self.interf_droite.place(relx=0.7, rely=0, relwidth=0.3, relheight=1.0)

        self.graphiques = Graphiques(self.interf_droite, self.simulation)

    def creer_bande_bas(self):
        self.interf_bas = ttk.Frame(self, style="Card.TFrame", borderwidth=1, relief="solid")
        self.interf_bas.place(relx=0.15, rely=0.92, relwidth=0.55, relheight=0.08)

        # Déplacer les contrôles vers la gauche (colonne 0)
        frame_nb = ttk.Frame(self.interf_bas)
        frame_nb.grid(row=0, column=0, padx=10, pady=30, sticky="ew")
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
        frame_width.grid(row=0, column=1, padx=10, pady=30, sticky="ew")
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
                self.label_width_value.config(text=str(int(float(val)))),
                self.display.update_width(int(float(val))),
            ]
        )
        self.slider_largeur.set(800)
        self.slider_largeur.pack(side="left", fill="x", expand=True)

        frame_length = ttk.Frame(self.interf_bas)
        frame_length.grid(row=0, column=2, padx=10, pady=30, sticky="ew")
        ttk.Label(frame_length, text="Longueur:").pack(side="left")
        self.label_length_value = ttk.Label(frame_length, text="600", width=5)
        self.label_length_value.pack(side="left")
        self.slider_longueur = ttk.Scale(
            frame_length,
            from_=100,
            to=900,
            orient="horizontal",
            command=lambda val: [
                self.simulation.update_map_dimensions(self.simulation.width, int(float(val))),
                self.label_length_value.config(text=str(int(float(val)))),
                self.display.update_height(int(float(val)))
            ]
        )
        self.slider_longueur.set(600)
        self.slider_longueur.pack(side="left", fill="x", expand=True)

        # Configurer le poids des colonnes dans interf_bas
        self.interf_bas.grid_columnconfigure(0, weight=1)
        self.interf_bas.grid_columnconfigure(1, weight=1)
        self.interf_bas.grid_columnconfigure(2, weight=1)

    def init_taille_zone_centrale(self):
        self.update_idletasks()  # force un rendu à jour
        self.largeur_bande_centrale = self.winfo_width()*0.55
        self.hauteur_bande_centrale = self.winfo_height()*0.92
        print(f"Taille zone centrale: {self.largeur_bande_centrale}x{self.hauteur_bande_centrale}") 

    
    

if __name__ == "__main__":
    sim = Simulation(fps=60)
    app = SimulationInterface(sim)
    app.mainloop()