from argparse import ArgumentParser
import typing
import json


class Argument:
    sub_parsers: list["Parser"]
    options: dict[str, typing.Any]

    def __init__(self, options):
        self.sub_parsers = {}
        if 'subs' in options:
            self.sub_parsers = [Parser.parse_config(parser) for parser in options['subs']]
            self.options = {option: value for option, value in options.items() if option != 'subs'}
        else:
            self.options = options

    def construct_argument(self, parser: ArgumentParser):
        if self.sub_parsers:
            subparsers = parser.add_subparsers(**self.options)
            for sub_parser in self.sub_parsers:
                sub_parser.construct_parser(subparsers)
        else:
            parser.add_argument(**self.options)


class Parser:
    options: dict[str, typing.Any]
    args: list[Argument]

    def __init__(self, options):
        self.options = options
        self.args = []

    @classmethod
    def parse_config(cls, config):
        res = cls({option: value for option, value in config.items() if option != 'args'})
        for options in config['args']:
            res.args.append(Argument(options))
        return res

    def construct_parser(self, prev_parser=None):
        if prev_parser is None:
            parser = ArgumentParser(**self.options)
            for arg in self.args:
                arg.construct_argument(parser)
            return parser
        else:
            subparser = prev_parser.add_parser(name=self.options['prog'], **self.options)
            for arg in self.args:
                arg.construct_argument(subparser)


def parse_arguments(config_path):
    with open(config_path, 'r') as config_file:
        config = json.loads(config_file.read())
        parser = Parser.parse_config(config).construct_parser()
    print(parser.parse_args())
