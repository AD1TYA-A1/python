# You can use "with" statement to open multiple files. You can use multiple context managers in a single "with" statement

with(
    open("01_walrus.py") as f1,
    open("02_type.py") as f2,
):
    print(f1.read())
    print(f2.read())