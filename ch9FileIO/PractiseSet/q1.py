# Write a program  to read the text from a given file "poem.txt" and find out whether it contains the word "Twinkle"
f = open("poems.txt")
data = f.read()
if "Twinkle" in data or "twinkle" in data:
    print("Twinkle is Present")
else:
    print("Twinkle is not Present")
# print(type(data))     <class 'str'>
