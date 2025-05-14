import time
import random
import numpy as np
from entity import Entity
from nourriture import Nourriture

class Simulation():
    def __init__(self, fps=60):
        self.start_time = time.time()
        self.entities = []
        self.nourritures = []
        self.data = {s}
        self.fps = fps
        self.time_step = 1 / fps
        self.running = True
        self.loop = 0


    def add_entity(self, entity):
        self.entities.append(entity)
    
    def add_nourriture(self, nourriture):
        self.nourritures.append(nourriture)
    
    def updade_entity(self):
        for entity in self.entity:
            entity.update()
            
    def record_data(self):
        current_time = self.loop * self.time_step
        
    def pause(self):
        self.running = False

    def resume(self):
        self.running = True

    def stop(self):
        self.running = False
        self.save_data()

    def change_fps(self, fps):
        self.fps = fps
        self.time_step = 1 / fps

    def update(self):
        last_time = time.time()
        while self.running:
            if time.time() - last_time >= self.time_step:
                last_time = time.time()
                self.update_entity()
                self.record_data()
                self.loop += 1

    def save_data(self):
        with open('simulation_data.txt', 'w') as f:
            for entry in self.data:
                f.write(f"{entry}\n")

if __name__ == "__main__":
    sim = Simulation(fps=30)
    sim.add_entity(Entity(id=1, level=1, position=[0, 0]))
    sim.add_nourriture(Nourriture(position=[5, 5]))
    sim.run_simulation(duration=10)
    sim.save_data()