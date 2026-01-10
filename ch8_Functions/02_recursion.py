
# Function stack keeps moving if there is no base condition to exit the recursion here base condition is inside "if"
def factorial(n):
    if n==1 or n==0:    # Base condition to resolve Recursion
        return 1

    return n*factorial(n-1)

n = int(input("Enter a number to find factorial of : \n"))
print(f"Factorial of {n} is {factorial(n)}")