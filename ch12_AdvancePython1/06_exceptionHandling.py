try:
    a = int(input("Enter your Number: "))
    print(a)

except Exception as e:
    print(e)

# This avoids Crashing the program 
# If there will be not try catch and user give a wrong input to "a" the program will crash at that moment will not go for further execution 


# BUT WHEN WE USE TRY CATCH, It catches the exception and shows it to the user Without crashing the program that is WHY, print("Thank You") is working or else it would have crashed and no pirnt 
# 
# 
# IT IS THE DUTY OF A PROGRAMMER TO MAKE A PROGRAM THAT DOES NOT CRASH   

print("Thank You")