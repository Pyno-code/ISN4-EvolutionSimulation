from backend.simulation import Simulation
from frontend.app import SimulationInterface 

class Controller:
    def __init__(self):
        self.simulation = Simulation()
        self.app = SimulationInterface(self.simulation)
        self.running = True

    def update(self):
        self.simulation.update()
        self.app.update()

        pass
    def run(self):
        while self.running:
            self.running = self.app.running
            self.update()

if __name__ == "__main__":
    controller = Controller()
    controller.run()