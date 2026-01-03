# Q1 ----> Write a program to Make dictionery of Hindi Words with there English Meaning. Provide the User with an option to look it up!!!

words = {
    "jao": "go",
    "aao": "come",
    "idhr": "here",
    "udhr": "there",
    "jagah": "palce",
    "billi": "cat",
}
word = input("Enter the Word you want to find the meaning of : ")
print(words[word])


# Q2 -----> Write a program to input 8 numbers from user and display all unique numbers (once)

set = set()
print("Enter 8 numbers")
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))
set.add(int(input("Enter Number : ")))

print(set)


# Q3 ----> Can we have a set with 18 as integer and "18" as string
s = {18,"18"}
print(s,type(s))  # {18, '18'} <class 'set'>

# Q4 ------> Getting the length of the following SET
st = set()
st.add(20)
st.add(20.0)
st.add("20")  # Find the length of the String
print(st, type(st))     # {20, '20'} <class 'set'>
print(len(st))      #  2

# Q5 -------> if s = {} soo what is S??
# A5---------> It is an Empty Dictionery

# Q6 -------> Create an Empty Dictionary. llow 4 friends to enter their favourite language as value and use key as their name.Assume that the names are Unique
d = {}
name = input("Enter Friend's Name :")
lang = input("Enter Language Name :")
d.update({name:lang})
name = input("Enter Friend's Name :")
lang = input("Enter Language Name :")
d.update({name:lang})
name = input("Enter Friend's Name :")
lang = input("Enter Language Name :")
d.update({name:lang})
name = input("Enter Friend's Name :")
lang = input("Enter Language Name :")
d.update({name:lang})
print(d)


# Q7 -----> If the name of two friends are same so then what will happen :
# A7 ------> It will Update that Key Value pair of the Friend (Here:Aditya)

d1 = {
    "Aditya" : "JavaScript",
    "Rohan" : "Python",
    "Aditya" : "Python",
    "Admin" : "C#"
}
print(d1)        # {'Aditya': 'Python', 'Rohan': 'Python', 'Admin': 'C#'}

# Q8 --------> If Languages of two people are same then what will Happen to the Program??
# A8 --------> The program will run smoothly. In a dictionary two keys can have same Values
d = {
    "Aditya" : "JavaScript",
    "Rohan" : "Python",
    "Harish" : "Python",
    "Admin" : "C#"
}
print(d)     #{'Aditya': 'JavaScript', 'Rohan': 'Python', 'Harish': 'Python', 'Admin': 'C#'}      


#Q9 --------> Can you Chnge the value of a list inside a Set??
s = {8,7,12,"Aditya",[1,2]}
# Sets arenot Indexed i.e, We cannot access data in a set using index

# print(s)      # ERROR : cannot use 'list' as a set element (unhashable type: 'list')