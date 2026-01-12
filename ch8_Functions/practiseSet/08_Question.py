# Write a python function to print the multiplication table of a given number
def multiplicationTable(n):
    for i in range(1,11):
        print(f"{n} X {i} = {n*i}")

n = int(input("Enter a number you want to find Multiplicatin Table of : "))
multiplicationTable(n)