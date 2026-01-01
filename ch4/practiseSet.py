#   Q1---> Program to store seven fruits in a list enetered by user
fruits = []
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)
f1 = input("Enter Fruit: ")
fruits.append(f1)

print(fruits)


#   Q2---> Program to accept marks of 6 studdetns and arrange them in order
marks = []
f1 = int(input("Enter Marks: "))
marks.append(f1)
f1 = int(input("Enter Marks: "))
marks.append(f1)
f1 = int(input("Enter Marks: "))
marks.append(f1)
f1 = int(input("Enter Marks: "))
marks.append(f1)
f1 = int(input("Enter Marks: "))
marks.append(f1)
f1 = int(input("Enter Marks: "))
marks.append(f1)
marks.sort()
print(marks)

#   Q3---->Program to add all the integer values inside a list

l1 = [
    23,
    2,
    10,
]  # Only Integer If you Enter any other type of value inside this list It will Throw Error
print(sum(l1))

# Q4 ----> Count The number of '0' in Tuple
a = (1, 45, 23, 0, 4, 0, 90, 0, 1)
print(a.count(0))
