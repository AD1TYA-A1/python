# Write a program to rename a file to "renamed_by_python.txt" NO USE OF OS MODULE
with open("hahaFile.txt") as f:
    content = f.read()
    with open("renamed_by_python.txt","w") as f1:
        f1.write(content)
