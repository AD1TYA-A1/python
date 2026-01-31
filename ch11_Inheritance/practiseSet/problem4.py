# Write a class "Complex" to represent complex numbers, along with overloaded operators "+" and "*" which adds and multiplies them


class complex:
    def __init__(
        self, r, i
    ):  # r = real part of the number , i = imaginary part of the number
        self.r = r
        self.i = i

    def __add__(
        self, c2
    ):  # This is a Dunder Method that makes manupilates "+" operator to work in another way as user wants
        return complex(self.r + c2.r, self.i + c2.i)
    
    def __mul__(self, c2):
            # (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
            real_part = self.r * c2.r - self.i * c2.i
            imaginary_part = self.r * c2.i + self.i * c2.r
            return complex(real_part, imaginary_part)


    def __str__(self):
        return f"{self.r} + {self.i}i "

c1 = complex(1, 3)
c2 = complex(4, 5)
# print(c1.__add__(c2))
# or
print(c1 + c2)
print(c1 * c2)
