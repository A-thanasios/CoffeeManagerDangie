class Name:
    def __init__(self, first_name: str, last_name: str, middle_name=''):
        if not first_name or not isinstance(first_name, str) or first_name == '':
            raise ValueError("First name must be a non-empty string.")
        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name must be a non-empty string.")

        if (middle_name != '') and not isinstance(middle_name, str):
            raise ValueError("Middle name must be a string or empty string.")

        self.__first_name = first_name
        self.__last_name = last_name
        self.__middle_name = middle_name

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("First name must be a non-empty string.")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Last name must be a non-empty string.")
        self.__last_name = value

    @property
    def middle_name(self):
        return self.__middle_name

    @middle_name.setter
    def middle_name(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Middle name must be a string or None.")
        self.__middle_name = value
    
    @property
    def full_name(self):
        if self.__middle_name:
            return f"{self.__first_name} {self.__middle_name} {self.__last_name}"
        return f"{self.__first_name} {self.__last_name}"

    def __eq__(self, other):
        if not isinstance(other, Name):
            return False
        return self.full_name == other.full_name
    
    def __str__(self):
        return self.full_name
