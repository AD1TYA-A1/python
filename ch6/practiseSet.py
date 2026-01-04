#  Q1----> Write a program to find the greatest of four numbers entered by the user
a = b = c = d=None
a = int(input("Enter Number : "))
b = int(input("Enter Number : "))
c = int(input("Enter Number : "))
d = int(input("Enter Number : "))

if (a>b and a>c and a>d) :
    print( a, " is Greatest")
elif (b>a and b>c and b>d):
    print(b," is Greatest")
elif (c>a and c>b and c>d):
    print(c," is Greatest")
else:
    print(d," is Greatest")


# Q2--->Write a program to find out wether the student have passed or failed if it requires a total of 40% and at least 33% in subject to pass.Assume 3 subjects and total marks as an input from the user

math = int(input("Enter your Marks in Mathematics:  "))
enlgish = int(input("Enter your Marks in Enlgish :  "))
biology = int(input("Enter your Marks in Biology :  "))
drawing = int(input("Enter your Marks in drawing :  "))

if math < 33 or enlgish < 33 or biology < 33 or drawing < 33:
    print("You failed, as you scored less that 33 in one of your subject ")
else:
    percentage = ((math + biology + enlgish + drawing) / 400) * 100
    if percentage < 40 :
        print("Ypu faild because your % is less than 40 ")
        print("Percentage : ",percentage)
    else:
        print("You Passed!!!")
        print("Your percentage : ",int(percentage),"%")


# Q3----->A spam comment is defined as a text containnig the following keywords
# "Make a lot of money", "buy now" , "subscribe this" , "click this".
#   WRITE  A PROGRAM TO DETETCT THESE SPAMS!!

comment = input("Enter your comment to check if it spam or not: ")
list = ["make a lot of money", "buy now", "subscribe this", "click this"]
lowerComment = comment.lower()
if lowerComment.find(list[0]) != -1 :
    print("Spam")
elif lowerComment.find(list[1]) != -1 :
    print("Spam")
elif lowerComment.find(list[2]) != -1 :
    print("Spam")
elif lowerComment.find(list[3]) != -1 :
    print("Spam")
else:
    print("Not Spam")

# Q4 -------> Write a program to find wether a given UserName contains lesss than 10 charectors or not!!
userName = input("Enter Your userName to check if it is of 10 charectors or Not: \n")
if len(userName)<10:
    print("Length of UserName is less than 10")
else:
    print("Length of UserName is greator than 10")


#  Q5--------> Write a program to find out wether a given name is present in a list or Not.
people = [
    "Aarav",
    "Ananya",
    "Arjun",
    "Emily",
    "Diya",
    "Michael",
    "Ishaan",
    "Sarah",
    "Kavya",
    "Krishna",
    "David",
    "Meera",
    "Rohan",
    "Jessica",
    "Saanvi",
    "Vihaan",
    "Priya",
    "Amit",
    "Sneha",
    "Vikram",
]
pName = input("Enter your name to check if It is present in list or not: \n")
if pName in people:
    print("Name is present in the List")
else:
    print("Name is not present in the List")

# Q6 --------> Write a program to calculate the grade of the student based on following schema:
# 90-100 >> Excellent
# 80-90 >> A
# 70-80 >> B
# 60-70 >> C
# 50-60 >> D
# -50 >> F

mrk = int(input("Enter your Marks: \n"))
if mrk>=90:
    print("Excellent Grade")
elif mrk>=80 and mrk<90:
    print("A Grade")
elif mrk>=70 and mrk<80:
    print("B Grade")
elif mrk>=60 and mrk<70:
    print("C Grade")
elif mrk>=50 and mrk<60:
    print("D Grade")
else:
    print("Failed")


# Q7 ----> Write a program to find out wether a given post is talking about "Harry" or not
post = input('Enter a post to check if It is about "Harry" or not: \n')
if "Harry" in post or "harry" in post:
    print("Post is talking About Harry")
else:
    print("Post is not Talking about Harry")