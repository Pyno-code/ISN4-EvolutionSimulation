from tkinter import Canvas

class Nourriture: 
    def __init__(self, canvas, x, y, id, energie=0):
        self.energie = energie % 16

        self.id = id

        self.type = "Nourriture"

        self.size = 1
        self.color = self.make_color()
        self.canvas_color = self.make_canvas_color()

        self.canvas = canvas
        self.x, self.y = x, y
        self.square = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill=self.canvas_color)

        self.exist = True

    def make_color(self):
        return (90 + int((255-90) * (self.energie/15)**1.7), 255, 93)
    
    def make_canvas_color(self):
        return "#%02x%02x%02x" % self.color
    
    def delete(self):
        if self.exist:
            self.canvas.delete(self.square)
            self.exist = False