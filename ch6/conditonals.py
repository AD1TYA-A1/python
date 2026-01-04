age = int(input("Enter Your Age : "))
# if (age >= 18): IS ====== TO if age >= 18:
# "if elif else" LADDER IS ALSO DEMONSTRATED HERE!!!
if age >= 18:
    print("You can Vote")
    print("Goo Ahead!!!")
elif age < 0:
    print("Do not Add Neatuve Age")
elif age == 0:
    print("0 is not a valid Age")
else:
    print("You Cannot Vote")

print("Program Ended")
