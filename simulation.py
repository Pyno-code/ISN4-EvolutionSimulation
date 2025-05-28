import time
import random
import numpy as np
from entity import Entity
from nourriture import Nourriture
from tkinter import Canvas

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

        self.start_time = time.time() # doit disparaitre

        self.running = False
        self.initialized = False



    def get_time(self):
        # return self.current_time
        return (time.time() - self.start_time) / 1000
    
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
        self.initialize_entities()
        self.initialize_nourritures()

    def initialize_time(self):
        self.current_time = 0

    def initialize_entities(self):
        while len(self.entities) < self.number_entity:
            self.add_entity()

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
            else:
                self.entities.remove(entity)
        
    def update(self):
        if self.running:
            self.update_entity()
            self.record_data()
            self.number_loop += 1
            
    def record_data(self):
        current_time = self.number_loop * self.time_step
        

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
    # on ne devrais pas avoir besoin de canvas
    # faut qu'on réalise le coeur de la simulation c'est à dire l'update, le spawn et la suppression des entités et de la nourriture
    # et la sauvegarde des données en temps réel

    # chamgement des parametres et des classes des objets de la simulation

    canvas = Canvas()
    sim = Simulation(fps=30)
    sim.add_entity(Entity(id=1, canvas=canvas, x=10, y=50, level=2))
    sim.add_nourriture(Nourriture(id=1, canvas=canvas, x=100, y=100))
    sim.save_data()