# Create a class (2-D Vector) and use it to craete another class representing a (3-D Vector)


class _2D_Vector:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def show(self):
            print(f"The 2D coordinates are: {self.i}i , {self.j}j")


class _3D_Vector(_2D_Vector):
    def __init__(self, i, j, k):
        self.k = k
        super().__init__(i, j)

    def show(self):
        print(f"The 3D coordinates are: {self.i}i, {self.j}j,  {self.k}k ")


a = _2D_Vector(3,6)
b = _3D_Vector(1, 3, 5)
a.show()
b.show()