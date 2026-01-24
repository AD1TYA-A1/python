# Write a class "Calculator" capable of finding square, cube and square root of a number.

class Calculator:

    def __init__(self, a ):
        self.a = a
        print(self.a)

    def square(self):
        print(self.a*self.a)
    
    def cube(self):
        print(self.a*self.a*self.a)

    def squareRoot(self):
        print(f"Square Root is {self.a**(1/2)}")
    


num = Calculator(9)
num.square()
num.cube()
num.squareRoot()