from abc import ABC, abstractmethod

class LogRepository(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass
