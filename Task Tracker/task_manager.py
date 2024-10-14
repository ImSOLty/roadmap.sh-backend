from args_parser import parse_arguments


ARGS_CONFIG_PATH = 'args_config.json'


def main():
    parse_arguments(ARGS_CONFIG_PATH)


if __name__ == "__main__":
    main()
