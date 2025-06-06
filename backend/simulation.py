import time
import random
import numpy as np
from backend.entity import Entity
from backend.nourriture import Nourriture
from tkinter import Canvas
from logger import SimulationLogger

class Simulation():
    def __init__(self, fps=60, max_loop=1000):
        self.entities = []
        self.nourritures = []

        self.data = {}

        self.fps = fps
        self.time_step = 1 / fps
        self.running = True
        self.number_loop = 0

        self.number_entity = 0
        self.number_nourriture = 0

        self.height = 0
        self.width = 0
        
        self.current_time = 0

        self.running = False
        self.initialized = False

        self.last_update_time = None

        self.max_loop = max_loop

        # self.logger = SimulationLogger(sim_number=1)


    def get_time(self):
        # return self.current_time
        return (self.number_loop * self.time_step)
    
    def get_current_time(self):
        return self.current_time

    def get_fps(self):
        return self.fps
    
    def get_number_entity(self):
        return len(self.entities)
        return random.randint(0, 100)
    
    def get_number_nourriture(self):
        return len(self.nourritures)
        return random.randint(0, 100)

    def get_map_dimensions(self):
        return self.width, self.height

    def update_fps(self, fps):
        self.fps = fps
        self.time_step = 1 / fps
        for entity in self.entities:
            entity.update_fps(fps)
    
    def update_speed(self, speed):
        for entity in self.entities:
            entity.update_kv(speed)
    
    def update_number_entity(self, number):
        self.number_entity = number

    def update_number_nourriture(self, number):
        self.number_nourriture = number

    def update_map_dimensions(self, width, height):
        self.width = width
        self.height = height

    def initialize(self):
        self.initialize_entities()
        self.initialize_nourritures()
        self.initialized = True

        print(f"Simulation parameters:\n"
            f"FPS: {self.fps}\n"
            f"Number of Entities: {self.number_entity}\n"
            f"Number of Nourritures: {self.number_nourriture}\n"
            f"Map Dimensions: {self.width}x{self.height}")

    def initialize_time(self):
        self.current_time = 0

    def initialize_entities(self):
        while len(self.entities) < self.number_entity:
            self.add_entity()
        for entity in self.entities:
            entity.set_entities(self.entities)
            entity.set_nourritures(self.nourritures)

    def initialize_nourritures(self):
        while len(self.nourritures) < self.number_nourriture:
            self.add_nourriture()
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)

    def reset(self):
        self.entities.clear()
        self.nourritures.clear()
        self.running = False
        self.initialized = False
        self.number_loop = 0
        self.last_update_time = None

        print("Simulation reset.")


    def add_entity(self):
        current_entity = Entity(id=len(self.entities), width=self.width, height=self.height, fps=self.fps, x=random.randint(0, self.width), y=random.randint(0, self.height), level=1)
        self.entities.append(current_entity)

    def add_nourriture(self):
        current_nourriture = Nourriture(id=len(self.nourritures), width=self.width, height=self.height, x=random.randint(0, self.width), y=random.randint(0, self.height))
        self.nourritures.append(current_nourriture)
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)

    def update_entity(self):
        for entity in self.entities:
            if entity.exist:
                entity.update()
                # self.record_entities(entity)
            else:
                self.entities.remove(entity)

    def update_nouriture(self):
        for nourriture in self.nourritures:
            if not nourriture.exist:
                self.nourritures.remove(nourriture)
        
    def update(self):
        if self.running:
            # self.logger.add_frame(timestamp=self.get_time())  

            self.update_entity()
            self.update_nouriture()   
            # self.logger.save_frame()
            self.number_loop += 1
            self.last_update_time = time.time()
            if self.number_loop > self.max_loop:
                self.stop()

    
    def record_entities(self, entity): # permet d'enregeistrer toutes les postions dans le logger
        self.logger.add_entity(entity_id=entity.id, position=[entity.x, entity.y], level=entity.level)
        
    def record_nouritures(self, nourriture):
        self.logger.add_food(entity_id=nourriture.id, position=[nourriture.x, nourriture.y])

    def pause(self):
        self.running = False
        print("Simulation paused.")

    def resume(self):
        print("Resuming started...")
        self.last_update_time = time.time()
        self.running = True

    def stop(self):
        self.running = False
        self.initialized = False
        print("Simulation stopped.")

    def total_energy(self):
        total_energy = sum(entity.get_energy() for entity in self.entities) + sum(nourriture.get_energy() for nourriture in self.nourritures)
        return total_energy

    def save_data(self):  
        with open('simulation_data.txt', 'w') as f:
            for entry in self.data:
                f.write(f"{entry}\n")

if __name__ == "__main__":
    # TODO:

    canvas = Canvas()
    sim = Simulation(fps=30)
    sim.add_entity(Entity(id=1, canvas=canvas, x=10, y=50, level=2))
    sim.add_nourriture(Nourriture(id=1, canvas=canvas, x=100, y=100))
    sim.save_data()