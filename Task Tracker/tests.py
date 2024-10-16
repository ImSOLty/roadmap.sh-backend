import enum
import subprocess
import os
from datetime import datetime

import pytest


class Actions(enum.Enum):
    UNEXISTING = 'whatever'
    ADD = 'add'
    UPDATE = 'update'
    DELETE = 'delete'
    MARK_IN_PROGRESS = 'mark-in-progress'
    MARK_DONE = 'mark-done'
    LIST = 'list'


class TaskStatus(enum.Enum):
    EMPTY = ''
    UNEXISTING = 'whatever'
    TODO = 'todo'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'


# Todo: remove (will be passed through workflows)
if os.getenv('PATH_TO_SCRIPT') is None:
    os.environ = {
        'INTERPRETER': 'python',
        'PATH_TO_SCRIPT': 'task_manager.py',
        'TASKS_FILE_NAME': 'tasks.json',
    }

COMMAND = f'{os.getenv("INTERPRETER")} {os.getenv("PATH_TO_SCRIPT")}'
TASKS_FILE_NAME = os.getenv('TASKS_FILE_NAME')
PATH_TO_TASKS_FILE = os.path.join(os.path.dirname(__name__), TASKS_FILE_NAME)


class Mocker:
    execution_command: str
    process: subprocess.CompletedProcess[bytes]
    executed: bool

    def __init__(self, args):
        self.executed = False
        arguments_as_string = [
            # convert to str if enum
            ar.value if isinstance(ar, enum.Enum) else str(ar) for ar in args
        ]
        self.execution_command = COMMAND + ' ' + ' '.join(arguments_as_string)

    def run(self):
        self.process = subprocess.run(self.execution_command,
                                      capture_output=True)
        self.executed = True

    @property
    def stdout(self):
        if not self.executed:
            return None
        return self.process.stdout.strip().decode("utf-8")

    @property
    def stderr(self):
        if not self.executed:
            return None
        return self.process.stderr.strip().decode("utf-8")


def clear_tasks_file():
    if os.path.exists(PATH_TO_TASKS_FILE):
        os.remove(PATH_TO_TASKS_FILE)


def get_tasks_file_content():
    if os.path.exists(PATH_TO_TASKS_FILE):
        with open(PATH_TO_TASKS_FILE, 'r') as file:
            return file.read()
    else:
        raise FileNotFoundError


@pytest.fixture(autouse=True)
def clear_file_on_test_start():
    yield
    clear_tasks_file()


@pytest.mark.parametrize('arguments', [
    [],
    [Actions.ADD],
    [Actions.DELETE],
    [Actions.UPDATE],
    [Actions.UPDATE, 0],
    [Actions.UPDATE, 'test_task'],
    [Actions.MARK_IN_PROGRESS],
    [Actions.MARK_DONE],
])
def test_missing_required_arguments(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token.lower() in mocker.stderr.lower() for token in [
        'usage', 'error', 'arguments are required'
    ])


@pytest.mark.parametrize('arguments', [
    [Actions.ADD, 'test_task', 'inc_argument'],
    [Actions.DELETE, 1, 'inc_argument'],
    [Actions.UPDATE, 1, 'test_task2', 'inc_argument'],
    [Actions.MARK_IN_PROGRESS, 1, 'inc_argument'],
    [Actions.MARK_DONE, 1, 'inc_argument'],
    [Actions.LIST, TaskStatus.DONE, 'inc_argument'],
])
def test_incorrect_command_length(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token.lower() in mocker.stderr.lower() for token in [
        'usage', 'error', 'unrecognized arguments', arguments[-1]
    ])


@pytest.mark.parametrize('arguments', [
    [Actions.UNEXISTING],
    [Actions.UNEXISTING, 'random_argument'],
    [Actions.LIST, TaskStatus.UNEXISTING],
])
def test_incorrect_command(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token.lower() in mocker.stderr.lower() for token in [
        'usage', 'error', 'invalid choice'
    ])


@pytest.mark.parametrize('id', [-1, 'string', 2])
@pytest.mark.parametrize('arguments', [
    [Actions.DELETE],
    [Actions.UPDATE, 'test_task2'],
    [Actions.MARK_IN_PROGRESS],
    [Actions.MARK_DONE],
])
def test_incorrect_id_in_command(arguments, id):
    Mocker([Actions.ADD, 'test_task']).run()  # add task to test identifiers
    mocker = Mocker([arguments[0]] + [id] + arguments[1:])
    mocker.run()
    assert all(token.lower() in mocker.stderr.lower() for token in [
        'error', 'id'
    ])


