from classes import Actions, State, Task
from argparse import Namespace
import typing


def add_task(tasks: dict[int: Task], task_name: str) -> None:
    """
    'Add task' action function
    """
    new_id = 1 if not tasks else (max(tasks.keys()) + 1)
    tasks[new_id] = Task(task_name)
    print(f'Task "{task_name}" successfully added!')


def update_task(tasks: dict[int: Task], id: int, new_task_name: str) -> None:
    """
    'Update task' action function
    """
    task_description = tasks[id].description
    tasks[id].update_description(new_task_name)
    print(f'Successfully updated "{task_description}"' +
          ' task with the new description: "{new_task_name}"!')


def delete_task(tasks: dict[int: Task], id: int) -> None:
    """
    'Delete task' action function
    """
    task_description = tasks[id].description
    tasks.pop(id)
    print(f'Task "{task_description}" successfully deleted!')


def mark_as(tasks: dict[int: Task], id: int, state: State) -> None:
    """
    'Mark as "done/in progress"' action function
    """
    tasks[id].update_state(state)
    print(f'Task "{tasks[id].description}" marked as "{state.value}"!')


def list_tasks(tasks: dict[int: Task], type: State) -> None:
    """
    Prints tasks according to their state
    """
    def print_tasks(type_to_print: State, tasks_to_print: dict[int: Task]):
        if type_to_print == State.IN_PROGRESS:
            print("[In progress]:")
        elif type_to_print == State.TODO:
            print("[To do]:")
        elif type_to_print == State.DONE:
            print("[Completed]:")

        for id, task in tasks_to_print.items():
            print(f'{id}. {task}')
        print()

    for t in [State.IN_PROGRESS, State.TODO, State.DONE]:
        if type == State.EMPTY or type == t:
            print_tasks(t, {
                key: value for key, value in tasks.items() if value.state == t
            })


def perform_action(tasks: dict[int: Task], arguments: Namespace) -> None:
    """
    Performs any action provided from user:
    - Add
    - Update
    - Delete
    - Mark as "in progress"
    - Mark as "done"
    - List
    Validates id argument as well
    """
    action = Actions(arguments.action)

    # id validation
    try:
        arguments.id = int(arguments.id)
        if arguments.id not in tasks:
            raise KeyError("There is no such identifier in the list of tasks!")
    except ValueError:
        raise ValueError(
            "Inappropriate argument value: id can't be converted to integer"
        )
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


def parse_tasks(tasks: dict[int: typing.Any]) -> None:
    """
    Parses tasks from json representation to dict[int: Task]
    """
    try:
        return {int(id): Task.from_dict(value) for id, value in tasks.items()}
    except ValueError:
        raise ValueError(
            "Tasks file may be corrupted. IDs should be convertable to int"
        )
