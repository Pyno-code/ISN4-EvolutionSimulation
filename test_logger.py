import numpy as np
import h5py
import os
from logger import SimulationLogger
import json

# Création d'une simulation avec 2 frames
logger = SimulationLogger(sim_number=1)

# Frame 0
logger.add_frame(timestamp=0.0)
logger.add_food(entity_id=1, position=[1.0, 2.0, 3.0])
logger.add_entity(entity_id=100, position=[0.0, 0.0, 0.0], direction=[1.0, 0.0, 0.0])
logger.save_frame()

# Frame 1
logger.add_frame(timestamp=1/60)
logger.add_food(entity_id=2, position=[4.0, 5.0, 6.0])
logger.add_entity(entity_id=101, position=[1.0, 1.0, 1.0], direction=[0.0, 1.0, 0.0])
logger.add_entity(entity_id=102, position=[2.0, 2.0, 2.0], direction=[0.0, 0.0, 1.0])
logger.save_frame()

logger.close()


def read_simulation_as_json_like(filename):
    with h5py.File(filename, "r") as f:
        frames = []
        for frame_name in sorted(f["frames"].keys()):
            frame_grp = f[f"frames/{frame_name}"]
            timestamp = frame_grp.attrs["timestamp"]

            frame_data = {
                "frame": int(frame_name),
                "timestamp": float(timestamp),
                "entities": [],
                "foods": []
            }

            # Lecture des entités
            if "entities" in frame_grp:
                ent_grp = frame_grp["entities"]
                ids = ent_grp["ids"][:]
                positions = ent_grp["positions"][:]
                directions = ent_grp["directions"][:]
                for i in range(len(ids)):
                    frame_data["entities"].append({
                        "id": int(ids[i]),
                        "position": positions[i].tolist(),
                        "direction": directions[i].tolist()  # ou un angle si tu veux convertir
                    })

            # Lecture des nourritures
            if "food" in frame_grp:
                food_grp = frame_grp["food"]
                ids = food_grp["ids"][:]
                positions = food_grp["positions"][:]
                for i in range(len(ids)):
                    frame_data["foods"].append({
                        "id": int(ids[i]),
                        "position": positions[i].tolist()
                    })

            frames.append(frame_data)

    return frames

# Exemple d'utilisation
data = read_simulation_as_json_like("simulations/simulation_001.h5")
print(json.dumps(data, indent=2))
