from datetime import datetime

from examples.example_3.repository.log_repository import LogRepository

from lightdi import implementation


@implementation(qualifier="console")
class ConsoleLogRepository(LogRepository):
    def log(self, message: str):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"{current_time}: {message}")
