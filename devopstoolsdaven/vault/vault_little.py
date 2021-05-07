import getpass
import logging
import os
from typing import Tuple, Text, Union, Any, cast

import requests

from .vault import VaultException, Vault, VaultAuthenticationException

VAULT = 'Vault'
ENV_VAR = 'VAULT_TOKEN'
LIMIT = 3


class VaultLittle(Vault):
    __token: Union[Text, None] = None

    def __init__(self, url: str, env: str) -> None:
        self.__url = url
        self.__env = env

    def is_authenticated(self, count: int) -> bool:
        if self.__token is not None:
            return True
        if count > LIMIT:
            logging.error('\r\tVault authentication error: {} retries exceeded.'.format(count))
            raise VaultAuthenticationException(message='unable to authenticate after {} retries'.format(count))
        self.__authenticate()
        return self.is_authenticated(++count)

    def __authenticate(self) -> None:
        if not os.getenv('VAULT_TOKEN'):
            self.__token = self.__get_token(creds=self.get_password_from_input())
        else:
            self.__token = os.getenv('VAULT_TOKEN')
        logging.debug('\n\tToken:\t{}'.format(self.__token))

    def __get_token(self, creds: Tuple[Text, Text]) -> Text:
        url = '{}/v1/auth/common/login/{}'.format(self.__url, creds[0])
        response = requests.post(url=url, data={'password': creds[1]})
        if not response.ok:
            raise VaultException(message='{}:{}'.format(response.status_code, response.reason), url=url)
        obj: Any = response.json()
        logging.info(
            '\n\tAUTHENTICATED! Token received, lease time {} seconds.'.format(obj.get('auth').get('lease_duration'))
        )
        return cast(Text, obj.get('auth').get('client_token'))

    def write_secret(self, name: str, secret: dict) -> None:
        url = '{}/v1/secret/data/{}/{}/config/cloudamqp'.format(self.__url, name, self.__env)
        response = requests.post(url=url,
                                 json={
                                     'data': secret},
                                 headers={
                                     'X-Vault-Namespace': 'test',
                                     'X-Vault-Token': self.__token,
                                     'Content-type': 'application/json'
                                 })
        if not response.ok:
            raise VaultException(message='{}:{}'.format(response.status_code, response.reason), url=url)
        obj: dict = response.json()
        logging.debug('response: {}'.format(obj))
        logging.info('\n\tThe secret with key {} has been stored in vault.'.format(name))
        logging.info('\n\tVault Store path:\t{}'.format(url))

    def read_secret(self, name: str) -> dict:
        raise VaultException(message='Not implemented yet', url='')

    def close(self) -> None:
        pass

    @staticmethod
    def get_password_from_input() -> Tuple[Text, Text]:
        logging.info('Your AD credentials are required in order to interact with Harshicorp Vault.\n')
        user: str = input("\n\tType your AD credentials:\t")
        passwd: str = getpass.getpass("\n\tInput your password:\t\t")
        return user.upper(), passwd
