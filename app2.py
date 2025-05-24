import tkinter as tk
import math
from simulation import Simulation


class CanvaFrame(tk.Canvas):
    def __init__(self, master, simulation):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.simulation: Simulation = simulation

    def update(self):
        for entity in self.simulation.entities:
            self.draw_entity(entity)

    def draw_entity(self, entity):
        x, y = entity.position
        size = entity.size
        color = entity.color
        self.create_oval(x - size, y - size, x + size, y + size, fill=color)
        self.create_line(x, y, x + math.cos(math.radians(entity.angle)) * 20,
                         y + math.sin(math.radians(entity.angle)) * 20, fill="black")
        


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.running = True
        self.title = "ISN4-evolution"
        self.height = 1080
        self.width = 1920
        self.geometry(f"{self.width}x{self.height}")
        self.simulation = Simulation()
        self.canva_frame = CanvaFrame(self, simulation=self.simulation)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update(self):
        self.canva_frame.update()
        super().update()
    
    def on_close(self):
        self.simulation.stop()
        self.destroy()
        self.running = False


if __name__ == "__main__":
    app = App()
    while app.running:
        app.update()
        app.after(1000 // app.simulation.fps)