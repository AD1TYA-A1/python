a = int(input('Enter value of a: '))
b = int(input('Enter value of b: '))
if (b==0):
    raise ZeroDivisionError("This is a critical Error, Our program do not allows devisoin of ZERO")
else:
    print(f"The division of {a}/{b} is {a/b}")



# SEE WHY DO WE WANT TO RAISE ERROR IN OUR PROGRAM LIKE WHYY???
# SAY If you are making a module in python and when someone Imports this module, I do not want any of the developer to make mistakes we will stop him.
# SEE THIS AS, WE SHOULD NOT HIT A KID , BUT IF HE DOES A CRITICAL MISTAKE WE SHOULD HIT HIM SOO THAT HE CANNOT DO THE MISTAKE AGAIN!! 