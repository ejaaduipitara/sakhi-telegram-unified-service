import os
from configparser import ConfigParser
from logger import logger

config_file_path = 'config.ini'  # Update with your config file path
config = ConfigParser()
config.read(config_file_path)


def get_config_value(section, key, default=None):
    # Check if the key exists in the environment variables
    value = os.getenv(key, default)

    # If the key is not in the environment variables, try reading from a config file
    if value is None or value == "":
        # Attempt to read the config file
        try:
            value = config.get(section, key, fallback=default)
        except Exception as e:
            logger.error(
                {"Exception": f"Error reading config file: {e}"})
            raise ValueError(f"Missing configuration variable '{key}' in section '{section}'")

    return value
