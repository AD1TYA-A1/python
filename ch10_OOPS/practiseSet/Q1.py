# Create a class "Programmer" for storing information of a few programmer working at Microsoft.

class Programmer:
    company = "Microsoft"
    def __init__(self,name,salary,pin):
        self.name = name
        self.salary = salary
        self.pin = pin

Admin = Programmer("Admin" , 130000000 , 249145 )
print(Admin.name,Admin.salary, Admin.pin)

Aditya = Programmer("Aditya", 19000000000 , 249001)
print(Aditya.name,Aditya.salary,Aditya.pin)





