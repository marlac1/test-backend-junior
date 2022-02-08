from copy import deepcopy as copy
from enum import Enum
from typing import Any, Dict, Set

from pydantic import BaseModel


class Entity(BaseModel):
    initial_values: dict

    def __init__(self, **data: Any) -> None:
        data["initial_values"] = copy(data)
        super().__init__(**data)

    def dict(
        self,
        *,
        include: Any = None,
        exclude: Any = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        if not exclude:
            exclude = {"initial_values"}
        else:
            if isinstance(exclude, set):
                exclude.add("initial_values")
            else:
                exclude

        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )

    def to_log(self) -> Dict:
        return self.dict(exclude={"initial_values"})

    def updated_fields(self) -> Set[str]:
        modified_key: Set[str] = set()
        for key, value in self.__dict__.items():
            if key == "initial_values":
                pass

            if key not in self.initial_values or value != self.initial_values[key]:
                modified_key.add(key)

        return modified_key


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHERS = "others"


class Player(Entity):
    id: str = ""
    nickname: str
    phone_number: str
    gender: Gender = Gender.OTHERS
