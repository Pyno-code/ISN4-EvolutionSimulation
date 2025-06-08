from backend.simulation import Simulation
from frontend.app import SimulationInterface 
import time

class Controller:
    def __init__(self):
        self.simulation = Simulation()
        self.app = SimulationInterface(self.simulation)
        self.running = True

    def update(self):
        """
        Met à jour l'état de l'application et de la simulation.
        Cette méthode attend que le temps défini par `time_step` se soit écoulé depuis la dernière mise à jour de la simulation.
        Ensuite, elle met à jour l'application (`self.app.update()`) puis la simulation (`self.simulation.update()`).
        """
        while self.simulation.last_update_time is not None and (time.time() - self.simulation.last_update_time) < self.simulation.time_step:
            pass
        self.app.update()
        self.simulation.update()

        pass

    def run(self):
        """
        Exécute la boucle principale du contrôleur tant que l'application est en cours d'exécution.
        Cette méthode vérifie l'état de l'application et appelle la méthode update() à chaque itération
        pour mettre à jour la simulation ou l'état du contrôleur.
        """
        while self.running:
            self.running = self.app.running
            self.update()

if __name__ == "__main__":
    controller = Controller()
    controller.run()