import os
import json

def get_config() -> dict:
    path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(path, "../config/config.json")

    if not os.path.isfile(config_path):
        raise FileNotFoundError("The file config.json could not be found inside the config folder. Have you set up the config already?")
    with open(config_path) as f:
        data = json.loads(f.read())
    return data