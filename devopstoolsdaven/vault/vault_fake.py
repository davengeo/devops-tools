import json

from .vault import Vault


class VaultFake(Vault):

    def __init__(self, path_json: str) -> None:
        with open(path_json) as json_file:
            self.__data = json.load(json_file)

    def is_authenticated(self, count: int = 0) -> bool:
        return True

    def write_secret(self, name: str, secret: dict) -> None:
        pass

    def read_secret(self, name: str) -> dict:
        return self.__data[name]

    def close(self) -> None:
        pass
