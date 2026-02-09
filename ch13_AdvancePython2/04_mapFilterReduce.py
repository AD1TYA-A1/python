from functools import reduce

l = [1,2,3,4,5,6]
# Map Example
square = lambda x: x*x
sqList = map(square,l)
print(list(sqList))

# Filter example
def isEven(l):
    if(l%2==0):
        return True
    return False

onlyEven = filter(isEven,l)
print(list(onlyEven))



# Reduce Example
sum = lambda x,y: x+y
mul = lambda a,b: a*b
totalSum = reduce(sum,l)
print(totalSum) 
print(reduce(mul,l)) 