import random
import math
import time
import tkinter as tk

class Entity:
    
    list_color = ["red", "blue", "green"]

    def __init__(self, canvas, x, y, width=1280, height=720):
        self.level = 1

        self.canvas = canvas
        self.x, self.y = x, y
        self.speed = 4 - self.level
        self.angle = random.uniform(0, 360)  # Direction aléatoire

        self.circle = self.canvas.create_oval(x - 10*self.level, y - 10*self.level, x + 10*self.level, y + 10*self.level, fill=self.list_color[self.level-1])
        self.width = width
        self.height = height

        self.direction_line = self.canvas.create_line(x, y, x + 30 * math.cos(math.radians(self.angle)), y + 30 * math.sin(math.radians(self.angle)), fill="yellow", width=2)
        self.entities = []

        self.detection_range = (4 - self.level) * 40


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

    def set_entities(self, entities):
        self.entities = entities

    def delete(self):
        if self in self.entities:
            self.entities.remove(self)
            self.canvas.delete(self.circle)
            self.canvas.delete(self.direction_line)

    def update(self):
        entities_in_scope = self.scope_detection_entity()
        self.update_direction(entities_in_scope)
        self.update_position()

    def update_direction(self, entities_in_scope):
        if not entities_in_scope:
            self.angle += random.gauss(0, 15)  # Biais vers un faible changement
            self.angle %= 360  # Garder entre 0 et 360°
            return 

        force_x, force_y = 0, 0
        for other in entities_in_scope:
            distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
            direction = math.atan2(other.y - self.y, other.x - self.x)
            weight = (self.detection_range - distance) / self.detection_range  # Influence décroissante avec la distance
            
            if other.level < self.level:
                force_x += math.cos(direction) * weight
                force_y += math.sin(direction) * weight
            else:
                force_x -= math.cos(direction) * weight
                force_y -= math.sin(direction) * weight

        margin = 20
        repulsion_strength = 2.0
        
        if self.x < margin:
            force_x += repulsion_strength * (margin - self.x) / margin
        elif self.x > self.width - margin:
            force_x -= repulsion_strength * (self.x - (self.width - margin)) / margin
        
        if self.y < margin:
            force_y += repulsion_strength * (self.height - self.y) / margin
        elif self.y > self.height - margin:
            force_y -= repulsion_strength * (self.y - (self.height - margin)) / margin
        
        self.angle = math.degrees(math.atan2(force_y, force_x)) % 360

    def update_position(self):
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Vérification des limites
        if not (0 + 20 < new_x < self.width - 20 and 0 + 20 < new_y < self.height - 20):
            self.angle += 180  # Rebond
            self.angle %= 360
            dx = self.speed * math.cos(math.radians(self.angle))
            dy = self.speed * math.sin(math.radians(self.angle))
            new_x = self.x + dx
            new_y = self.y + dy
        
        self.check_collision()
        self.canvas.move(self.circle, dx, dy)
        self.canvas.coords(self.direction_line, new_x, new_y, new_x + 30 * math.cos(math.radians(self.angle)), new_y + 30 * math.sin(math.radians(self.angle)))
        self.x, self.y = new_x, new_y

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
            self.canvas.delete(self.circle)
            self.circle = self.canvas.create_oval(self.x - 10*self.level, self.y  - 10*self.level, self.x + 10*self.level, self.y  + 10*self.level, fill=self.list_color[self.level-1])
            self.canvas.delete(self.direction_line)
            self.direction_line = self.canvas.create_line(self.x, self.y, self.x + 30 * math.cos(math.radians(self.angle)), self.y + 30 * math.sin(math.radians(self.angle)), fill="yellow", width=2)
            self.speed = 4 - self.level
            self.detection_range = (4 - self.level) * 40


