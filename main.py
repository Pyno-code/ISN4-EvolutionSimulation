import tkinter as tk
import random
import math
import threading
import time

class Entity:
    def __init__(self, canvas, x, y, speed=2, width=1280, height=720):
        self.canvas = canvas
        self.x, self.y = x, y
        self.speed = speed
        self.angle = random.uniform(0, 360)  # Direction aléatoire
        self.circle = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
        self.width = width
        self.height = height

        self.level = random.randint(1, 3)

        self.direction_line = self.canvas.create_line(x, y, x + 30 * math.cos(math.radians(self.angle)), y + 30 * math.sin(math.radians(self.angle)), fill="blue", width=2)
        self.entities = []

    def check_collision(self):
        for other in self.entities:
            if other is not self:
                distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
                if distance < 50 and other.level >= self.level:  # Rayon de détection de collision
                    self.entities.remove(self)
                    # TODO make them disapear

    def set_entities(self, entities):
        self.entities = entities

    def update_position(self):
        self.angle += random.gauss(0, 15)  # Biais vers un faible changement
        self.angle %= 360  # Garder entre 0 et 360°
        
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

class CanvaFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("Biased Random Walk")
        
        self.canvas = tk.Canvas(root, width=1280, height=720, bg="black")
        self.canvas.pack()

        self.entities = []
        self.number_entities = 20

        for i in range(self.number_entities):
            self.entities.append(Entity(self.canvas, random.randint(20, 1260), random.randint(20, 700)))
        for entity in self.entities:
            entity.set_entities(self.entities)
        
        self.running = True
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
    
    def run_loop(self):
        while self.running:
            for entity in self.entities:
                self.canvas.after(0, entity.update_position)  # Mettre à jour depuis le thread principal
            time.sleep(1/60)  # 50ms

    
    def stop(self):
        self.running = False
        self.thread.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CanvaFrame(root)
    root.mainloop()
