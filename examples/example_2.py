from abc import ABC, abstractmethod

from lightdi import implementation, wire


class LogRepository(ABC):
    @abstractmethod
    def log(self, message):
        pass

@implementation(qualifier="console")
class ConsoleLogRepository(LogRepository):
    def log(self, message):
        print(message)

@implementation(qualifier="timestamp", primary=True)
class TimeStampLogRepository(LogRepository):
    def log(self, message):
        print(f"{__import__('datetime').datetime.now()}: {message}")

if __name__ == "__main__":
    logger = wire(LogRepository)
    logger.log("message to be logged")

    console_logger = wire(LogRepository, qualifier="console")
    console_logger.log("message to be logged")
