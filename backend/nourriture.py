from tkinter import Canvas
import random

class Nourriture: 
    def __init__(self, id, width, height, x=0, y=0, energy=0, pos_random=True):
        

        self.id = id

        self.type = "Nourriture"

        self.size = 1
        
        if pos_random:
            self.x = random.randint(20, width - 20)
            self.y = random.randint(20, height - 20)
            self.energy = random.randint(1, 16)
        else:
            self.energy = energy
            self.x, self.y = x, y


        self.x, self.y = x, y

        self.exist = True


    def delete(self):
        """
        Supprime l'objet en le marquant comme inexistant.

        Cette méthode vérifie si l'objet existe actuellement (self.exist est True).
        Si c'est le cas, elle définit self.exist à False pour indiquer que l'objet
        a été supprimé ou désactivé dans le contexte de la simulation.

        Returns:
            None
        """
        if self.exist:
            self.exist = False
    
    
