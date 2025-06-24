from dataclasses import dataclass, field, fields

from Module.Model.person import Person


@dataclass
class PurchaseSettlement:
    person: Person = field()
    amount: float = field()
    is_paid: bool = field(default=False)

    def __post_init__(self):
        if not isinstance(self.person, Person):
            raise TypeError(f"Expected a Person instance, got {type(self.person).__name__}")
        if not isinstance(self.amount, (int, float)) or self.amount < 0:
            raise ValueError("Amount must be a non-negative number")
        if not isinstance(self.is_paid, bool):
            raise TypeError("is_paid must be a boolean value")


    @staticmethod
    def __field_count__() -> int:
        return len(fields(PurchaseSettlement))