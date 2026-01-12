# Write a program using functions to find greatest of Three Numbers
def greatestOfThree(a,b,c):
    if a>b and a>c:
        print(f"{a} is bigggest")
    elif b>a and b>c:
        print(f"{b} is biggest")
    else:
        print(f"{c} is biggest")
        

a = int(input("Enter 1st Number: \n"))
b = int(input("Enter 2nd Number: \n"))
c = int(input("Enter 3rd Number: \n"))
greatestOfThree(a,b,c)