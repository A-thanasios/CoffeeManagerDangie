from Module.Model.data.person_detail import PersonDetail


class Person:
    def __init__(self, **kwargs):
        if 'id' in kwargs and (not isinstance(kwargs['id'], int) or kwargs['id'] < 0):
            raise ValueError("ID must be a positive integer or None")

        self.__id = kwargs.pop('id', None)
        self.__person_detail = PersonDetail(**kwargs)


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
    def detail(self) -> PersonDetail:
        return self.__person_detail

    @property
    def person_detail_dict(self) -> dict[str, str | int | bool]:
        return {
                "name": self.__person_detail.name,
                "e_mail": self.__person_detail.e_mail,
                "days_per_week": self.__person_detail.days_per_week,
                "is_buying": self.__person_detail.is_buying,
                }

    @property
    def detail_field_count(self):
        return self.__person_detail.__field_count__()

    __eq__ = lambda self, other: (isinstance(other, Person)
                                  and self.__person_detail.name == other.__person_detail.name)

    def __str__(self):
        return f'{self.__id}: {self.__person_detail.name}'
