from abc import ABC, abstractmethod
from typing import Union, Text


class Vault(ABC):
    __token: Union[Text, None] = None

    @abstractmethod
    def is_authenticated(self, count: int) -> bool:
        pass

    @abstractmethod
    def write_secret(self, name: str, secret: dict) -> None:
        pass

    @abstractmethod
    def read_secret(self, name: str) -> dict:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class VaultException(BaseException):
    def __init__(self, message: str, url: str):
        self.message = message
        self.url = url


class VaultAuthenticationException(BaseException):
    def __init__(self, message: str):
        self.message = message
