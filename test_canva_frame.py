import tkinter as tk
import random
from display import Display

# Classes factices pour tester l'affichage
class FakeEntity:
    def __init__(self, x, y, dx, dy, level):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.level = level

class FakeFood:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

class FakeSimulation:
    def __init__(self):
        self.entities = []
        self.foods = []

    def randomize(self, width, height, n_entities=5, n_foods=10):
        self.entities = [
            FakeEntity(
                x=random.randint(50, width - 50),
                y=random.randint(50, height - 50),
                dx=random.uniform(-1, 1),
                dy=random.uniform(-1, 1),
                level=random.randint(1, 4)
            ) for _ in range(n_entities)
        ]
        self.foods = [
            FakeFood(
                x=random.randint(10, width - 10),
                y=random.randint(10, height - 10),
                energy=random.randint(1, 16)
            ) for _ in range(n_foods)
        ]

# Boucle principale
def main():
    root = tk.Tk()
    root.title("Test Canvas Simulation")

    sim = FakeSimulation()
    sim.randomize(width=800, height=600)

    display = Display(root, sim, width=800, height=600)

    def refresh():
        sim.randomize(width=800, height=600)
        display.update()
        root.after(1000, refresh)

    refresh()
    root.mainloop()

if __name__ == '__main__':
    main()
