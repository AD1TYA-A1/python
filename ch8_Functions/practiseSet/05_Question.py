# Write a python funtion to print first "n" lines of the following pattern:
# ***
# **
# *
# FOR N = 3
    
def pattern(n):
    while(n!=0):
        p = 0
        while(p!=n):
            print("*",end="")
            p+=1
        print()
        n-=1

pattern(4)