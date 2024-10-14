from args_parser import parse_arguments
from file_manager import read_tasks_from_file, write_tasks_to_file
from actions import perform_action, parse_tasks

ARGS_CONFIG_PATH = 'configs/args_config.json'
# Requirements: "Use a JSON file to store the tasks in the current directory."
TASKS_PATH = 'tasks.json'


def main() -> None:
    """
    The main function of the program, performing the following stages:
    1. Parses arguments passed from the user
    2. Parses tasks from the file (with tasks)
    3. Performs the required action
    4. Writes tasks to a file
    """
    arguments = parse_arguments(ARGS_CONFIG_PATH)
    tasks = parse_tasks(read_tasks_from_file(TASKS_PATH))
    perform_action(tasks, arguments)
    write_tasks_to_file(tasks, TASKS_PATH)


if __name__ == "__main__":
    main()
