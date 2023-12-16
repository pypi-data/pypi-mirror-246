# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/TelegramExtended > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/TelegramExtended/blob/main/LICENSE >
#
# All rights reserved.

from json import load as js_load
from os import listdir
from os.path import isfile, join
import yaml
from VaniLite.errors import *

def get_all_files_in_dir(directory: str) -> list:
    """Get all files in the given directory."""
    return [f for f in listdir(directory) if isfile(join(directory, f))]


def load_json_file(path_to_file: str) -> dict:
    """Load the JSON file for the given language code."""
    json_file_path = path_to_file + ".json"
    with open(json_file_path, 'r', encoding="utf-8") as json_file:
        return js_load(json_file)

def load_yaml_file(path_to_file: str) -> dict:
    """Load the YAML file for the given language code."""
    yaml_file_path = path_to_file + ".yaml"
    with open(yaml_file_path, 'r', encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)

def load_file(language_code, language_dir="/strings/"):
    """Load the file for the given language code."""
    path_to_file = join(language_dir, language_code.upper())
    if isfile(path_to_file + ".json"):
        return load_json_file(path_to_file)
    elif isfile(path_to_file + ".yaml"):
        return load_yaml_file(path_to_file)
    else:
        raise FileNotFoundError(f"Translation file for language code {language_code} not found in directory {language_dir}.")