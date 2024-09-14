import logging
import os
from datetime import datetime

import pyperclip
import toml
from os.path import expanduser

# Define the path to your config.toml file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.toml')

# Setup Logs
logger = logging.getLogger("TrimAudio")
logging_format = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler("anki_script.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging_format)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # You can set the desired log level for console output
console_handler.setFormatter(logging_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

temp_directory = ''


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            config_file = toml.load(file)

            # Expanding user home paths in case "~" is used
            config_file['paths']['folder_to_watch'] = expanduser(config_file['paths']['folder_to_watch'])
            config_file['paths']['audio_destination'] = expanduser(config_file['paths']['audio_destination'])
            config_file['paths']['screenshot_destination'] = expanduser(config_file['paths']['screenshot_destination'])

            return config_file
    except FileNotFoundError:
        logger.error(f"Configuration file {CONFIG_FILE} not found!")
        return None
    except toml.TomlDecodeError as e:
        logger.error(f"Error parsing {CONFIG_FILE}: {e}")
        return None


config = load_config()

if config:
    path_config = config.get('paths', {})
    folder_to_watch = path_config.get('folder_to_watch', expanduser("~/Videos/OBS"))
    audio_destination = path_config.get('audio_destination', expanduser("~/Videos/OBS/Audio/"))
    screenshot_destination = path_config.get('screenshot_destination', expanduser("~/Videos/OBS/SS/"))

    # Anki fields
    anki_config = config.get('anki', {})
    anki_url = config.get('url', 'http://127.0.0.1:8765')
    sentence_audio_field = anki_config.get('sentence_audio_field', "Sentence Audio")
    picture_field = anki_config.get('picture_field', "Picture")
    current_game = anki_config.get('current_game', "GameSentenceMiner")
    custom_tags = anki_config.get("custom_tags", [])
    add_game_tag = anki_config.get("add_game_tag", True)

    # Feature flags
    feature_config = config.get('features', {})
    do_vosk_postprocessing = feature_config.get('do_vosk_postprocessing', True)
    remove_video = feature_config.get('remove_video', True)
    update_anki = feature_config.get('update_anki', True)
    act_on_new_card_in_anki = feature_config.get('full_auto_mode', False)

    # Vosk config
    vosk_config = config.get('vosk', {})
    vosk_model_url = vosk_config.get('url', "https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip")
    vosk_log_level = vosk_config.get('log-level', -1)

    # screenshot config
    screenshot_config = config.get('screenshot', {})
    screenshot_width = screenshot_config.get('width', 0)
    screenshot_quality = str(screenshot_config.get('quality', 85))
    screenshot_extension = screenshot_config.get('extension', "webp")

    # audio config
    audio_config = config.get('audio', {})
    audio_extension = audio_config.get('extension', 'opus')
    audio_beginning_offset = audio_config.get('beginning_offset', 0.0)
    audio_end_offset = audio_config.get('end_offset', 0.5)

    # Parse OBS settings from the config
    obs_config = config.get('obs', {})
    obs_enabled = obs_config.get('enabled', True)
    obs_start_buffer = obs_config.get('start_buffer', True)
    obs_full_auto_mode = obs_config.get('full_auto_mode', False)
    OBS_HOST = obs_config.get('host', "localhost")
    OBS_PORT = obs_config.get('port', 4455)
    OBS_PASSWORD = obs_config.get('password', "your_password")

    #secret config DO NOT PUT THESE IN THE EXAMPLE
    override_audio = anki_config.get("override_audio", False)

else:
    raise Exception("No config found")
