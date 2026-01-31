# Override the __len__() method on vector of problem 5 to display the dimention of the vector


class vector:
    def __init__(self, l):
        self.l = l
        self.x = l[0]
        self.y = l[1]
        self.z = l[2]

    def __add__(self, other):
        result = self.x + other.x, self.y + other.y, self.z + other.z
        return result

    def __mul__(self, other):
        result = self.x * other.x + self.y * other.y + self.z * other.z
        return result
    
    def __len__(self):
        return len(self.l)


v1 = vector([1, 2, 3])
v2 = vector([4, 6, 9])

print(v1 + v2)
print(v1 * v2)
print(len(v1))