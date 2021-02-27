import configparser
import json
import os
from typing import Dict, Text, Tuple, Optional

import yaml


class Config(object):

    def __init__(self, path_file: str):
        self.path_file = path_file
        self.config = configparser.ConfigParser()
        self.config.read(path_file)

    def get_value(self, section: str, key: str, default: Optional[str] = None) -> str:
        if not self.config.has_option(section=section, option=key) and default is not None:
            return default
        return self.config[section][key]

    def get_tuple(self, section: str, key: str) -> Tuple[Text, ...]:
        raw = self.get_value(section=section, key=key).split('\n')
        return tuple(str(x).strip() for x in tuple(raw) if x)

    def get_section(self, section: str) -> Dict[Text, Text]:
        result = {}
        for key in self.config.options(section):
            result[key] = self.config.get(section, key)
        return result

    def get_path(self, key: str) -> str:
        return os.path.abspath(os.path.join(os.path.dirname(self.path_file), self.config['Paths'][key]))

    def get_file_path(self, key: str, file_name: str) -> str:
        return os.path.join(self.get_path(key=key), file_name)

    def get_json_file(self, key: str, file_name: str) -> dict:
        with open(self.get_file_path(key=key, file_name=file_name)) as json_file:
            return json.load(json_file)

    def get_yaml_file(self, key: str, file_name: str) -> dict:
        with open(self.get_file_path(key=key, file_name=file_name)) as yaml_file:
            return yaml.safe_load(yaml_file)
