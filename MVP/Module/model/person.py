from MVP.Module.model.data.person_detail import PersonDetail


class Person:
    def __init__(self, person_detail: PersonDetail, db_id: int = None):
        if not isinstance(person_detail, PersonDetail):
            raise ValueError("PersonDetail must be a valid PersonDetail object")
        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")

        self.__id = db_id
        self.__person_detail = person_detail


    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        if self.__id:
            raise ValueError("ID is already set and cannot be changed")

        if not isinstance(value, int) or value < 0:
            raise ValueError("ID must be a positive integer")
        self.__id = value

    @property
    def person_detail(self):
        return self.__person_detail