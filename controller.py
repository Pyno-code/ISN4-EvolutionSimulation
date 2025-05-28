from simulation.simulation import Simulation
from interface.app import Interface 

class Controller:
    def __init__(self):
        self.simulation = Simulation()
        self.app = Interface(self.simulation)
        self.running = True

    def update(self):
        self.simulation.update()
        self.app.update()

    def run(self):
        while self.running:
            self.update()

if __name__ == "__main__":
    controller = Controller()
    controller.run()