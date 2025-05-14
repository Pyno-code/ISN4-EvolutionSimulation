class Nourriture: 
    def __init__(self, id, position, energie=0):
        self.position = position
        self.energie = energie % 16
        self.id = id
        self.type = "Nourriture"
        self.size = 1
        self.color = self.make_color()

    def make_color(self):
        return (90 + int((255-90) * (self.energie/15)**1.7), 255, 93)