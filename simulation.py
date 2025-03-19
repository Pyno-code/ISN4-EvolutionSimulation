from entity import Entity
import tkinter as tk
import random
import threading
import time


class CanvaFrame:
    def __init__(self, root):

        self.number_entities = 30

        self.root = root
        self.root.title("Biased Random Walk")
        self.window_width = 1280
        self.window_height = 960
        self.canvas = tk.Canvas(root, width=self.window_width, height=self.window_height, bg="black")
        self.canvas.pack()
        
        self.entities = []

        margin = 40
        for i in range(self.number_entities):
            self.entities.append(Entity(self.canvas, random.randint(margin, self.window_width-margin), random.randint(margin, self.window_height-margin), self.window_width, self.window_height))
        for entity in self.entities:
            entity.set_entities(self.entities)
        
        self.running = True
        self.thread = threading.Thread(target=self.run_loop)
        self.thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.fps = 0
        self.fps_fixed = 90
    
    def run_loop(self):
        while self.running:
            print("-------------------------------------")
            start = time.time()
            for entity in self.entities:
                self.canvas.after(0, entity.update)  # Mettre à jour depuis le thread principal
            time.sleep(1/self.fps_fixed)
            if time.time() - start != 0:
                self.fps = 1/(time.time() - start)
            else:
                self.fps = 0
            print("-------------------------------------")



    def get_number_entity(self):
        return len(self.entities)
    
    def get_fps(self):
        return self.fps

    def stop(self):
        self.running = False
        self.thread.join()
        self.root.destroy()