import json

def get_settings():
    """Load Cosmos DB settings from app_settings.json."""
    with open("config/appsettings.json") as config_file:
        return json.load(config_file)