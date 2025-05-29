from dataclasses import dataclass

from Module import Person


@dataclass
class PurchaseSettlement:
    person: Person
    amount: float
    is_paid: bool = False