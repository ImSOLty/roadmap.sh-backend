from classes import Task
import json
import typing


def read_tasks_from_file(path: str) -> dict[str: typing.Any]:
    """
    Reads the json file with tasks if exists, otherwise returns an empty dictionary
    """
    try:
        with open(path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}


def write_tasks_to_file(tasks: dict[int: Task], path: str) -> None:
    """
    Creates the json file (if there is no such file), converts each Task instance to json and rewrites the content of json file
    """
    with open(path, 'w') as file:
        file.write(json.dumps({id: task.to_json() for id, task in tasks.items()}))
