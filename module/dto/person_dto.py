from pydantic import BaseModel

class PersonDTO(BaseModel):
    """
    Data Transfer Object (DTO) for Person.
    This class is used to transfer data between different layers of the application.
    """

    id: int
    first_name: str
    last_name: str
    middle_name: str
    days_per_week: int
    is_buying: bool
    img: str

