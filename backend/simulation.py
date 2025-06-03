import time
import random
import numpy as np
from backend.entity import Entity
from backend.nourriture import Nourriture
from tkinter import Canvas
from logger import SimulationLogger

class Simulation():
    def __init__(self, fps=60):
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


        # self.logger = SimulationLogger(sim_number=1)


    def get_time(self):
        # return self.current_time
        return (self.number_loop * self.time_step)
    
    def get_current_time(self):
        return self.current_time

    def get_fps(self):
        return self.fps
    
    def get_number_entity(self):
        # return len(self.entities)
        return random.randint(0, 100)
    
    def get_number_nourriture(self):
        # return len(self.nourritures)
        return random.randint(0, 100)

    def get_map_dimensions(self):
        return self.width, self.height

    def update_fps(self, fps):
        self.fps = fps
        self.time_step = 1 / fps
    
    def update_number_entity(self, number):
        self.number_entity = number

    def update_number_nourriture(self, number):
        self.number_nourriture = number

    def update_map_dimensions(self, width, height):
        self.width = width
        self.height = height

    def initialize(self):
        self.initialize_nourritures()
        self.initialize_entities()

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

    def add_entity(self):
        current_entity = Entity(id=self.number_entity, canvas=None, x=random.randint(0, self.width), y=random.randint(0, self.height), level=1)
        self.entities.append(current_entity)

    def add_nourriture(self):
        current_nourriture = Nourriture(id=self.number_nourriture, canvas=None, x=random.randint(0, self.width), y=random.randint(0, self.height))
        self.nourritures.append(current_nourriture)
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)

    def update_entity(self):
        for entity in self.entities:
            if entity.exist:
                entity.update()
                self.record_entities(entity)
            else:
                self.entities.remove(entity)

    def update_nouriture(self):
        for nourriture in self.nourritures:
            if nourriture.exist:
                nourriture.update()
                self.record_nouritures(nourriture)
            else:
                self.nourritures.remove(nourriture)
        
    def update(self):
        if self.running:
            if self.last_update_time is None or (time.time() - self.last_update_time) >= self.time_step:
                self.logger.add_frame(timestamp=self.get_time())
                self.update_entity()
                self.update_nouriture()   
                self.logger.save_frame()
                self.number_loop += 1
                self.last_update_time = time.time()


    
    def record_entities(self, entity): # permet d'enregeistrer toutes les postions dans le logger
        self.logger.add_entity(entity_id=entity.id, position=[entity.x, entity.y], level=entity.level)
        
    def record_nouritures(self, nourriture):
        self.logger.add_food(entity_id=nourriture.id, position=[nourriture.x, nourriture.y])

    def pause(self):
        self.running = False

    def resume(self):
        self.running = False
        self.initialized = True

    def stop(self):
        self.running = False
        self.initialized = False

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