# LIGHT DI
## Dependency Injection Module for Python

LightDI is a lightweight, framework-agnostic dependency injection module for Python.

## Features

- Automatic dependency resolution
- Support for qualifiers
- Abstract class inference

## Usage
### Example 1: Basic Usage
```python
from abc import ABC, abstractmethod

from lightdi import implementation, inject


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: int) -> str:
        pass

@implementation(qualifier="credit_card")
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: int) -> str:
        return f"Processed {amount} via Credit Card."

@implementation(qualifier="paypal", primary=True)
class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: int) -> str:
        return f"Processed {amount} via PayPal."

class LogTransactionRepository(ABC):
    @abstractmethod
    def save(self, amount: int) -> None:
        pass

@implementation(qualifier="in_memory")
class InMemoryLogTransactionRepository(LogTransactionRepository):
    def save(self, amount: int):
        self._write_to_file(f"Transaction saved: {amount}")

    def _write_to_file(self, message) -> None:
        with open("transactions.txt", "a") as file:
            file.write(message + "\n")

@inject
class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def checkout(self, amount) -> str:
        return self.payment_processor.process_payment(amount)

@inject
class PaymentController:
    def __init__(self, checkout_service: CheckoutService, log_transaction_repository: LogTransactionRepository):
        self.checkout_service = checkout_service
        self.log_transaction_repository = log_transaction_repository

    def process_checkout(self, amount) -> str:
        self.log_transaction_repository.save(amount)
        return self.checkout_service.checkout(amount)

if __name__ == "__main__":
    controller = PaymentController()
    print(controller.process_checkout(100))

```

### Example 2: Wire repositories to variables
```python
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

```

## Examples
- Example 1: Basic Usage | [link](examples/example_1.py)
- Example 2: Wire repositories to variable | [link](examples/example_2.py) 
- Example 3: Multi-file usage | [link](examples/example_3)
