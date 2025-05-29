from dataclasses import dataclass
from datetime import datetime


@dataclass
class PurchaseDetail:
    name: str
    date: datetime

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.date, datetime):
            raise ValueError("Date must be a datetime.date object")