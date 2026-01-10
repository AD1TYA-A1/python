# Funtion Defination = The part containing exact set of instructions which are executed during the function call.

# Function Defintion Starts
def add(a, b):
    return a + b
# Function Defintion Ends


sum = add(100, 9)  # Function Call
print(sum)
sum = add(10, 9)
print(sum)
sum = add(0, 9)
print(sum)


# Concept of Default Parameters
def wish(name,greet = "Hello"):     # greet is a default parameter which takes default value as "Hello" if user dosn't pass any value to wish's 2nd Argument
    print(f"{greet} {name}")


wish("Aditya")  # Output: Hello Aditya
wish("Aditya","Welcome")    # Output: Welcome Aditya


