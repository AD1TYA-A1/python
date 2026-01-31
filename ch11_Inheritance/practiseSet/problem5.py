# Write a class vector representing a vector of "n" dimentions. Overload the + and * operator which calculates the sum and the dot (.) product of them.


class vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        result = self.x + other.x, self.y + other.y, self.z + other.z
        return result   

    def __mul__(self, other):
        result = self.x * other.x + self.y * other.y + self.z * other.z
        return result   
    


v1 = vector(1,2,3)
v2 = vector(4,6,9)

print(v1+v2)
print(v1*v2)