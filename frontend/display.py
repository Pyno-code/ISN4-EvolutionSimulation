import tkinter as tk


class Display(tk.Canvas):
    def __init__(self, master, simulation, width=800, height=600, **kwargs):
        super().__init__(master, width=width, height=height, bg='white', **kwargs)

        self.pack(expand=True, fill="both")


        self.simulation = simulation
        self.pack()
        self.configure(bg='grey')

    def update(self):
        self.delete("all")
        for entity in self.simulation.entities:
            self.draw_entity(entity)
        for food in self.simulation.foods:
            self.draw_food(food)

    def update_width(self, width):
        self.config(width=width)
        self.center_self()

    def update_height(self, height):
        self.config(height=height)
        self.center_self()

    def draw_entity(self, entity):
        x, y = entity.x, entity.y
        level = getattr(entity, 'level', 1)
        # Rayon dépend du niveau : 10 (lvl1), 20 (lvl2), 30 (lvl3)
        r = 10 + (level - 1) * 10
        # Couleur selon le niveau
        if level == 1:
            color = 'green'
        elif level == 2:
            color = 'red'
        elif level == 3:
            color = 'blue'
        else:
            color = 'gray'
        self.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='black')

        # Affiche une barre pour la direction de déplacement
        dx = getattr(entity, 'dx', 1)
        dy = getattr(entity, 'dy', 0)
        # Normalisation du vecteur direction
        norm = (dx**2 + dy**2) ** 0.5 or 1
        dir_len = r  # Longueur de la barre = rayon
        end_x = x + (dx / norm) * dir_len
        end_y = y + (dy / norm) * dir_len
        self.create_line(x, y, end_x, end_y, fill='black', width=2)

    def draw_food(self, food):
        x, y = food.x, food.y
        r = 2.5  # demi-côté pour un carré de 5x5
        # Calcul du gradient de couleur du jaune (énergie 1) au rouge (énergie 16)
        energy = max(1, min(getattr(food, 'energy', 1), 16))
        # Interpolation linéaire entre jaune (255,255,0) et rouge (255,0,0)
        g = int(255 * (1 - (energy - 1) / 15))
        color = f'#ff{g:02x}00'
        self.create_rectangle(x - r, y - r, x + r, y + r, fill=color, outline='darkred')


    def center_self(self):
        self.place(relx=0.5, rely=0.5, anchor="center")
