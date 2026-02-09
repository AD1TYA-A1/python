# Write a program to filter a list of numbers div by 5
def isDiv5(l):
    if(l%5 == 0):
        return True
    return False

l = [10,2,3,90,40,45,78,8,90,75]
divBy5List = filter(isDiv5,l)
print(list(divBy5List))