from setuptools import setup

setup(
    name='myscript',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'task-cli=task_manager:main'
        ]
    }
)
