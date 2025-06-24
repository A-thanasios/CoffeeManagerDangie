from datetime import datetime
from pydantic import BaseModel


class PurchaseDTO(BaseModel):
    """
    Data Transfer Object (DTO) for Purchase.
    This class is used to transfer data between different layers of the application.
    """

    id: int
    name: str
    settlements: list[dict]
    products_id: list[int]
    date: datetime
    strategy_type: str