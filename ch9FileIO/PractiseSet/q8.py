# Write a program to make a copy of a text file "this.txt"
with open("this.txt") as f:
    content = f.read()
    with open("thisCopy.txt","w") as f1:
        f1.write(content)