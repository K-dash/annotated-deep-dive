from dataclasses import dataclass, field
from typing import Annotated, get_type_hints


def validate_age(min_val: int, max_val: int):
    def validator(value):
        if not (min_val <= value <= max_val):
            raise ValueError(f"入力できる数値の範囲は {min_val} 〜 {max_val} です")
        return value
    return validator


@dataclass
class User:
    age: Annotated[int, validate_age(0, 120)] = field()

    def __post_init__(self):
        type_hints = get_type_hints(self, include_extras=True)
        for name, type_hint in type_hints.items():
            if hasattr(type_hint, '__metadata__'):
                for metadata in type_hint.__metadata__:
                    if callable(metadata):
                        setattr(self, name, metadata(getattr(self, name, None)))

# success
user = User(age=120)

# error
# user = User(age=130)
print(user.age)
