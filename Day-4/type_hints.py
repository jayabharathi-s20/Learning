from typing import Optional, List, Tuple, Union, Callable

# TYPE HINTS

# Type hints are a feature in Python that allow developers to annotate their code with expected types for variables and function arguments.

# 1.Variable and Function Type Hints
age: int = 25


def greet(name: str) -> str:
    return f"Welcome {name}"


a = greet("jaya")
print(a)


# 2. Function Return Type
def add(x: int, y: int) -> int:
    return x + y


y = add(10, 4)
print(y)

# To install mypy
"""
python3 -m pip install mypy

Check installation:

mypy --version

"""
"""
Use a type checker:

mypy your_file.py

"""

# 3. Optional Types and Collections


def get_user(id: int) -> Optional[str]:
    return None if id == 0 else "User"


x = get_user(12)
print(x)

# def get_user(id: int) -> str | None:
#     return None if id == 0 else "User"

# x=get_user(12)
# print(x)


def total(num: List[int]) -> int:
    return sum(num)


sum_of_numbers = total([10, 23, 5, 4])
print(sum_of_numbers)


def get_name_and_age() -> Tuple[str, int]:
    return ("Abc", 25)


z = get_name_and_age()
print(z)

# 4. Union Types
# def maths(a:int|str):
#     print(a)
# maths("25")


def maths(a: Union[int | str]):
    print(a)


maths("25")

# 5.Function Types


def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)


# A function that matches the Callable type
def square(x: int) -> int:
    return x * x


result = apply(square, 5)
print(result)
