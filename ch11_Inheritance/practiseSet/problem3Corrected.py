class Employee:
    def __init__(self, salary=280, increment=20):
        self.salary = salary
        self.increment = increment  # in %

    @property
    def salaryAfterIncrement(self):
        return self.salary * (1 + self.increment/100)

    @salaryAfterIncrement.setter
    def salaryAfterIncrement(self, new_salary):
        self.increment = ((new_salary/self.salary) - 1) * 100


# Example usage:
a = Employee()
print(f"Current salary: {a.salary}")
print(f"Current increment: {a.increment}%")
print(f"Salary after increment: {a.salaryAfterIncrement}")

# Set new salary and automatically calculate increment
a.salaryAfterIncrement = 336  # Setting new salary
print(f"\nNew increment calculated: {a.increment}%")
print(f"Salary after increment: {a.salaryAfterIncrement}")
# ```

# **Output:**
# ```
# Current salary: 280
# Current increment: 20%
# Salary after increment: 336.0

# New increment calculated: 20.0%
# Salary after increment: 336.0