import h5py
import numpy as np
import os

class SimulationLogger:
    def __init__(self, sim_number: int, timestep: float = 1/60):
        filename = f"/files/simulations/simulation_{sim_number:03d}.h5"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.file = h5py.File(filename, "w", libver='latest')
        self.file.swmr_mode = True
        self.file.attrs["timestep"] = timestep
        self.frame_count = 0

    def add_frame(self, timestamp: float):
        """Crée une nouvelle frame dans le fichier."""
        frame_grp = self.file.create_group(f"frames/{self.frame_count:06d}")
        frame_grp.attrs["timestamp"] = timestamp
        self._current_frame = frame_grp
        self._foods = []
        self._entities = []
        self.frame_count += 1

    def add_food(self, entity_id: int, position):
        self._foods.append({
            "id": entity_id,
            "position": position
        })

    def add_entity(self, entity_id: int, position, direction):
        self._entities.append({
            "id": entity_id,
            "position": position,
            "direction": direction
        })

    def save_frame(self):
        """Sauvegarde les nourritures et entités ajoutées à la frame."""
        if self._foods:
            food_ids = np.array([f["id"] for f in self._foods], dtype=np.int32)
            food_positions = np.array([f["position"] for f in self._foods], dtype=np.float32)
            food_grp = self._current_frame.create_group("food")
            food_grp.create_dataset("ids", data=food_ids, chunks=True)
            food_grp.create_dataset("positions", data=food_positions, chunks=True)

        if self._entities:
            entity_ids = np.array([e["id"] for e in self._entities], dtype=np.int32)
            entity_positions = np.array([e["position"] for e in self._entities], dtype=np.float32)
            entity_directions = np.array([e["direction"] for e in self._entities], dtype=np.float32)
            ent_grp = self._current_frame.create_group("entities")
            ent_grp.create_dataset("ids", data=entity_ids, chunks=True)
            ent_grp.create_dataset("positions", data=entity_positions, chunks=True)
            ent_grp.create_dataset("directions", data=entity_directions, chunks=True)

        self.file.flush()

    def close(self):
        self.file.close()
