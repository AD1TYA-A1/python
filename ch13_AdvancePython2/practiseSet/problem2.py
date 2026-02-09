# Write a program to input name, marks and phoneNumber of a student and format it using format function like below:
"The name of the student is Harry, his marks are 72 and phoneNumber is 9999888890"

name = input("Enter Name: ")
marks = int(input("Enter Marks: "))
phone = int(input("Enter PhoneNumber: "))

s = "The name of the student is {1}, his marks are {0} and phoneNumber is {2}".format(marks,name, phone)
print(s)
