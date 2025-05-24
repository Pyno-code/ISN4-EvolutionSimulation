from simulation import Simulation
from app import Interface 

class Controller:
    def __init__(self):
        self.simulation = Simulation()
        self.app = Interface()
        self.running = True

    def update(self):
        self.simulation.update()
        self.app.update()

    def run(self):
        while self.running:
            self.running = self.app.running and self.simulation.running
            self.update()
            
    

if __name__ == "__main__":
    controller = Controller()
    controller.run()