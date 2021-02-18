import sys
from distutils.core import run_setup
from typing import Any, Text, Dict, Callable

ACCEPTED: Dict[Text, Callable[[Any], Any]] = {
    'name': lambda a: a.get_name(),
    'author': lambda a: a.get_author(),
    'version': lambda a: a.get_version(),
    'all': lambda a: a.__dict__
}


def main(argv: Any) -> None:
    if len(argv) < 2 or argv[1] not in ACCEPTED.keys():
        usage_exit()
    else:
        result = run_setup('./setup.py', stop_after='init')
        print(ACCEPTED[argv[1]](result))


def usage_exit() -> None:
    print('Usage: \n\tpython3 -m devops.utils.read_setup <entry = name|author>')
    print('\n\tprint the value for <entry> found in the setup.py')
    sys.exit(-1)


if __name__ == "__main__":
    main(argv=sys.argv)
