# Write a program to print the third, fifth and seventh element form the list using enumerate function.
l = [12, 23, 34, 56, 67, 78, 89, 90]

for index, item in enumerate(l):
    if index > 1:
        if index % 2 == 0:  # They are talkig about elemt not index 3rd element is at 2ns index
            print(f"Item in Index {index} is {item}")
