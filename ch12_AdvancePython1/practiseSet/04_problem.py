# Write a program to display a/b when a and b are integers. If b = 0, display infinite by handling the "ZeroDivisionError" 

try:
    a = int(input("Enter a integer Value: "))
    b = int(input("Enter a integer Value: "))
    print(a/b)
except ZeroDivisionError as e:
    print("Infinity")
except Exception as e:
    print("Enter Integer Values Only")
else:
    print("Thank You ")