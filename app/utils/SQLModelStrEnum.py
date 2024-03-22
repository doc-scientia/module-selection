from enum import StrEnum


class SQLModelStrEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        # SQLModel uses the 'name' field as SQL enum values.
        # Given by default the auto() value is the lowercase version
        # of the name, we forcibly align the two behaviours
        return name

    @classmethod
    def members(cls) -> list[str]:
        return [e.value for e in cls]
