from dataclasses import dataclass

from MVP.Module.model.person import Person


@dataclass
class PurchaseSettlement:
    person: Person
    amount: float
    is_paid: bool = False