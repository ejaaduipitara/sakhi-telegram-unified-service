import glob
import json
from logger import logger
from config_util import get_config_value
import os

language_dict = {}
default_lang = get_config_value('default', 'language', None)
languages_array = []

def language_init():
    """Loads language JSON files and builds the language dictionary."""

    for filename in glob.glob('./languages/*.json'):
        lang_code = filename.split('/')[-1].split('.')[0]
        with open(filename, 'r') as f:
            language_dict[lang_code] = json.load(f)

def get_message(language=default_lang, key=None, bot_id=None):
    """Retrieves a message from the language dictionary, handling fallbacks."""

    message = None
    try:
        if bot_id:
            message = language_dict[language].get(key, {}).get(bot_id)
        if not message:
            message = language_dict[language].get(key)
        if message:
            return json.loads(json.dumps(message))
    except KeyError:
        logger.warn(f"❌ Object doesn't exist for {language}.{key}")
        logger.info(f"Getting default language (en) message for key: {key}")
        if bot_id:
            message = language_dict[default_lang].get(key, {}).get(bot_id)
        if not message:
            message = language_dict[default_lang].get(key)
        if message:
            return json.loads(json.dumps(message))
    return None

def get_languages():
    """Returns the global languages array."""
    languages = os.getenv('SUPPORTED_LANGUAGES', "").split(",")
    return list(filter(lambda x: x.get("code") in languages , json.loads(get_config_value('default', 'languages', None))))