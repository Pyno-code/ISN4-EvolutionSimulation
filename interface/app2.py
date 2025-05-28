import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from simulation import Simulation
from entity import Entity
from nourriture import Nourriture

class SimulationInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Évolutive (Vista-style theme)")
        self.root.state("zoomed")

        # Utilisation d'un thème clair proche de Vista
        self.style = self.root.style
        self.style.theme_use("flatly")
        self.style.configure("Graph.TFrame", background="black", borderwidth=1, relief="solid")

        self.couleur_bande = "#e1e1e1"

        self.simulation = Simulation(fps=60)
        self.simulation.update_map_dimensions(width=800, height=600)

        self.creer_interfaces()

    def creer_interfaces(self):
        self.creer_bande_gauche()
        self.creer_zone_centrale()
        self.creer_bande_droite()
        self.creer_bande_bas()

    def creer_bande_gauche(self):
        self.interf_gauche = ttk.Frame(self.root, width=420, style="Card.TFrame")
        self.interf_gauche.pack(side="left", fill="y", padx=5, pady=5)

        ttk.Label(
            self.interf_gauche, 
            text="Contrôles", 
            font=("Segoe UI", 12, "bold"),  
            style="Card.TLabel"
        ).pack(pady=10)

        self.btn_demarrer = ttk.Button(
            self.interf_gauche, 
            text="Démarrer", 
            command=self.simulation.resume,
            bootstyle="success"
        )
        self.btn_demarrer.pack(pady=5, fill="x", padx=10)

        self.btn_redemarrer = ttk.Button(
            self.interf_gauche, 
            text="Redémarrer", 
            command=self.simulation.initialize
        )
        self.btn_redemarrer.pack(pady=5, fill="x", padx=10)

        ttk.Label(self.interf_gauche, text="Vitesse :").pack(pady=(10, 0))
        frame_vitesse = ttk.Frame(self.interf_gauche)
        frame_vitesse.pack(pady=5, fill="x", padx=10)
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
        self.bouton_pause_play.pack(pady=10, fill="x", padx=10)

        ttk.Separator(self.interf_gauche, orient='horizontal').pack(fill='x', pady=10)

        self.bouton_quitter = ttk.Button(
            self.interf_gauche, 
            text="Quitter", 
            command=self.root.quit,
            bootstyle="danger"
        )
        self.bouton_quitter.pack(side="bottom", pady=10, fill="x", padx=10)

        self.info_label = ttk.Label(
            self.interf_gauche, 
            text="Informations sur la simulation",
            font=("Segoe UI", 10, "bold")
        )
        self.info_label.pack(pady=5)

        self.info_content = ttk.Label(
            self.interf_gauche,
            text="Prêt à démarrer",
            font=("Segoe UI", 9)
        )
        self.info_content.pack(pady=5)

    def creer_zone_centrale(self):
        self.zone_centrale = ttk.Frame(self.root, style="Card.TFrame")
        self.zone_centrale.pack(expand=True, fill="both", padx=5, pady=5)

        self.canvas = ttk.tk.Canvas(
            self.zone_centrale, 
            bg="white", 
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill="both")

    def creer_bande_droite(self):
        self.interf_droite = ttk.Frame(self.root, width=2000, style="Card.TFrame")
        self.interf_droite.pack(side="right", fill="y", padx=5, pady=5)

        ttk.Label(
            self.interf_droite,
            text="Graphiques en temps réel",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=10)

        self.graph_frame1 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame1.pack(fill="x", padx=10, pady=5)

        self.graph_frame2 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame2.pack(fill="x", padx=10, pady=5)

        self.graph_frame3 = ttk.Frame(
            self.interf_droite,
            style="Graph.TFrame",
            height=200
        )
        self.graph_frame3.pack(fill="x", padx=10, pady=5)

    def creer_bande_bas(self):
        self.interf_bas = ttk.Frame(self.root, height=150, style="Card.TFrame")
        self.interf_bas.pack(side="bottom", fill="x", padx=5, pady=5)

        frame_nb = ttk.Frame(self.interf_bas)
        frame_nb.pack(side="left", padx=10, pady=5, fill="x", expand=True)
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
        frame_width.pack(side="left", padx=10, pady=5, fill="x", expand=True)
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
        frame_length.pack(side="left", padx=10, pady=5, fill="x", expand=True)
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

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = SimulationInterface(root)
    root.mainloop()