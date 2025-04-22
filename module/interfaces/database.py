from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def exists(self):
        pass