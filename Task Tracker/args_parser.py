from argparse import ArgumentParser
import typing

ARGS_CONFIG = {
    'name': 'Task Management Tool',
    'description': 'This program allows manipulation of tasks to track progress.',
    'args': [{
            'dest': 'action',
            'help': 'The action to perform on the list of tasks.',
            'subs': {
                'add': [
                    {'dest': 'task_name', 'help': 'The name of the new task.'}
                ],
                'update': [
                    {'dest': 'id', 'help': 'The identifier of the task to update.'},
                    {'dest': 'new_task_name', 'help': 'The new name for the existing task.'}
                ],
                'delete': [
                    {'dest': 'id', 'help': 'The identifier of the task to delete.'}
                ],
                'mark-in-progress': [
                    {'dest': 'id', 'help': 'The identifier of the task to mark as "in progress".'}
                ],
                'mark-done': [
                    {'dest': 'id', 'help': 'The identifier of the task to mark as "done".'}
                ],
                'list': [
                    {'dest': 'list_type', 'nargs': '?',
                        'help': 'The filter type for listing tasks (leave blank to list all tasks).',
                        'choices': ['done', 'todo', 'in-progress']}
                ]
            }
    }]
}


class Argument:
    sub_parsers: dict[str, list["Argument"]]
    options: dict[str, typing.Any]

    def __init__(self, options):
        self.sub_parsers = {}
        if 'subs' in options:
            for parser_name, arguments in options['subs'].items():
                self.sub_parsers[parser_name] = [Argument(arg_opt) for arg_opt in arguments]
            self.options = {option: value for option, value in options.items() if option != 'subs'}
        else:
            self.options = options

    def construct_argument(self, parser: ArgumentParser):
        if self.sub_parsers:
            subparsers = parser.add_subparsers(**self.options)
            for sub_parser_name, arguments in self.sub_parsers.items():
                subparser = subparsers.add_parser(sub_parser_name)
                for arg in arguments:
                    arg.construct_argument(subparser)
        else:
            parser.add_argument(**self.options)


class Parser:
    prog_name: str
    description: str
    args: list[Argument]

    def __init__(self, name, description):
        self.prog_name = name
        self.description = description
        self.args = []

    @classmethod
    def parse_config(cls, config):
        res = cls(config["name"], config["description"])
        for options in config["args"]:
            res.args.append(Argument(options))
        return res

    def construct_parser(self):
        parser = ArgumentParser(prog=self.prog_name, description=self.description)
        for arg in self.args:
            arg.construct_argument(parser)
        return parser


def parse_arguments():
    parser = Parser.parse_config(ARGS_CONFIG).construct_parser()
    print(parser.parse_args())
