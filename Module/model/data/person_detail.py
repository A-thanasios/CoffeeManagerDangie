from dataclasses import dataclass, field, fields


@dataclass
class PersonDetail:
        name: str = field()
        e_mail: str = field()
        days_per_week: int = field()
        is_buying: bool = field(default=True)


        def __post_init__(self):
            if not isinstance(self.name, str) or not self.name:
                raise ValueError("Name must be a non-empty string")
            if not isinstance(self.e_mail, str) or '@' not in self.e_mail:
                raise ValueError("E-mail must be a valid string containing '@'")
            if not isinstance(self.days_per_week, int) or not (0 <= self.days_per_week <= 5):
                raise ValueError("days_per_week must be an integer between 0 and 5")
            if not isinstance(self.is_buying, bool):
                raise ValueError("is_buying must be a boolean")

        @staticmethod
        def __field_count__() -> int:
            return len(fields(PersonDetail))