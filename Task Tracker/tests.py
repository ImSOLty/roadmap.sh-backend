import enum
import subprocess
import os
import pytest


class Actions(enum.Enum):
    UNEXISTING = 'whatever'
    ADD = 'add'
    UPDATE = 'update'
    DELETE = 'delete'
    MARK_IN_PROGRESS = 'mark-in-progress'
    MARK_DONE = 'mark-done'
    LIST = 'list'


class TaskType(enum.Enum):
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
            arg.value if isinstance(arg, enum.Enum) else str(arg) for arg in args
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
        return str(self.process.stdout.strip())

    @property
    def stderr(self):
        if not self.executed:
            return None
        return str(self.process.stderr.strip())


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
    assert all(token in mocker.stderr.lower() for token in ['usage', 'error', 'arguments are required'])


@pytest.mark.parametrize('arguments', [
    [Actions.ADD, 'test_task', 'inc_argument'],
    [Actions.DELETE, 0, 'inc_argument'],
    [Actions.UPDATE, 0, 'test_task2', 'inc_argument'],
    [Actions.MARK_IN_PROGRESS, 0, 'inc_argument'],
    [Actions.MARK_DONE, 0, 'inc_argument'],
    [Actions.LIST, TaskType.DONE, 'inc_argument'],
])
def test_incorrect_command_length(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token in mocker.stderr.lower() for token in ['usage', 'error', 'unrecognized arguments', arguments[-1]])


@pytest.mark.parametrize('arguments', [
    [Actions.UNEXISTING],
    [Actions.UNEXISTING, 'random_argument'],
    [Actions.LIST, TaskType.UNEXISTING],
])
def test_incorrect_command(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token in mocker.stderr.lower() for token in ['usage', 'error', 'invalid choice'])


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
    assert all(token in mocker.stderr.lower() for token in ['error', 'id'])


@pytest.mark.parametrize('arguments_sequence', [
    [
    ]
])
def test_end_to_end(arguments_sequence):
    # todo
    assert True
