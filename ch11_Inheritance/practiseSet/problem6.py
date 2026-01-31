# Write an "__str__()" method to print vector as follows:
# 7i + 8j + 10k
# Assume vector of dimention 3 for this problem
class vector:
    def __init__(self, i, j, k):
        self.i = i
        self.j = j
        self.k = k

    def __str__(self):
        return f"{self.i}i + {self.j}j + {self.k}k"
    
v1 = vector(7,8,10)
print(v1)
