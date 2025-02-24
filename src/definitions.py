import os
from pathlib import Path

import yaml


def load_settings():
    with open(SETTINGS_PATH, "r") as settings_file:
        settings = yaml.load(settings_file, Loader=yaml.FullLoader)
    return settings


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = Path(ROOT_DIR)
SETTINGS_PATH = os.path.join(ROOT_DIR, '../settings.yaml')
SETTINGS = load_settings()
