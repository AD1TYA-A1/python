# Q1 ---> Write a program to print multiplication table of a given number using For loop.

# n = int(input("Enter a Number to find Multiplication table till 10 : \n"))
# print()
# for i in range(1,11):
#     print(f"{n} X {i} = {n*i}")


# Q2 -----> Write a program to greet all person nmaes stores in a list "l" and which starts with S
#   l = ["Harry","Soham","Sachin","Rahul"]

# l = ["Harry","Soham","Sachin","Rahul"]
# for i in l:
#     if i.startswith("S") or i.startswith("s"):
#         print(f" Greetings to {i}")


# Q3 -------> Attempt problem 1 using while Loop
# i = 1;
# n = int(input("Enter a Number to find Multiplication table till 10 : \n"))
# print()
# while i!=11:
#     print(f" {n} X {i} = {n*i}")
#     i+=1

# Q4 -------> Write a program to find whether a given number is prime or not
# num = int(input("Enter a number To check If it Prime or not \n"))
# count = 0
# for i in range(1,num+1):
#     if num%i==0:
#         count+=1

# if count == 2 :
#     print("Prime")
# else:
#     print("Not Prime")


#    OR  OR OR OR OR NEW APPROACH IMPP  IMPP    IMPP    IMPP    IMPP    IMPP

# num = int(input("Enter a number To check If it Prime or not \n"))
# for i in range(2, num):
#     if num % i == 0:
#         print("Not Prime Number")
#         break

# else:
#     print("Prime Number")


# Q5 -----> Write a program to find sum of first "n" natural numbers using while Loops
# natural_Number = int(input("Enter a Natural Number to find sum till that Number \n"))
# sum = 0
# i = 1
# while i!=natural_Number+1:
#     sum = sum+i;
#     i+=1
# print(sum)


# Q6 -------> Write a program to calculate the factorial of a given number using for Loop

# fctNumber = int(input("Enter a number to find factorial of : \n"))
# factorial = 1;
# for i in range(1,fctNumber+1):
#     factorial = factorial*i
# print(f" The factorial of {fctNumber} is {factorial}")

# Q7 ------> Write a program to print the following Star Pattern
#         *
#        ***
#       *****
#   for n  = 3

# n = 3;
# for i in range (1,n+1): # For N lines
#     print(" "*(n-i), end="")
#     print("*"*((2*i)-1),end="")
#     print()


# Q8 -----> Program to print the following Star Pattern

# *
# **
# ***
# for n = 3

# n = 3;
# i = 1;
# j = 1;
# while j!=n+1:
#     prnt = 0
#     while prnt<j:
#         print("*", end="")
#         prnt+=1
#     print()
#     j+=1


# Q9 ---> Print the following Star Pattern
# for n = 3
# ***
# * *
# ***
# i = 1
# n = 3
# while i != n + 1:
#     if i == 1 or i == n:
#         for k in range(1, n + 1):
#             print("*", end="")
#     else:
#         for k in range(1, n + 1):
#             if k == 1 or k == n:
#                 print("*", end="")
#             else:
#                 print(" ", end="")
#     print()
#     i += 1


# Q10 -----> Write a program to print Multiplication Table of n using a loop in reverse Order
mulNum = int(input("Enter a number to get Multiplication Table: \n"))
i = 10
j = 1
while i!=0:
    print(f"{mulNum} X {j} = {mulNum*j}")
    j+=1
    i-=1