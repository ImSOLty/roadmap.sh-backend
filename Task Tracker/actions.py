from classes import Actions, State, Task
from argparse import Namespace
import typing


def add_task(tasks: dict[int: Task], task_name):
    new_id = 1 if not tasks else (max(tasks.keys()) + 1)
    tasks[new_id] = Task(task_name)


def update_task(tasks: dict[int: Task], id: int, new_task_name):
    tasks[id].update_description(new_task_name)


def delete_task(tasks: dict[int: Task], id: int):
    tasks.pop(id)


def mark_as(tasks, id, state):
    tasks[id].update_state(state)


def list_tasks(tasks, type):
    def print_tasks(type_to_print, tasks_to_print):
        if type_to_print == State.IN_PROGRESS:
            print("In progress:")
        elif type_to_print == State.TODO:
            print("To do:")
        elif type_to_print == State.DONE:
            print("Completed:")

        for id, task in tasks_to_print.items():
            print(f'{id}. {task}')
        print()

    for t in [State.IN_PROGRESS, State.TODO, State.DONE]:
        if type == State.EMPTY or type == t:
            print_tasks(t, {key: value for key, value in tasks.items() if value.state == t})


def perform_action(tasks, arguments: Namespace):
    action = Actions(arguments.action)

    # id validation
    try:
        arguments.id = int(arguments.id)
        if arguments.id not in tasks:
            raise KeyError("There is no such identifier in the list of tasks!")
    except ValueError:
        raise ValueError("Incorrect data passed to a command: id can't be converted to integer")
    except AttributeError:
        pass

    if action == Actions.ADD:
        add_task(tasks, arguments.task_name)
    elif action == Actions.UPDATE:
        update_task(tasks, arguments.id, arguments.new_task_name)
    elif action == Actions.DELETE:
        delete_task(tasks, arguments.id)
    elif action == Actions.MARK_IN_PROGRESS:
        mark_as(tasks, arguments.id, State.IN_PROGRESS)
    elif action == Actions.MARK_DONE:
        mark_as(tasks, arguments.id, State.DONE)
    elif action == Actions.LIST:
        list_tasks(tasks, State(arguments.list_type))


def parse_tasks(tasks: dict[int: typing.Any]):
    try:
        return {int(id): Task.from_dict(value) for id, value in tasks.items()}
    except ValueError:
        raise ValueError("Tasks file was corrupted. Objects' keys should be convertable to integer")
