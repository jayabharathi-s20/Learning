#Ocp--2. Open/Closed Principle
'''This principle states that "Software entities (classes, modules, functions, etc.) 
should be open for extension, but closed for modification" which means you 
should be able to extend a class behavior, without modifying it.'''

from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def calculate(self, amount):
        pass

# Extension 1
class RegularDiscount(Discount):
    def calculate(self, amount):
        return amount * 0.1

# Extension 2
class VIPDiscount(Discount):
    def calculate(self, amount):
        return amount * 0.2

# Extension 3 (new feature added without changing old code)
class StudentDiscount(Discount):
    def calculate(self, amount):
        return amount * 0.3

# Function using base class
def apply_discount(discount: Discount, amount: int):
    return discount.calculate(amount)

# Usage
print(apply_discount(RegularDiscount(), 1000))
print(apply_discount(VIPDiscount(), 1000))
print(apply_discount(StudentDiscount(), 1000))