import json


def read_tasks_from_file(path):
    try:
        with open(path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}


def write_tasks_to_file(tasks, path):
    with open(path, 'w') as file:
        file.write(json.dumps({id: task.to_json() for id, task in tasks.items()}))
