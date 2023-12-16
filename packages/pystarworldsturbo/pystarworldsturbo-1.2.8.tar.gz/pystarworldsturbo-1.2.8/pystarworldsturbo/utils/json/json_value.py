from typing import TypeAlias


JSONValue: TypeAlias = None | str | int | float | bool | list["JSONValue"] | dict[str, "JSONValue"]
