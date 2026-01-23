class Employee:
    language = "JAVA",
    salary = 980000000000

    def info(self):
        type(self)
        print(f"I am {self.name}, with Salary {self.salary}")
    
    # Here I see I need to pass the object to this wish function but there is no use of self object soooooo This will increase space Complexity of program soo to fix this I am like declaring this wish as a "static method"
#       Admin.wish() ----------> FOR NO SELF GIVEN
#     ~~~~~~~~~~^^
# TypeError: Employee.wish() takes 0 positional arguments but 1 was given
    @staticmethod    # ---------> means wish() is a static method and it doesnt require object
    def wish():
        print("Good Morning!!!")


# STATIC METHOD IS A "DECORATOR"


Admin = Employee()
Admin.name = "Admin"
Admin.wish()        # this works without any error because it is an static method(No need of    Instance/Object)
Admin.info()

