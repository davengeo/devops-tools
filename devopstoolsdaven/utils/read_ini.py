import configparser
import sys
from typing import Any

config = configparser.ConfigParser()


def main(argv: Any) -> None:
    if len(argv) < 4:
        usage_exit()
    try:
        config.read_file(open(argv[1]))
        print(config.get(section=argv[2], option=argv[3]))
    except Exception as e:
        print_exception(e)
        usage_exit()


def print_exception(e: Exception) -> None:
    print(e)


def usage_exit() -> None:
    print('Usage: \n\tpython3 -m devops.utils.read_ini <ini-file> <section> <entry>')
    print('\n\tjust print the value for <entry> found in the indicated <section> of the <ini-file>')
    sys.exit(-1)


if __name__ == "__main__":
    main(argv=sys.argv)
