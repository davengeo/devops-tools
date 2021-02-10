import sys
from distutils.core import run_setup
from typing import Any


def main(argv: Any) -> None:
    if len(argv) < 2 or argv[1] not in ['name', 'author', 'version', 'all']:
        usage_exit()
    else:
        result = run_setup('./setup.py', stop_after='init')
        if argv[1] == 'name':
            print(result.get_name())  # type: ignore[attr-defined]
        if argv[1] == 'author':
            print(result.get_author())  # type: ignore[attr-defined]
        if argv[1] == 'version':
            print(result.get_version())  # type: ignore[attr-defined]
        if argv[1] == 'all':
            print(result.__dict__)


def usage_exit() -> None:
    print('Usage: \n\tpython3 -m devops.utils.read_setup <entry = name|author>')
    print('\n\tprint the value for <entry> found in the setup.py')
    sys.exit(-1)


if __name__ == "__main__":
    main(argv=sys.argv)
