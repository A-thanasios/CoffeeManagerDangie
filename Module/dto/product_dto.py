from pydantic import BaseModel


class ProductDTO(BaseModel):
    """
    Data Transfer Object (DTO) for Product.
    This class is used to transfer data between different layers of the application.
    """

    id: int
    name: str
    shop: str
    cost: int