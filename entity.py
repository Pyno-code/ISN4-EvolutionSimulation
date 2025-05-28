import random
import math
import time
import tkinter as tk

class Entity:
    

    def __init__(self, id, width, height, x=0, y=0, pos_random = True, level=random.randint(1, 3)):
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


    def check_collision(self):
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < 50:
                    if other.level > self.level:  # Rayon de détection de collision
                        self.delete()
                        other.update_level()
                    else:
                        other.delete()
                        self.update_level()
        for nourriture in self.nourritures:
            distance = math.sqrt((self.x - nourriture.x) ** 2 + (self.y - nourriture.y) ** 2)
            if distance < 50:
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
        # if not self.updating:
        #     self.updating = True
        #     entities_in_scope = self.scope_detection_entity()
        #     self.update_direction(entities_in_scope)
        #     self.update_position()
        #     self.updating = False
        pass

    def update_direction(self, entities_in_scope):
        self.angle += random.gauss(0, 15)  # Biais vers un faible changement
        self.angle %= 360  # Garder entre 0 et 360°
        
        for entity in entities_in_scope:
            dx = entity.x - self.x
            dy = entity.y - self.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-6  # Évite la division par zéro
            direction_angle = math.degrees(math.atan2(dy, dx))

            level_difference = self.level - entity.level
            weight = abs(level_difference) / (distance**2)  # Poids basé sur la différence de niveau et la distance
            
            attract_x, attract_y = 0, 0

            if level_difference > 0:
                # Attirance proportionnelle à la différence de niveau
                attract_x += weight * math.cos(direction_angle)
                attract_y += weight * math.sin(direction_angle)
            elif level_difference < 0:
                # Répulsion proportionnelle à la différence de niveau
                attract_x -= weight * math.cos(direction_angle)
                attract_y -= weight * math.sin(direction_angle)
        else:
            return

        self.angle = math.degrees(math.atan2(attract_y, attract_x)) % 360  # Nouvelle direction

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

        time_delta = time.time() - self.time_last_update
        self.time_last_update = time.time()  # On met à jour AVANT de recalculer dx/dy


        dx = self.speed * time_delta * math.cos(math.radians(self.angle))
        dy = self.speed * time_delta * math.sin(math.radians(self.angle))


        new_x = self.x + dx
        new_y = self.y + dy

        if 20 < self.x < self.width - 20 and 20 < self.y < self.height - 20:
            self.canvas.coords(self.circle, self.x - 10*self.level, self.y - 10*self.level, self.x + 10*self.level, self.y + 10*self.level)
            self.canvas.coords(self.direction_line, new_x, new_y,
                            new_x + 30 * math.cos(math.radians(self.angle)),
                            new_y + 30 * math.sin(math.radians(self.angle)))
            self.x += dx
            self.y += dy

    def scope_detection_entity(self):
        entity_seen = []
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < self.detection_range:
                    entity_seen.append(other)
        return entity_seen

    def update_level(self):
        if self.level < 3:
            self.level += 1
            self.update_speed()
            self.detection_range = (4 - self.level) * 40

    def update_speed(self):
        self.speed = (4 - self.level)*50