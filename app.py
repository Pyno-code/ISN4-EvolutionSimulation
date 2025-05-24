import tkinter as tk

class Interface(tk.Tk):
    def __init__(self, simulation):
        super().__init__()
        self.running = True
        self.simulation = simulation
        self.title("Interface de simulation")
        self.state("zoomed")
        self.couleur_bande = "#efeff2"

        self.creer_interfaces()
        self.bind("<Configure>", self.ajuster_bouton_quitter)
        self.protocol("WM_DELETE_WINDOW", self.on_close)


    def creer_interfaces(self):
        self.creer_bande_gauche()
        self.creer_bande_droite()
        self.creer_zone_centrale()
        self.creer_bande_bas()

    def creer_bande_gauche(self):
        self.interf_gauche = tk.Frame(self, width=240, bg=self.couleur_bande)
        self.interf_gauche.pack(side="left", fill="y")

        self.zone_infos = tk.Label(self.interf_gauche, text="Infos de simulation", anchor="nw", justify="left")
        self.zone_infos.place(x=10, y=10, width=220, height=120)

        self.btn_demarrer = tk.Button(self.interf_gauche, text="Démarrer la simulation")
        self.btn_demarrer.place(x=20, y=140, width=200, height=30)

        self.btn_redemarrer = tk.Button(self.interf_gauche, text="Redémarrer")
        self.btn_redemarrer.place(x=20, y=180, width=200, height=30)

        self.slider_vitesse = tk.Scale(self.interf_gauche, from_=10, to=500, orient="horizontal", command=self.update_valeur_vitesse)
        self.slider_vitesse.set(100)
        self.slider_vitesse.place(x=10, y=230, width=220)

        self.label_valeur_vitesse = tk.Label(self.interf_gauche, text="100 %")
        self.label_valeur_vitesse.place(x=85, y=270)

        self.bouton_pause_play = tk.Checkbutton(self.interf_gauche, text="Pause / Lecture")
        self.bouton_pause_play.place(x=60, y=310)

        self.bouton_enregistrement = tk.Button(self.interf_gauche, text="Enregistrer l'expérience")
        self.bouton_enregistrement.place(x=10, y=360, width=220, height=30)

        self.bouton_quitter = tk.Button(self.interf_gauche, text="Quitter l'interface", command=self.on_close)
        self.bouton_quitter.place(x=10, y=0, width=220, height=30)

    def ajuster_bouton_quitter(self, event):
        hauteur_gauche = self.interf_gauche.winfo_height()
        self.bouton_quitter.place_configure(y=hauteur_gauche - 50)

    def creer_bande_droite(self):
        self.interf_droite = tk.Frame(self, width=250, bg=self.couleur_bande)
        self.interf_droite.pack(side="right", fill="y")

    def creer_zone_centrale(self):
        self.centre = tk.Frame(self, bg="white")
        self.centre.pack(expand=True, fill="both")

    def creer_bande_bas(self):
        self.interf_bas = tk.Frame(self, height=150, bg="#f0f0f0")
        self.interf_bas.pack(side="bottom", fill="x")

        self.zone_sliders = tk.Frame(self.interf_bas, bg="#f0f0f0")
        self.zone_sliders.pack(side="left", padx=40, pady=20, anchor="nw")

        self.zone_affichage = tk.Frame(self.interf_bas, bg="#f0f0f0")
        self.zone_affichage.pack(side="right", padx=40, pady=20, anchor="ne")

        self.slider_nb = tk.Scale(self.zone_sliders, from_=0, to=100, orient="horizontal", label="Nombre d'individus",
                                  font=("Helvetica", 12), length=400, command=self.update_affichage_parametres)
        self.slider_nb.set(10)
        self.slider_nb.pack(pady=5)

        self.slider_largeur = tk.Scale(self.zone_sliders, from_=0, to=100, orient="horizontal", label="Largeur",
                                       font=("Helvetica", 12), length=400, command=self.update_affichage_parametres)
        self.slider_largeur.set(20)
        self.slider_largeur.pack(pady=5)

        self.slider_longueur = tk.Scale(self.zone_sliders, from_=0, to=100, orient="horizontal", label="Longueur",
                                        font=("Helvetica", 12), length=400, command=self.update_affichage_parametres)
        self.slider_longueur.set(30)
        self.slider_longueur.pack(pady=5)

        tk.Label(self.zone_affichage, text="Paramètres établis", font=("Helvetica", 13, "bold")).pack(anchor="center", pady=(0, 10))
        self.label_largeur = tk.Label(self.zone_affichage, text=f"Largeur : {self.slider_largeur.get()}", font=("Helvetica", 12))
        self.label_largeur.pack(anchor="center", pady=2)

        self.label_longueur = tk.Label(self.zone_affichage, text=f"Longueur : {self.slider_longueur.get()}", font=("Helvetica", 12))
        self.label_longueur.pack(anchor="center", pady=2)

        self.label_nb = tk.Label(self.zone_affichage, text=f"Nombre initial : {self.slider_nb.get()}", font=("Helvetica", 12))
        self.label_nb.pack(anchor="center", pady=2)

    def update_affichage_parametres(self, val=None):
        self.label_largeur.config(text=f"Largeur : {self.slider_largeur.get()}")
        self.label_longueur.config(text=f"Longueur : {self.slider_longueur.get()}")
        self.label_nb.config(text=f"Nombre initial : {self.slider_nb.get()}")

    def update_valeur_vitesse(self, val):
        pourcentage = int(float(val))
        self.label_valeur_vitesse.config(text=f"{pourcentage} %")

    def update(self):
        super().update()
    
    def on_close(self):
        self.destroy()
        self.running = False



if __name__ == "__main__":
    app = Interface()
    app.mainloop()
