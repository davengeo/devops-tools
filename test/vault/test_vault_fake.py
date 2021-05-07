import os
import sys

from assertpy import assert_that

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from devopstoolsdaven.vault.vault_fake import VaultFake
from devopstoolsdaven.vault.vault import Vault

from devopstoolsdaven.common.config import Config

config = Config(os.path.join(os.path.dirname(__file__), '../../app.ini'))


def test_vault_fake_read_from_json() -> None:
    path: str = config.get_file_path(key='fakes', file_name='vault.json')
    vault: Vault = VaultFake(path_fake=path)
    result: dict = {}
    if vault.is_authenticated(0):
        result = vault.read_secret('test')
    assert_that(result).is_equal_to({'test': 'OK'})
