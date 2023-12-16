from typing import Type

from .action_outcome import ActionOutcome
from .action_result import ActionResult
from .action import Action


class ExtendedActionResult(ActionResult):
    def __init__(self, action: Action, outcome: ActionOutcome) -> None:
        super(ExtendedActionResult, self).__init__(outcome=outcome)

        self.__action_type: Type[Action] = type(action)

    def get_action_type(self) -> Type[Action]:
        return self.__action_type

    def to_json(self) -> dict[str, str]:
        return {
            "action": self.__action_type.__name__,
            "outcome": str(self.get_outcome())
        }
