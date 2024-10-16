# Task Tracker
- Requirements for the "project": https://roadmap.sh/projects/task-tracker
- Difficulty: **beginner**
- Tags: `Programming Language`, `CLI`, `Filesystem`

## Description
Sample solution for the "Task Tracker" project from [roadmap.sh](https://roadmap.sh/). An app is a simple CLI todo-list, implemented with Python. Core features: 
- CRUD task manipulation
- Mark tasks as *todo*, *in-progress* or *completed*
- List all tasks, or filtered by their status

## Installation and usage

In order to install and play around with this app use the following command:
```sh
pip install -e "git+https://github.com/ImSOLty/roadmap.sh-backend.git#egg=task-cli&subdirectory=Task Tracker"
```
What this command basically does is installs the `task-cli` package from this repository (`Task Tracker` subdirectory). 

**Note:** in order to run the command you need to have `Git`/`Python`/`pip` installed on your system along with the `setuptools` py-package.

---

The installed package can be used to manipulate tasks...

- Add task: `task-cli add <task-name>`
- Delete task: `task-cli delete <task-id>`
- Update task: `task-cli update <task-id> <new-task-name>`

...mark tasks...

- Mark task as **in-progress**: `task-cli mark-in-progress <task-id>`
- Mark task as **done**: `task-cli mark-done <task-id>`

...and view the list of tasks...

- Output all tasks: `task-cli list`
- Output tasks with status: `task-cli list <status>`, where `<status>` can be one of the [`done`, `in-progress`, `todo`]

---

```
-----> task-cli list    
[In progress]:

[To do]:

[Completed]:

-----> task-cli add "Wash the dishes"
Task "Wash the dishes" successfully added!

-----> task-cli add "Fix the lights"  
Task "Fix the lights" successfully added!

-----> task-cli add "Unalive the cactus" 
Task "Unalive the cactus" successfully added!

-----> task-cli list
[In progress]:

[To do]:
1. Wash the dishes       | Created: 2024-10-16 19:37:42  | Updated: 2024-10-16 19:37:42
2. Fix the lights        | Created: 2024-10-16 19:38:18  | Updated: 2024-10-16 19:38:18
3. Unalive the cactus    | Created: 2024-10-16 19:38:39  | Updated: 2024-10-16 19:38:39

[Completed]:

-----> task-cli mark-done 1
Task "Wash the dishes" marked as "done"!

-----> task-cli mark-in-progress 2
Task "Fix the lights" marked as "in-progress"!

-----> task-cli list
[In progress]:
2. Fix the lights        | Created: 2024-10-16 19:38:18  | Updated: 2024-10-16 19:39:12

[To do]:
3. Unalive the cactus    | Created: 2024-10-16 19:38:39  | Updated: 2024-10-16 19:38:39

[Completed]:
1. Wash the dishes       | Created: 2024-10-16 19:37:42  | Updated: 2024-10-16 19:39:06

-----> task-cli update 3 "Eat the cactus"
Successfully updated "Unalive the cactus" task with the new description: "Eat the cactus"!

-----> task-cli list todo
[To do]:
3. Eat the cactus        | Created: 2024-10-16 19:38:39  | Updated: 2024-10-16 19:40:00
```

## ~~Other~~
Something that i want to highlight (mostly for myself :) ):
- The solution is fully tested.
- The repository includes a GitHub Actions workflow that checks the correctness of the solution by linting and running tests.
- All modules include type annotations.
- All core classes, functions, and methods have docstrings.
- The solution is logically split into modules.
- The app can be installed via pip due to the use of setuptools.