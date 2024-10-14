import enum
import json
import typing


class Actions(enum.Enum):
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_IN_PROGRESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    LIST = "list"


class State(enum.Enum):
    EMPTY = None
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    description: str
    state: State

    def __init__(self, description: str, state: State | str = State.TODO):
        self.description = description
        self.state = state if isinstance(state, State) else State(state)

    def update_description(self, new_description: str):
        self.description = new_description

    def update_state(self, new_state: State):
        self.state = new_state

    @classmethod
    def from_dict(cls, obj: dict[str: typing.Any]):
        return cls(**obj)

    def __str__(self):
        if self.state == State.DONE:
            return '\u0336'.join(self.description) + '\u0336'
        return self.description

    def to_json(self):
        return {
            "description": self.description,
            "state": self.state.value
        }
