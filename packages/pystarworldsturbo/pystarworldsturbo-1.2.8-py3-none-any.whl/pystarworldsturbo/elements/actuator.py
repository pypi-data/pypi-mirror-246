from typing import Type, Iterable, Any
from queue import Queue
from pyoptional.pyoptional import PyOptional

from ..common.action import Action


class Actuator():
    def __init__(self, subscribed_events: list[Type[Any]]=[]) -> None:
        self.__action_buffer: Queue[Action] = Queue()

        if not subscribed_events:
            raise ValueError("Cannot subscribe to a `None` list of event types.")
        elif not all([isinstance(t, Type) for t in subscribed_events]):
            raise TypeError("Cannot subscribe to something which is not a list of event types.")
        elif not all([isinstance(event_type, Type) and issubclass(event_type, Action) for event_type in subscribed_events]):
            raise TypeError("Cannot subscribe to something which is not a type of `Action`.")
        else:
            self.__subscribed_events: list[Type[Any]] = subscribed_events

    def subscribe_to_event_type(self, event_type: Type[Any]) -> None:
        if not event_type:
            raise ValueError("Cannot subscribe to a `None` event type.")
        elif not isinstance(event_type, Type) or not issubclass(event_type, Action):
            raise TypeError("Cannot subscribe to something which is not a type of `Action`.")
        elif event_type not in self.__subscribed_events:  # We do not want to re-subscribe.
            self.__subscribed_events.append(event_type)

    def unsubscribe_from_event_type(self, event_type: Type[Any]) -> None:
        if not event_type:
            raise ValueError("Cannot unsubscribe from a `None` event type.")
        elif not isinstance(event_type, Type) or not issubclass(event_type, Action):
            raise TypeError("Cannot unsubscribe from something which is not a type of `Action`.")
        elif event_type in self.__subscribed_events:
            self.__subscribed_events.remove(event_type)

    def is_subscribed_to(self, event_type: Type[Any]) -> bool:
        return event_type in self.__subscribed_events

    def sink(self, action: Action) -> None:
        if not action:
            raise ValueError("Cannot sink a `None` `Action`.")
        elif self.is_subscribed_to(event_type=type(action)):
            self.__action_buffer.put(action)
        else:
            raise ValueError("Cannot sink an `Action` which this `Actuator` is not subscribed to.")

    def has_pending_actions(self) -> bool:
        return not self.__action_buffer.empty()

    def source(self) -> PyOptional[Action]:
        if not self.__action_buffer.empty():
            return PyOptional.of(self.__action_buffer.get())
        else:
            return PyOptional[Action].empty()

    def source_all(self) -> Iterable[Action]:
        while not self.__action_buffer.empty():
            yield self.__action_buffer.get()
