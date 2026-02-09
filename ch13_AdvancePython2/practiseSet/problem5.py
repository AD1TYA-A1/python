# Write a program to find the maximum of the numbers in a list using the reduce function
from functools import reduce
def findMax(a,b):
    if(a>b):
        return a
    return b

l = [12,34,1,5,44,9,8,90]
maxInL = reduce(findMax,l)
print(maxInL)