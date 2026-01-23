class Employee:
    salary = 300000000000
    # Class Attribute
    language = "js"  # Class Attribute

    def __init__(self, salary, language , name ):
        self.salary = salary
        self.language = language
        self.name = name

    def getInfo(self):
        print(f"The language is {self.language}. The Salary is {self.salary}")
    @staticmethod
    def greet():
        print(f"Good Morning!!")


# Created an object Adiesssss
Adiesssss = Employee(19000000000,"Python", "Admin") # Want to send parameters??? YOU CAN DO IT BY __init__ method

# Now if you do not give arguments while creating an Instance you will get an error
# Admin = Employee() ----->   TypeError: Employee.__init__() missing 3 required positional arguments: 'salary', 'language', and 'name'


print(f"I am {Adiesssss.name} and have Salary of  {Adiesssss.salary} , have specialization in {Adiesssss.language}")

# Here "name" is an Instance Attribute  and "salary" , "language" are Class Attribute
