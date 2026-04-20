# Docstrings (Documentation Strings) are special strings used to document Python code.


def greet(name):
    """This function greets the user by their name."""
    return f"Hello, {name}!"


a = greet("Jaya")
print(a)

print(greet.__doc__)

# Types of Docstrings


# 1. Triple-Quoted Strings
def my_func():
    """This is a docstring using triple single quotes."""
    pass


# 2. Google Style Docstrings


def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a (int): First number.
        b (int): Second number.

    Returns:
        int: Product of a and b.
    """
    return a * b


print(multiply(3, 5))

# 3. Numpydoc Style Docstrings


def divide(a, b):
    """
    Divide two numbers.

    Parameters
    ----------
    a : float
        Dividend.
    b : float
        Divisor.

    Returns
    -------
    float
        Quotient of division.
    """
    if b == 0:
        raise ValueError("Division by zero not allowed.")
    return a / b


print(divide(6, 2))


# 4. One-line Docstrings
def power(a, b):
    """Return a raised to power b."""
    return a**b


print(power.__doc__)
