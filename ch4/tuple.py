# String --> Immutable
# List ----> Mutable + Stores Multiple Values of different types
# Tuple ----> Immutable + Stores Multiple Values of different types

# By () -- Rounded braces we can Start initializing Tuple
a = (1, True, "Admin", 43.3)
print(type(a))
# <class 'tuple'>
# a[1] = False; ==Cnnot Modify Tuple as it is IMMUTABLE

# FUNCTIONS OF TUPLE
b = (12, 4445, "True", "True", True)
no = b.count(b[2])
print(no)


i = b.index("True")
# 3 Gives the end True
print(i)

len = len(b)
print(len);