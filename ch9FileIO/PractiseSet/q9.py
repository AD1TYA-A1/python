# Write a program to find out whether a file is identical and matches the content of another file


def checkIdenticalFiles(file1path, file2path):

    with open(file1path) as f:
        content = f.read()
        with open(file2path) as f:
            content1 = f.read()
            if content == content1:
                print("Identical Files!!")
            else:
                print("UnIdentical Files!!")

checkIdenticalFiles("this.txt","thisCopy.txt")
