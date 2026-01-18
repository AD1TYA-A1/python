# To avoid f.close()
with open("file.txt") as f:
    print(f.read())

# No need to close the file it is closed by default