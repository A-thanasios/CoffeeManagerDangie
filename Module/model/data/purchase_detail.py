from dataclasses import dataclass, field, fields
from datetime import datetime


@dataclass
class PurchaseDetail:
    name: str = field()
    date: datetime = field()

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.date, datetime):
            raise ValueError("Date must be a datetime.date object")

    @staticmethod
    def __field_count__() -> int:
        return len(fields(PurchaseDetail))