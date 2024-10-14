import enum
import typing


class Actions(enum.Enum):
    """
    Enum class representing possible actions performed by user
    """
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    MARK_IN_PROGRESS = "mark-in-progress"
    MARK_DONE = "mark-done"
    LIST = "list"


class State(enum.Enum):
    """
    Enum class representing the state of tasks
    """
    EMPTY = None
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task:
    """
    Class, representing Task instance, has description and state attributes
    """
    description: str
    state: State

    def __init__(
            self, description: str, state: State | str = State.TODO
    ) -> "Task":
        self.description = description
        self.state = state if isinstance(state, State) else State(state)

    def update_description(self, new_description: str) -> None:
        """
        Updates Task's description to a new one passed as an argument
        """
        self.description = new_description

    def update_state(self, new_state: State) -> None:
        """
        Updates Task's state (State) to a new one passed as an argument
        """
        self.state = new_state

    @classmethod
    def from_dict(cls, obj: dict[str: typing.Any]) -> "Task":
        """
        Creates new Task instance from dictionary object of type [str: Any]
        """
        return cls(**obj)

    def __str__(self) -> str:
        if self.state == State.DONE:
            return '\u0336'.join(self.description) + '\u0336'
        return self.description

    def to_json(self) -> dict[str: typing.Any]:
        """
        Returns a converted instance dictionary representation
        """
        return {
            "description": self.description,
            "state": self.state.value
        }
