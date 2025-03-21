import os
import json

from config import TARGET_PATH

mode = "canton"  # 'canton' or 'gde'

if not os.path.exists(f"{TARGET_PATH}{mode}"):
    os.makedirs(f"{TARGET_PATH}{mode}")

if not os.path.exists(f"data/{mode}/current_coas.json"):
    exit(1)

with open(f"data/{mode}/current_coas.json", "r") as f:
    current_coas = json.load(f)

    for id in current_coas.keys():
        os.system(f"cp data/{mode}/png/{id}.png {TARGET_PATH}{mode}/{id}.png")
