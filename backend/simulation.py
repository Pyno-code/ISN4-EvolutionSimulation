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
        """
        Retourne le temps actuel de la simulation.

        Cette méthode calcule le temps écoulé en multipliant le nombre de boucles effectuées
        par la valeur de l'intervalle de temps (time_step) de chaque boucle.

        Returns:
            float: Le temps actuel de la simulation.
        """
        # return self.current_time
        return (self.number_loop * self.time_step)
    
    def get_current_time(self):
        """
        Retourne le temps actuel de la simulation.

        Returns:
            float: Le temps courant de la simulation.
        """
        return self.current_time

    def get_fps(self):
        """
        Retourne la valeur actuelle des images par seconde (FPS) de la simulation.

        Returns:
            int: Le nombre d'images par seconde actuellement utilisé dans la simulation.
        """
        return self.fps
    
    def get_number_entity(self):
        """
        Retourne le nombre d'entités présentes dans la simulation.

        Returns:
            int: Le nombre total d'entités.
        """
        return len(self.entities)
    
    def get_number_nourriture(self):
        """
        Retourne le nombre d'objets de nourriture présents dans la simulation.

        Returns:
            int: Le nombre total de nourritures actuel.
        """
        return len(self.nourritures)

    def get_map_dimensions(self):
        """
        Retourne les dimensions de la carte.

        Renvoie :
            tuple : Un tuple contenant la largeur et la hauteur de la carte (width, height).
        """
        return self.width, self.height

    def update_fps(self, fps):
        """
        Met à jour la valeur des images par seconde (fps) pour la simulation et ses entités.

        Paramètres :
            fps (float) : Le nouveau nombre d'images par seconde à appliquer.

        Effets :
            - Met à jour l'attribut fps de la simulation.
            - Calcule et met à jour le pas de temps (time_step) en fonction du fps.
            - Applique la nouvelle valeur de fps à toutes les entités de la simulation.
        """
        self.fps = fps
        self.time_step = 1 / fps
        for entity in self.entities:
            entity.update_fps(fps)
    
    def update_speed(self, speed):
        """
        Met à jour la vitesse de toutes les entités de la simulation.

        Paramètres :
            speed (float) : La nouvelle vitesse à appliquer à chaque entité.
        """
        for entity in self.entities:
            entity.update_kv(speed)
    
    def update_number_entity(self, number):
        """
        Met à jour le nombre d'entités dans la simulation.

        Paramètres :
            number (int) : Le nouveau nombre d'entités à définir.
        """
        self.number_entity = number

    def update_number_nourriture(self, number):
        """
        Met à jour le nombre de nourriture disponible dans la simulation.

        Paramètres :
            number (int) : Le nouveau nombre de nourriture à définir.
        """
        self.number_nourriture = number

    def update_map_dimensions(self, width, height):
        """
        Met à jour les dimensions de la carte de simulation.

        Paramètres :
            width (int) : La nouvelle largeur de la carte.
            height (int) : La nouvelle hauteur de la carte.
        """
        self.width = width
        self.height = height

    def initialize(self):
        """
        Initialise la simulation en créant les entités et les nourritures nécessaires.

        Cette méthode appelle les fonctions d'initialisation des entités et des nourritures,
        puis marque la simulation comme initialisée.
        """
        self.initialize_entities()
        self.initialize_nourritures()
        self.initialized = True

    def initialize_time(self):
        """
        Initialise le temps courant de la simulation à zéro.

        Cette méthode doit être appelée au début de la simulation pour réinitialiser
        le compteur de temps interne.
        """
        self.current_time = 0

    def initialize_entities(self):
        """
        Initialise les entités de la simulation.

        Cette méthode ajoute de nouvelles entités jusqu'à atteindre le nombre spécifié par `self.number_entity`.
        Ensuite, pour chaque entité, elle définit la liste complète des entités et la liste des nourritures disponibles,
        permettant ainsi aux entités d'interagir entre elles et avec leur environnement.

        """
        while len(self.entities) < self.number_entity:
            self.add_entity()
        for entity in self.entities:
            entity.set_entities(self.entities)
            entity.set_nourritures(self.nourritures)

    def initialize_nourritures(self):
        """
        Initialise la liste des nourritures dans la simulation.

        Cette méthode ajoute des objets nourriture jusqu'à atteindre le nombre spécifié par `self.number_nourriture`.
        Ensuite, elle met à jour chaque entité de la simulation en leur fournissant la liste des nourritures disponibles.

        """
        while len(self.nourritures) < self.number_nourriture:
            self.add_nourriture()
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)

    def reset(self):
        """
        Réinitialise la simulation en effaçant toutes les entités et nourritures, 
        en réinitialisant les indicateurs d'état et le compteur de boucles.
        Cette méthode remet la simulation à son état initial, prête à être relancée.
        """
        self.entities.clear()
        self.nourritures.clear()
        self.running = False
        self.initialized = False
        self.number_loop = 0
        self.last_update_time = None

        print("Simulation reset.")


    def add_entity(self):
        """
        Ajoute une nouvelle entité à la simulation.

        Cette méthode crée une instance de la classe Entity avec un identifiant unique,
        des coordonnées aléatoires dans les limites de la simulation, et un niveau initial de 1.
        L'entité est ensuite ajoutée à la liste des entités de la simulation.
        """
        current_entity = Entity(id=len(self.entities), width=self.width, height=self.height, fps=self.fps, x=random.randint(0, self.width), y=random.randint(0, self.height), level=1)
        self.entities.append(current_entity)

    def add_nourriture(self):
        """
        Ajoute un nouvel objet Nourriture à la simulation.

        Cette méthode crée une nouvelle instance de Nourriture avec un identifiant unique et des coordonnées aléatoires dans les limites de la simulation.
        La nouvelle nourriture est ajoutée à la liste des nourritures existantes.
        Ensuite, chaque entité de la simulation est mise à jour pour recevoir la liste actualisée des nourritures.

        """
        current_nourriture = Nourriture(id=len(self.nourritures), width=self.width, height=self.height, x=random.randint(0, self.width), y=random.randint(0, self.height))
        self.nourritures.append(current_nourriture)
        for entity in self.entities:
            entity.set_nourritures(self.nourritures)

    def update_entity(self):
        """
        Met à jour l'état de chaque entité dans la simulation.

        Pour chaque entité présente dans la liste `self.entities` :
            - Si l'entité existe (`entity.exist`), appelle sa méthode `update()` pour mettre à jour son état.
            - Sinon, retire l'entité de la liste `self.entities`.

        Cette méthode permet de maintenir la liste des entités à jour en supprimant celles qui n'existent plus et en actualisant les autres.
        """
        for entity in self.entities:
            if entity.exist:
                entity.update()
            else:
                self.entities.remove(entity)

    def update_nouriture(self):
        """
        Met à jour la liste des nourritures en supprimant celles qui n'existent plus.

        Parcourt toutes les nourritures présentes dans la simulation et retire celles dont l'attribut 'exist' est à False.
        """
        for nourriture in self.nourritures:
            if not nourriture.exist:
                self.nourritures.remove(nourriture)
        
    def update(self):
        """
        Met à jour l'état de la simulation à chaque itération de la boucle principale.
        Si la simulation est en cours d'exécution (`self.running`), cette méthode :
        - Met à jour les entités de la simulation.
        - Met à jour la nourriture présente dans la simulation.
        - Incrémente le compteur de boucles (`self.number_loop`).
        - Met à jour le temps du dernier rafraîchissement.
        - Arrête la simulation si le nombre maximal de boucles est atteint.
        """
        if self.running:

            self.update_entity()
            self.update_nouriture()   
            self.number_loop += 1
            self.last_update_time = time.time()
            if self.number_loop > self.max_loop:
                self.stop()

    def pause(self):
        """
        Met en pause la simulation en définissant l'attribut 'running' à False.

        Cette méthode arrête temporairement l'exécution de la simulation et affiche un message de confirmation dans la console.
        """
        self.running = False
        print("Simulation paused.")

    def resume(self):
        """
        Reprend l'exécution de la simulation en réinitialisant le temps de la dernière mise à jour
        et en définissant l'état de la simulation sur actif.

        Cette méthode affiche un message indiquant la reprise, met à jour l'attribut `last_update_time`
        avec l'heure actuelle, puis définit l'attribut `running` à True pour signaler que la simulation
        est en cours d'exécution.
        """
        print("Resuming started...")
        self.last_update_time = time.time()
        self.running = True

    def stop(self):
        """
        Arrête la simulation en cours.

        Cette méthode met à jour les attributs 'running' et 'initialized' à False,
        indiquant que la simulation n'est plus active ni initialisée. Un message
        de confirmation est affiché dans la console.
        """
        self.running = False
        self.initialized = False
        print("Simulation stopped.")

    def total_energy(self):
        """
        Calcule et retourne l'énergie totale présente dans la simulation.

        Cette méthode additionne l'énergie de tous les entités et de toutes les nourritures
        actuellement présentes dans la simulation.

        Retour:
            float: L'énergie totale disponible (somme des énergies des entités et des nourritures).
        """
        total_energy = sum(entity.get_energy() for entity in self.entities) + sum(nourriture.get_energy() for nourriture in self.nourritures)
        return total_energy

