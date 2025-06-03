from tkinter import Canvas
import random

class Nourriture: 
    def __init__(self, id, width, height, x=0, y=0, energy=0, random = True):
        

        self.id = id

        self.type = "Nourriture"

        self.size = 1
        self.color = self.make_color()
        self.canvas_color = self.make_canvas_color()
        
        if random:
            self.x = random.randint(20, width - 20)
            self.y = random.randint(20, height - 20)
            self.energy = random.randint(1, 16)
        else:
            self.energy = energy
            self.x, self.y = x, y


        self.x, self.y = x, y

        self.exist = True


    def delete(self):
        if self.exist:
            self.exist = False

    # def make_color(self):
    #     return (90 + int((255-90) * (self.energy/15)**1.7), 255, 93)
    
    # def make_canvas_color(self):
    #     return "#%02x%02x%02x" % self.color
    # import this in canva frame