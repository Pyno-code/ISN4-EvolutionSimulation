import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from simulation import Simulation

class SimulationInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Évolutive (Vista-style theme)")
        self.root.state("zoomed")
        
        # État de la simulation
        self.etat_start = False
        
        # Utilisation d'un thème clair proche de Vista
        self.style = self.root.style
        self.style.theme_use("flatly")
        self.style.configure("Graph.TFrame", background="black", borderwidth=1, relief="solid")

        self.couleur_bande = "#e1e1e1"

        self.simulation = Simulation(fps=60)
        self.simulation.update_map_dimensions(width=800, height=600)

        self.creer_interfaces()
        self.update_info_labels()  # Mise à jour initiale des informations

    def reset_simulation(self):
        self.etat_start = False
        self.bouton_pause_play.config(text="Pause")
        self.simulation.update_number_entity(20)
        self.simulation.update_number_nourriture(20)
        self.slider_nb.set(20)
        self.update_info_labels()
        self.info_content.config(text="Simulation réinitialisée. Prêt à démarrer.")

    def start_simulation(self):
        self.etat_start = True
        self.update_info_labels()
        self.info_content.config(text="Simulation démarrée.")

    def toggle_pause_play(self):
        if not self.etat_start:
            Messagebox.show_warning(
                "Vous devez d'abord cliquer sur Démarrer.", 
                "Erreur !", 
                parent=self.root
            )
            return

        if self.bouton_pause_play["text"] == "Pause":
            self.bouton_pause_play.config(text="Reprendre")
            self.info_content.config(text="Simulation en pause.")
        else:
            self.bouton_pause_play.config(text="Pause")
            self.info_content.config(text="Simulation reprise.")
        self.update_info_labels()

    def update_info_labels(self):
        # Mise à jour des informations de simulation en utilisant uniquement les fonctions autorisées
        nb_survivants = self.simulation.get_number_entity()
        nb_nourriture = self.simulation.get_number_nourriture()
        
        self.label_survivants.config(text=f"Nb survivants: {nb_survivants}")
        self.label_nourriture.config(text=f"Nb nourriture: {nb_nourriture}")
        
        # Mise à jour périodique
        self.root.after(1000, self.update_info_labels)

    def creer_interfaces(self):
        # Configuration des poids des colonnes
        self.root.grid_columnconfigure(0, weight=1)  # Colonne gauche (1/5)
        self.root.grid_columnconfigure(1, weight=3)  # Colonne centrale (3/5)
        self.root.grid_columnconfigure(2, weight=1)  # Colonne droite (1/5)
        self.root.grid_rowconfigure(0, weight=1)     # Ligne principale
        self.root.grid_rowconfigure(1, weight=0)     # Ligne du bas (pour les contrôles)

        self.creer_bande_gauche()
        self.creer_zone_centrale()
        self.creer_bande_droite()
        self.creer_bande_bas()

    def creer_bande_gauche(self):
        self.interf_gauche = ttk.Frame(self.root, style="Card.TFrame")
        self.interf_gauche.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.interf_gauche.grid_propagate(False)

        ttk.Label(
            self.interf_gauche, 
            text="Contrôles", 
            font=("Segoe UI", 12, "bold"),  
            style="Card.TLabel"
        ).grid(row=0, column=0, pady=10, sticky="ew", padx=10)

        # Bouton Démarrer
        self.btn_demarrer = ttk.Button(
            self.interf_gauche, 
            text="Démarrer", 
            command=self.start_simulation,
            bootstyle="success"