import json

def get_settings():
    """Load Cosmos DB settings from app_settings.json."""
    with open("config/app_settings.json") as config_file:
        return json.load(config_file)