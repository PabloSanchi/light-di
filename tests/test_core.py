import unittest
from abc import ABC, abstractmethod

from lightdi import container, implementation, inject, wire


class TestDependencyInjection(unittest.TestCase):
    def setUp(self):
        container._abstract_to_impl.clear()

    def test_register_and_resolve_default(self):
        class MyAbstract(ABC):
            @abstractmethod
            def do_something(self):
                pass

        @implementation()
        class MyImplementation(MyAbstract):
            def do_something(self):
                return "I did something!"

        instance = container.resolve(MyAbstract)
        self.assertIsInstance(instance, MyImplementation)
        self.assertEqual(instance.do_something(), "I did something!")

    def test_register_with_qualifiers(self):
        class PaymentProcessor(ABC):
            @abstractmethod
            def process_payment(self, amount):
                pass

        @implementation(qualifier="credit_card")
        class CreditCardProcessor(PaymentProcessor):
            def process_payment(self, amount):
                return f"Processed {amount} via Credit Card."

        @implementation(qualifier="paypal", primary=True)
        class PayPalProcessor(PaymentProcessor):
            def process_payment(self, amount):
                return f"Processed {amount} via PayPal."

        credit_card_processor = container.resolve(PaymentProcessor, qualifier="credit_card")
        self.assertIsInstance(credit_card_processor, CreditCardProcessor)
        self.assertEqual(credit_card_processor.process_payment(100), "Processed 100 via Credit Card.")

        paypal_processor = container.resolve(PaymentProcessor, qualifier="paypal")
        self.assertIsInstance(paypal_processor, PayPalProcessor)
        self.assertEqual(paypal_processor.process_payment(200), "Processed 200 via PayPal.")

    def test_automatic_dependency_injection(self):
        class Service(ABC):
            @abstractmethod
            def execute(self):
                pass

        @implementation()
        class MyService(Service):
            def execute(self):
                return "Executed!"

        @inject
        class Client:
            def __init__(self, service: Service):
                self.service = service

            def run(self):
                return self.service.execute()

        client = Client()
        self.assertEqual(client.run(), "Executed!")

    def test_missing_implementation_raises_error(self):
        class MissingAbstract(ABC):
            @abstractmethod
            def do_something(self):
                pass

        with self.assertRaises(TypeError):
            container.resolve(MissingAbstract)

    def test_wire_impl(self):
        class MyAbstract(ABC):
            @abstractmethod
            def do_something(self):
                pass

        @implementation()
        class MyImplementation(MyAbstract):
            def do_something(self):
                return "I did something!"

        impl = wire(MyAbstract)
        self.assertIsInstance(impl, MyImplementation)
        self.assertEqual(impl.do_something(), "I did something!")