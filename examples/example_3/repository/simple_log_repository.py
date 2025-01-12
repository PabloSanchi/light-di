from examples.example_3.repository.log_repository import LogRepository

from lightdi import implementation


@implementation(qualifier="simple")
class SimpleLogRepository(LogRepository):
    def log(self, message: str):
        print(f"{message}")