# used for test_action_feedback test
TEST_ACTION_FEEDBACK_TASK_NAME = "test_action_feedback"


@pytest.mark.parametrize('arguments,expected_tokens', [
    ([Actions.ADD, "test_task"], ["test_task", "add"]),
    ([Actions.DELETE, 1], [TEST_ACTION_FEEDBACK_TASK_NAME, "delete"]),
    ([Actions.UPDATE, 1, "new_task_name"], [TEST_ACTION_FEEDBACK_TASK_NAME, "update", "new_task_name"]),
    ([Actions.MARK_DONE, 1], [TEST_ACTION_FEEDBACK_TASK_NAME, TaskStatus.DONE.value]),
    ([Actions.MARK_IN_PROGRESS, 1], [TEST_ACTION_FEEDBACK_TASK_NAME, TaskStatus.IN_PROGRESS.value]),
])
def test_action_feedback(arguments, expected_tokens):
    Mocker([Actions.ADD, TEST_ACTION_FEEDBACK_TASK_NAME]).run()  # add task to test feedback
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token.lower() in mocker.stdout.lower() for token in expected_tokens)
    assert not mocker.stderr.strip()


fake_tasks = [
    '"Do my laundry"',
    '"Cancel milk delivery"',
    '"Clean fridge"',
    '"Check passport"',
    '"Do web check-in"',
    '"Download a movie for the flight"',
    '"Recharge mobile"',
    '"Pack swimsuit"',
]


def clear_string(s):
    return ''.join(e for e in s if e.isalnum()).lower()


def validate_list_output(output, included_tasks, excluded_tasks):
    output = clear_string(output)

    for task in included_tasks:
        description, created_ts, updated_ts =\
              task['description'], int(task['created']), int(task['updated'])
        assert clear_string(description) in output
        assert clear_string(str(datetime.fromtimestamp(created_ts))) in output
        assert clear_string(str(datetime.fromtimestamp(updated_ts))) in output
    for task in excluded_tasks:
        assert not (clear_string(task['description']).lower() in output)


@pytest.mark.parametrize('output_list', [TaskStatus.EMPTY, TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.DONE])
@pytest.mark.parametrize('arguments_sequence', [
    [
        [Actions.ADD, fake_tasks[0]],
        [Actions.ADD, fake_tasks[1]],
        [Actions.UPDATE, 2, fake_tasks[2]],
        [Actions.ADD, fake_tasks[3]],
        [Actions.UPDATE, 3, fake_tasks[4]],
        [Actions.UPDATE, 1, fake_tasks[5]],
        [Actions.MARK_IN_PROGRESS, 2],
        [Actions.MARK_DONE, 3],
        [Actions.DELETE, 1],
        [Actions.DELETE, 2],
        [Actions.DELETE, 3],
    ]
])
def test_end_to_end(arguments_sequence, output_list: TaskStatus):
    tasks = {}

    for arguments in arguments_sequence:
        mocker = Mocker(arguments)
        mocker.run()
        assert not mocker.stderr.strip()

        # parse command and action
        action = arguments[0]
        id = arguments[1]
        if action == Actions.ADD:
            tasks[1 if not tasks else max(tasks.keys()) + 1] = {
                "description": arguments[1],
                "created": datetime.now().timestamp(),
                "updated": datetime.now().timestamp(),
                "status": TaskStatus.TODO,
            }
        elif action == Actions.UPDATE:
            tasks[id]["description"] = arguments[2]
            tasks[id]["updated"] = datetime.now().timestamp()
        elif action == Actions.DELETE:
            tasks.pop(id)
        elif action == Actions.MARK_DONE:
            tasks[id]["status"] = TaskStatus.DONE
            tasks[id]["updated"] = datetime.now().timestamp()
        elif action == Actions.MARK_IN_PROGRESS:
            tasks[id]["status"] = TaskStatus.IN_PROGRESS
            tasks[id]["updated"] = datetime.now().timestamp()

        # run command
        mocker = Mocker([Actions.LIST, output_list])
        # validate "list" output
        included, excluded = [], []
        for task in tasks.values():
            if output_list in [task['status'], TaskStatus.EMPTY]:
                included.append(task)
            else:
                excluded.append(task)

        mocker.run()

        validate_list_output(mocker.stdout, included_tasks=included, excluded_tasks=excluded)
        assert not mocker.stderr.strip()
