# Create a class with a class attribute a; create an object from it and set "a" directly using object.a  = 0. Does this change the class Attribute?
#               NOOOOO!!!

class setA:
    a = 10



z = setA()
print(z.a)      # Prints the class Attribute because Instance Attribute was not set or present. 

z.a = 0         # A new Instance Attribute has been set
print(z.a)      # Prints the Instance Attribute because Instance Attribute is present (more priority than that of class Attribute) 

print(setA.a)   # Class attribute remains the same
