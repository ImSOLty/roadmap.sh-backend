import enum
import typing
from datetime import datetime


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
    created: datetime
    updated: datetime

    def __init__(
            self, description: str, state: State | str = State.TODO,
            created=int(datetime.now().timestamp()), updated=None
    ) -> "Task":
        self.description = description
        self.state = state if isinstance(state, State) else State(state)
        self.created = created
        self.updated = updated if updated else self.created

    def update_description(self, new_description: str) -> None:
        """
        Updates Task's description to a new one passed as an argument. Updates 'updated' param as well
        """
        self.description = new_description
        self.update_datetime_params()

    def update_state(self, new_state: State) -> None:
        """
        Updates Task's state (State) to a new one passed as an argument. Updates 'updated' param as well
        """
        self.state = new_state
        self.update_datetime_params()

    def update_datetime_params(self):
        """
        Updates Task's datetime params
        """
        self.updated = int(datetime.now().timestamp())

    @classmethod
    def from_dict(cls, obj: dict[str: typing.Any]) -> "Task":
        """
        Creates new Task instance from dictionary object of type [str: Any]
        """
        return cls(**obj)

    def __str__(self) -> str:
        datetime_part = f"\t | Created: {datetime.fromtimestamp(self.created)}" +\
            f"\t | Updated: {datetime.fromtimestamp(self.updated)}"
        return self.description + datetime_part

    def to_json(self) -> dict[str: typing.Any]:
        """
        Returns a converted instance dictionary representation
        """
        return {
            "description": self.description,
            "state": self.state.value,
            "created": self.created,
            "updated": self.updated,
        }
