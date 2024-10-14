import enum
import subprocess
import os
import pytest


class Actions(enum.Enum):
    UNEXISTING = "whatever"
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_IN_PROGRESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    LIST = "list"


# Todo: remove (will be passed through workflows)
os.environ = {
    "INTERPRETER": "python",
    "PATH_TO_SCRIPT": "task_manager.py",
    "TASKS_FILE_NAME": "tasks.json",
}

COMMAND = f"{os.getenv('INTERPRETER')} {os.getenv('PATH_TO_SCRIPT')}"
TASKS_FILE_NAME = os.getenv('TASKS_FILE_NAME')
PATH_TO_TASKS_FILE = os.path.join(os.path.dirname(__name__), TASKS_FILE_NAME)


class Mocker:
    execution_command: str
    process: subprocess.CompletedProcess[bytes]
    executed: bool

    def __init__(self, args):
        self.executed = False
        arguments_as_string = [
            # convert to str if enum Actions
            arg.value if isinstance(arg, Actions) else arg for arg in args
        ]
        self.execution_command = COMMAND + " " + " ".join(arguments_as_string)

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


@pytest.fixture(autouse=True)
def clear_file_on_test_start():
    yield
    clear_tasks_file()


@pytest.mark.parametrize("arguments", [
    [],
    [Actions.ADD],
    [Actions.DELETE],
    [Actions.UPDATE],
    [Actions.UPDATE, "0"],
    [Actions.UPDATE, "tmp_task"],
    [Actions.MARK_IN_PROGRESS],
    [Actions.MARK_DONE],
])
def test_missing_required_arguments(arguments):
    mocker = Mocker(arguments)
    mocker.run()
    assert all(token in mocker.stderr for token in ["usage", "error", "arguments are required"])
