import random
import math
import time
import tkinter as tk

class Entity:
    

    def __init__(self, id, width, height, fps, x=0, y=0, pos_random = True, level=random.randint(1, 3)):
        self.id = id
        self.level = level
        
        if pos_random:
            self.x, self.y = random.randint(20, width - 20), random.randint(20, height - 20)
        else:
            self.x, self.y = x, y

        self.update_speed()
        self.angle = random.uniform(0, 360)  # Direction aléatoire

        self.width = width
        self.height = height

        
        self.entities = []
        self.nourritures = []

        self.detection_range = (4 - self.level) * 40

        self.exist = True
        self.updating = False

        self.energy = 100 * self.level**1.5


        self.fps = fps
        self.time_step = 1 / fps
        
        self.dx = 0
        self.dy = 0

        self.kv = 1


    def get_energy(self):
        return self.energy

    def check_collision(self):
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < 50:
                    if other.level > self.level:  # Rayon de détection de collision
                        other.update_energy(self.energy)
                        self.delete()
                        other.update_level()
                    else:
                        self.update_energy(other.energy)
                        other.delete()
                        self.update_level()
        for nourriture in self.nourritures:
            distance = math.sqrt((self.x - nourriture.x) ** 2 + (self.y - nourriture.y) ** 2)
            if distance < 50:
                self.update_energy(nourriture.energy)
                self.update_level()
                nourriture.delete()

    def set_entities(self, entities):
        self.entities = entities

    def set_nourritures(self, nourritures):
        self.nourritures = nourritures

    def delete(self):
        if self in self.entities:
            self.entities.remove(self)
            self.exist = False

    def update(self):
        if not self.updating:
            self.updating = True
            entities_in_scope = self.scope_detection_entity()
            nourritures_in_scope = self.scope_detection_nourriture()
            self.update_direction(entities_in_scope, nourritures_in_scope)
            self.update_position()
            self.updating = False
        pass

    def update_direction(self, entities_in_scope, nourritures_in_scope):
        attracted = False
        attract_x, attract_y = 0, 0
        
        for nourriture in nourritures_in_scope:
            attracted = True

            dx = nourriture.x - self.x
            dy = nourriture.y - self.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-6
            direction_angle = math.atan2(dy, dx)
            weight = 1 / (distance**2)

            # Attirance proportionnelle à la distance
            attract_x += weight * math.cos(direction_angle)
            attract_y += weight * math.sin(direction_angle)


        for entity in entities_in_scope:
            dx = entity.x - self.x
            dy = entity.y - self.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-6  # Évite la division par zéro
            direction_angle = math.atan2(dy, dx)

            level_difference = self.level - entity.level
            weight = level_difference / (distance**2)  # Poids basé sur la différence de niveau et la distance
            
            attract_x += weight * math.cos(direction_angle)
            attract_y += weight * math.sin(direction_angle)

            if level_difference != 0:
                attracted = True

        

        
        if attracted and (attract_x != 0 or attract_y != 0):
            self.angle = math.degrees(math.atan2(attract_y, attract_x))
        else:
            self.angle += random.gauss(0, 15)
        
        self.angle %= 360



    def check_position_limit(self):
        if self.x > self.width - 20:
            self.x = self.width - 20 - 1
        elif self.x < 20:
            self.x = 20 + 1
        
        if self.y < 20:
            self.y = 20 + 1
        elif self.y > self.height - 20:
            self.y = self.height - 20 - 1

    def update_position(self):
        self.check_collision()
        self.check_position_limit()


        self.dx = self.speed * self.time_step * self.kv * math.cos(math.radians(self.angle))
        self.dy = self.speed * self.time_step * self.kv * math.sin(math.radians(self.angle))


        new_x = self.x + self.dx
        new_y = self.y + self.dy

        if 20 < new_x < self.width - 20 and 20 < new_y < self.height - 20:
            # self.canvas.coords(self.circle, self.x - 10*self.level, self.y - 10*self.level, self.x + 10*self.level, self.y + 10*self.level)
            # self.canvas.coords(self.direction_line, new_x, new_y,
            #                 new_x + 30 * math.cos(math.radians(self.angle)),
            #                 new_y + 30 * math.sin(math.radians(self.angle)))
            self.x += self.dx
            self.y += self.dy

    def scope_detection_entity(self):
        entity_seen = []
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < self.detection_range:
                    entity_seen.append(other)
        return entity_seen
    
    def scope_detection_nourriture(self):
        nourriture_seen = []
        for nourriture in self.nourritures:
            distance = math.sqrt((self.x - nourriture.x) ** 2 + (self.y - nourriture.y) ** 2)
            if distance < self.detection_range:
                nourriture_seen.append(nourriture)
        return nourriture_seen

    def update_kv(self, kv):
        self.kv = kv

    def update_level(self):
        if self.level < 3:
            self.level = int(max(1, min(3, int(self.energy / 7000**(1/1.5)))))
            self.update_speed()
            self.detection_range = (4 - self.level) * 40

    def update_speed(self):
        self.speed = (4 - self.level)*50
    
    def update_fps(self, fps):
        self.fps = fps
        self.time_step = 1 / fps
    
    def update_energy(self, energy):
        self.energy += energy
        if self.energy <= 0:
            self.delete()
        else:
            self.level = int(max(1, min(3, int(self.energy / 7000**(1/1.5)))))