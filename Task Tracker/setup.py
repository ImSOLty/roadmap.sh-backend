from setuptools import setup

setup(
    name='task-cli',
    version='0.0.1',
    py_modules=["task_manager", "args_parser", "classes", "file_manager", "task_manager", "actions"],
    entry_points={
        'console_scripts': [
            'task-cli=task_manager:main'
        ]
    }

)
