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
        )
        self.btn_demarrer.grid(row=1, column=0, pady=5, sticky="ew", padx=10)

        # Bouton Redémarrer
        self.btn_redemarrer = ttk.Button(
            self.interf_gauche, 
            text="Redémarrer", 
            command=self.reset_simulation,
            bootstyle="warning"
        )
        self.btn_redemarrer.grid(row=2, column=0, pady=5, sticky="ew", padx=10)

        # Contrôle de vitesse
        ttk.Label(self.interf_gauche, text="Vitesse :").grid(row=3, column=0, pady=(10, 0), sticky="w", padx=10)
        
        frame_vitesse = ttk.Frame(self.interf_gauche)
        frame_vitesse.grid(row=4, column=0, pady=5, sticky="ew", padx=10)
        
        self.label_vitesse_value = ttk.Label(frame_vitesse, text="100%", width=5)
        self.label_vitesse_value.pack(side="right")
        
        self.slider_vitesse = ttk.Scale(
            frame_vitesse, 
            from_=10, 
            to=500, 
            command=lambda v: [
                self.simulation.update_fps(float(v)),
                self.label_vitesse_value.config(text=f"{int(float(v))}%")
            ]
        )
        self.slider_vitesse.set(100)
        self.slider_vitesse.pack(side="left", fill="x", expand=True)

        # Bouton Pause/Reprendre
        self.bouton_pause_play = ttk.Button(
            self.interf_gauche, 
            text="Pause", 
            command=self.toggle_pause_play,
            bootstyle="secondary"
        )
        self.bouton_pause_play.grid(row=5, column=0, pady=10, sticky="ew", padx=10)

        ttk.Separator(self.interf_gauche, orient='horizontal').grid(row=6, column=0, sticky="ew", pady=10, padx=10)

        # Informations sur la simulation
        self.info_label = ttk.Label(
            self.interf_gauche, 
            text="Informations sur la simulation",
            font=("Segoe UI", 10, "bold")
        )
        self.info_label.grid(row=7, column=0, pady=5, sticky="w", padx=10)

        # Affichage des statistiques
        self.label_survivants = ttk.Label(
            self.interf_gauche,
            text="Nb survivants: 0",
            font=("Segoe UI", 9)
        )
        self.label_survivants.grid(row=8, column=0, pady=2, sticky="w", padx=10)

        self.label_nourriture = ttk.Label(
            self.interf_gauche,
            text="Nb nourriture: 0",
            font=("Segoe UI", 9)
        )
        self.label_nourriture.grid(row=9, column=0, pady=2, sticky="w", padx=10)

        self.info_content = ttk.Label(
            self.interf_gauche,
            text="Prêt à démarrer",
            font=("Segoe UI", 9)
        )
        self.info_content.grid(row=10, column=0, pady=5, sticky="w", padx=10)

        # Bouton Quitter
        self.bouton_quitter = ttk.Button(
            self.interf_gauche, 
            text="Quitter", 
            command=self.root.quit,
            bootstyle="danger"
        )
        self.bouton_quitter.grid(row=11, column=0, pady=10, sticky="ew", padx=10)

    def creer_zone_centrale(self):
        self.zone_centrale = ttk.Frame(self.root, style="Card.TFrame")
        self.zone_centrale.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.canvas = ttk.tk.Canvas(
            self.zone_centrale, 
            bg="white", 
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")

    def creer_bande_droite(self):
        self.interf_droite = ttk.Frame(self.root, style="Card.TFrame")
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
        self.interf_bas = ttk.Frame(self.root, style="Card.TFrame")
        self.interf_bas.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # Contrôle du nombre d'entités
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

        # Contrôle de la largeur
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
                self.simulation.update_map_dimensions(int(float(val)), self.simulation.get_map_dimensions()[1]),
                self.label_width_value.config(text=str(int(float(val))))
            ]
        )
        self.slider_largeur.set(800)
        self.slider_largeur.pack(side="left", fill="x", expand=True)

        # Contrôle de la longueur
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
                self.simulation.update_map_dimensions(self.simulation.get_map_dimensions()[0], int(float(val))),
                self.label_length_value.config(text=str(int(float(val))))
            ]
        )
        self.slider_longueur.set(600)
        self.slider_longueur.pack(side="left", fill="x", expand=True)

        # Configuration des poids des colonnes
        self.interf_bas.grid_columnconfigure(0, weight=1)
        self.interf_bas.grid_columnconfigure(1, weight=1)
        self.interf_bas.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = SimulationInterface(root)
    root.mainloop()