import os
import json

def get_config() -> dict:
    if not os.path.isfile("config/config.json"):
        raise FileNotFoundError("The file config.json could not be found inside the config folder. Have you set up the config already?")
    with open("config/config.json") as f:
        data = json.loads(f.read())
    return data