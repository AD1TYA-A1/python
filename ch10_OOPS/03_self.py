class Employee:
    salary = 300000000000
    # Class Attribute
    language = "js"  # Class Attribute

    def getInfo(self):
        print(f"The language is {self.language}. The Salary is {self.salary}")

    def greet(self):
        print(f"Good Morning!!")


# Created an object Adiesssss
Adiesssss = Employee()
Adiesssss.name = "Adiesssss"  # Instance Attribute
print(Adiesssss.salary, Adiesssss.language)
print(Adiesssss.name)
# Adiesssss.greet()       TypeError: Employee.greet() takes 0 positional arguments but 1 was given
# Adiesssss.greet() -----> On runTime gets converted into "Employee.greet(Adiesssss) but "greet" funcion do not takes in any Argument"
# Therefore to avoid this problem we put "self" as an argument where "self" is a special keyword for  self == object/Instance name ---> HERE:"Adiesssss"

Adiesssss.greet()
Adiesssss.getInfo()

# Here "name" is an Instance Attribute  and "salary" , "language" are Class Attribute
