from datetime import datetime
from pydantic import BaseModel

from Module import PurchaseDetail


class PurchaseDTO(BaseModel):
    """
    Data Transfer Object (DTO) for Purchase.
    This class is used to transfer data between different layers of the application.
    """

    id: int
    name: str
    persons_id: list[int]
    products_id: list[int]
    date: datetime
    purchase_detail: list[object]