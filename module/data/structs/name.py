class Name:
    def __init__(self, first_name, last_name, middle_name=None):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__middle_name = middle_name
    
    @property
    def first_name(self):
        return self.__first_name
    
    @property
    def last_name(self):
        return self.__last_name
    
    @property
    def middle_name(self):
        return self.__middle_name
    
    @property
    def full_name(self):
        if self.__middle_name:
            return f"{self.__first_name} {self.__middle_name} {self.__last_name}"
        return f"{self.__first_name} {self.__last_name}"
    
    def __str__(self):
        return self.full_name
