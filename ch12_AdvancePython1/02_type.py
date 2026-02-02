# This is a new feature in python program LIKE typeScript
# This allows user to set the type of variable or type of function EXPLICITALLY to improve the readability of the program!!!


# Advance TypeHints(Like int, str)
from typing import List, Tuple, Dict, Union

# List of Integers
numbers: List[int] = [1, 2, 3, 4, 5, 6, 7]
# You can Also add STR type value inside a list

# Tuple of a String and an Integer
person: tuple[str, int] = ("Hello", 34, "I am", 60)  # A tuple of str and Integers Types


# Dict with string Keys and Integer Values
scores:dict[str,int] = {"Admin":90, "Aditya":100}

n: int = 5


def sum(a: int, b: int) -> int:
    return a + b


print(sum("A", "Z"))
print(sum(10, 2))
# =====> IMP============>IMP=======>IMP=========>IMP=======>IMP=========>IMP


# Python's type hints are NOT enforced at runtime - they're just hints for developers and tools. Python remains dynamically typed, so the interpreter doesn't actually check or enforce these types when your code runs.
