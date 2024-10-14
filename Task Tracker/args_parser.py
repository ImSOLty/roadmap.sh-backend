from argparse import ArgumentParser, Namespace
import typing
import json


class Argument:
    """
    "Argument" class represents argument passed to the parser/subparser
    """
    sub_parsers: list["Parser"]
    options: dict[str, typing.Any]

    def __init__(self, options) -> "Argument":
        self.sub_parsers = {}
        if 'subs' in options:
            self.sub_parsers = [
                Parser.parse_config(parser) for parser in options['subs']
            ]
            self.options = {k: v for k, v in options.items() if k != 'subs'}
        else:
            self.options = options

    def construct_argument(self, parser: ArgumentParser) -> None:
        """
        Add an argument to passed parser if there is no subparsers,
        depending on this argument.
        Otherwise, constructs all related subparsers
        """
        if self.sub_parsers:
            subparsers = parser.add_subparsers(**self.options)
            for sub_parser in self.sub_parsers:
                sub_parser.construct_parser(subparsers)
        else:
            parser.add_argument(**self.options)


class Parser:
    """
    "Parser" class represents parser/subparser used to validate passed data
    """
    options: dict[str, typing.Any]
    args: list[Argument]

    def __init__(self, options: dict[str, typing.Any]) -> "Parser":
        self.options = options
        self.args = []

    @classmethod
    def parse_config(cls, config: dict[str, typing.Any]) -> "Parser":
        """
        Class method used to create the instance of "Parser"
        class from the config passed through arguments
        """
        res = cls({k: v for k, v in config.items() if k != 'args'})
        for options in config['args']:
            res.args.append(Argument(options))
        return res

    def construct_parser(
            self, prev_parser: typing.Optional["Parser"] = None
    ) -> ArgumentParser:
        """
        Method, used to construct the result ArgumentParser
        """
        if prev_parser is None:
            parser = ArgumentParser(**self.options)
            for arg in self.args:
                arg.construct_argument(parser)
            return parser
        else:
            subparser = prev_parser.add_parser(
                name=self.options['prog'], **self.options
            )
            for arg in self.args:
                arg.construct_argument(subparser)


def parse_arguments(config_path: str) -> Namespace:
    """
    Constructs an ArgumentParser based on the provided config file (path)
    and returns all the parsed_args via argparse's Namespace object
    """

    with open(config_path, 'r') as config_file:
        config = json.loads(config_file.read())

    parser = Parser.parse_config(config).construct_parser()
    return parser.parse_args()
