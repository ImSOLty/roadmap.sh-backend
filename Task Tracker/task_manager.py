from args_parser import parse_arguments
from file_manager import read_tasks_from_file, write_tasks_to_file
from actions import perform_action, parse_tasks

ARGS_CONFIG_PATH = 'args_config.json'
TASKS_PATH = 'tasks.json'  # Requirements: "Use a JSON file to store the tasks in the current directory."


def main():
    arguments = parse_arguments(ARGS_CONFIG_PATH)
    tasks = parse_tasks(read_tasks_from_file(TASKS_PATH))
    perform_action(tasks, arguments)
    write_tasks_to_file(tasks, TASKS_PATH)


if __name__ == "__main__":
    main()
