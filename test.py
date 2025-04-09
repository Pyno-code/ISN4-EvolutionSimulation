import tkinter as tk
from simulation import CanvaFrame

class TestAppStructure:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Interface")


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Définir la fenêtre à la taille de l'écran
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Configuration des colonnes pour respecter le ratio 1/5 - 3/5 - 1/5
        self.root.columnconfigure(0, weight=1)  # Partie gauche (infos / graphiques)
        self.root.columnconfigure(1, weight=4)  # Partie centrale (simulation)
        self.root.columnconfigure(2, weight=1)  # Partie droite (paramètres)

        # Partie gauche : Infos & Graphiques
        self.left_frame = tk.Frame(self.root, bg="lightgray")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Partie centrale : Simulation
        self.center_frame = tk.Frame(self.root, bg="white")
        self.center_frame.grid(row=0, column=1, sticky="nsew")


        # Partie droite : Paramètres
        self.right_frame = tk.Frame(self.root, bg="lightgray")
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        # Ajout d'exemple de contenu
        tk.Label(self.right_frame, text="Infos & Graphiques", bg="lightgray").pack(pady=10)
        tk.Label(self.center_frame, text="Simulation", bg="white").pack(pady=10)
        tk.Label(self.left_frame, text="Paramètres", bg="lightgray").pack(pady=10)




if __name__ == "__main__":
    root = tk.Tk()
    app = TestAppStructure(root)
    root.mainloop()
