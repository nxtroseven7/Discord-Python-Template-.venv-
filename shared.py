import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "allowed_channels": [],
    "blacklisted_channels": [],
    "blacklisted_users": [],
}

def get_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)