f = open("file.txt")  # mode = "r" = read by default
# f = open("file.txt","w")    # mode = "w" = Write into file
data = f.read()

print(data)
f.close()

addData = "\n Yes you are absolutely Best"
f = open("file.txt", "w")
f.write(addData) # --> Replaces the entire file data to addData
# print() # output --> 29

f.close()


f = open("fileWithMultipleLine.txt")
lines = f.readlines()  # Returns a pyhton List

# readLine is a function to get Only One Line

print(lines,type(lines))
f.close()

# To let file have old Data and add more data we can do it by append()
f = open("file.txt","a")
add = "\n Append me "
f.write(add)
f.write(add)
f.write(add)
f.close()

