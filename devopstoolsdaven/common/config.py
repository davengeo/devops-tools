import os

import yaml


def get_file_path(path: str, file_name: str) -> str:
    return os.path.join(path, file_name)


def get_yaml_file(path_file: str) -> dict:
    with open(os.path.abspath(path_file)) as yaml_file:
        return yaml.safe_load(yaml_file)
