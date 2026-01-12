# Write a python function to remove a given word form a list and strip it to same time
def rem(l,word):
    n=[]
    for item in l:
        if not(item==word):
            n.append(item.strip(word))
    return n

l = ["Aditya","Admin","Rohan","min"]

print(rem(l,"min"))