# WE CAN MANUPILATE OPERATORS WHEN WORKING WITH CLASSES 

class Number:
    def __init__(self,n):
        self.n = n

    def __add__(self, num):
        return f"{self.n} - {num.n} = {self.n-num.n}"
    
    def __len__(self):
        return 90 


n = Number(2)
m = Number(3)
# n+m ====> #n__add__(m)
print(n+m)
print(len(n))   # This gives "90" as Output I have MANUPILATED THIS LEN FUNCTION

# WHAT IS THE NEED OF THIS MANUPILATION:
# The Key Idea:
# Use __len__() when your object has something you can count or measure:

# Book → count pages
# Playlist → count songs
# Shopping cart → count items
# Bank account → maybe count transactions

# Don't use it for things like a single number, a person's age, or a temperature - those don't have a "length"!


# a.__add__(b) ====>a+b
# a.__sub__(b) ====>a-b
# a.__mul__(b) ====>a*b
# a.__truediv__(b)=>a/b
# a.__floordiv__(b)=>a//b
# a.__str__(b)
# __len()__    =====> used to set what gets displayed upon calling  .__len__() or len(obj) 