import argparse


def f() -> None:
    pass


commands = {'ini': f, 'test': f}


def main() -> None:
    args: argparse.Namespace = parse_arguments()
    print(args.command)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='basic tools for devops. Usage.')
    parser.add_argument('command', nargs='?', help='command to execute', choices=commands.keys())
    parser.add_argument('--file', nargs='?', help='file to parse')
    return parser.parse_args()


if __name__ == "__main__":
    main()
