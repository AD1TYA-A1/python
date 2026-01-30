# Create a class "Employee" and add salary and increment properties to it.
# Write a method "salaryAfterIncrement" method with a @property decorator with a setter which changes the value of increment based on salary


# newSalary = oldSalary(1+increment/100)
# increment = ((newSlary/oldSalary)-1)*100

class Employee:
    # Class property or class Atrribute
    salary = 290
    increment = 20  # in % like 20% increment in salary

    @property
    def salaryAfterIncrement(self):
        return (((self.salary)*self.increment)/100)+self.salary

    @salaryAfterIncrement.setter
    def salaryAfterIncrement(self,salary):
        self.increment = ((salary/self.salary)-1)*100




    # @salaryAfterIncrement.setter
    # def salaryAfterIncrement(self):
    #     self.newSalary = (((self.salary) * 20) / 100) + self.salary


a = Employee()
a.salaryAfterIncrement = 280 
print(a.salaryAfterIncrement)

# # Instance Attrribute
# a.salary = 2340000
# a.increment = 20  #in % like 20% increment in salary
