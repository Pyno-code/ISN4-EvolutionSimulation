import time
import random
import numpy as np
from entity import Entity
from nourriture import Nourriture
from tkinter import Canvas

class Simulation():
    def __init__(self, fps=60):
        self.start_time = time.time()
        self.entities = []
        self.nourritures = []
        self.data = {}
        self.fps = fps
        self.time_step = 1 / fps
        self.running = True
        self.loop = 0

        self.number_entity = 0
        self.number_nourriture = 0

        self.height = 0
        self.width = 0


    def start(self):
        self.initialize()
        self.data = {}
        self.loop = 0
        self.start_time = time.time()
        self.running = True

    def initialize(self):
        self.start_time = time.time()
        self.entities = []
        self.nourritures = []
        self.data = {}
        self.running = True
        self.loop = 0

        self.number_entity = 0
        self.number_nourriture = 0

        self.height = 0
        self.width = 0

    def reset(self):
        self.initialize()
        self.data = {}
        self.loop = 0
        self.start_time = time.time()
        self.running = False
    
    def update_fps(self, fps):
        self.fps = fps
        self.time_step = 1 / fps
    
    def update_number_entity(self, number):
        self.number_entity = number

    def updaate_number_nourriture(self, number):
        self.number_nourriture = number

    def self_update_map_dimensions(self, width, height):
        self.width = width
        self.height = height

    def update(self):
        pass

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_nourriture(self, nourriture):
        self.nourritures.append(nourriture)
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)
    
    def update_entity(self):
        for entity in self.entities:
            if entity.exist:
                entity.update()
            else:
                self.entities.remove(entity)
            
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

    def run_simulation(self, duration):
        self.duration = duration
        first_time = time.time()
        last_time = time.time()
        while self.running:
            if time.time() - last_time >= self.time_step:
                last_time = time.time()
                self.update_entity()
                self.record_data()
                self.loop += 1
                if last_time - first_time >= duration:
                    self.running = False

    def save_data(self):
        with open('simulation_data.txt', 'w') as f:
            for entry in self.data:
                f.write(f"{entry}\n")

if __name__ == "__main__":
    canvas = Canvas()
    sim = Simulation(fps=30)
    sim.add_entity(Entity(id=1, canvas=canvas, x=10, y=50, level=2))
    sim.add_nourriture(Nourriture(id=1, canvas=canvas, x=100, y=100))
    sim.run_simulation(duration=10)
    sim.save_data()