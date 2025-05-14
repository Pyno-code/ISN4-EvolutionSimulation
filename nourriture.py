class Nourriture: 
    def __init__(self, id, position, energie=0):
        self.position = position
        self.energie = energie % 16
        self.id = id
        self.type = "Nourriture"
        self.size = 1
        self.color = make_color()

    def make_color(self):
        return x