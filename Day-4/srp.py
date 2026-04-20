#Single Responsibility Principle (SRP): Each module or class should have one responsibility, meaning it should have a single reason to change.

#Without SRP
class User:
    def __init__(self, name):
        self.name = name

    def print_user_info(self):
        # Print user information
        pass

    def store_user_data(self):
        # Store user data in some storage
        pass

#WITH SRP
class User:
    def __init__(self, name):
        self.name = name

class UserPrinter:
    @staticmethod
    def print_user_info(user):
        # Print user information
        pass

class UserDataStore:
    @staticmethod
    def store_user_data(user):
        # Store user data in some storage
        pass


#Example
def validate_order(order):
    if order["amount"] <= 0:
        raise ValueError("Invalid amount")


def save_order(order):
    print(f"Order saved: {order['id']}")


def generate_invoice(order):
    print(f"Invoice generated for order {order['id']}")


def send_email(order):
    print(f"Email sent for order {order['id']}")


def process_order(order):
    validate_order(order)
    save_order(order)
    generate_invoice(order)
    send_email(order)


# 👉 REAL DATA
order_data = {
    "id": 101,
    "amount": 500
}

process_order(order_data)