from lightdi import inject

from examples.example_3.repository.log_repository import LogRepository

@inject
class LogService:
    def __init__(self, log_repository: LogRepository):
        self.log_repository = log_repository
    
    def log(self, message: str) -> None:
        self.log_repository.log(message)