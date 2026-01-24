# Add a static method in problem 2, to greet user with hello.


# Q2 ----> Write a class "Calculator" capable of finding square, cube and square root of a number.


class Calculator:

    def __init__(self, a):
        self.a = a

    @staticmethod
    def greet():
        print("Greetings to User    :)   ")

    def square(self):
        print(self.a * self.a)

    def cube(self):
        print(self.a * self.a * self.a)

    def squareRoot(self):
        print(f"Square Root is {self.a**(1/2)}")


num = Calculator(9)
num.greet()
num.square()
num.cube()
num.squareRoot()
