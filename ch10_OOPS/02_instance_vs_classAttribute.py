# Instance Variable take preference over class attributes during assignment and retrieval 

class Employee:
    salary = 300000000000; # Class Attribute
    language = "js"        # Class Attribute

# Created an object Aditya
Aditya = Employee()
Aditya.language = "python" # Instance Attribute

# Here this line "Aditya.language" ---> changes the value of class Attribute from "js" to "python" as Instance Attributes are given more priority than that of class Attributes 
# This means see:
# When looking for harry.attribute it checks for the following:
#     1) Is Attribute present in Object?        ----> First it checks this 
#     2) Is Attribute present in class?         ----> Then it goes for this 
print(Aditya.salary, Aditya.language)


