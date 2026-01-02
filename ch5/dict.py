# Dictionery in Python Programming

marks = {"Aditya": 100, "Admin": 99, "Sohit": 67, "Rohan": 23, 5: "Admin"}
d = {}; #Empty Dictionery
print(type(marks))  # <class 'dict'>
print(marks)

# WHY WE NEED DICTIONERY???
# Beacuse Searching takes O(1) computational complxity
print(marks["Aditya"])
# It will print it in O(1)

# If I will have 100+ marks and names soo The LOOKUP in python dictionery is VERY FAST (O(1))


#   Methods in Dictionery
print(marks.items())
print(marks.keys())
print(marks.values())
print(marks.update({5: "Agent", "Radhika": 100}))  # Dictionery Are MUTABLE

print(marks)

print(marks.get("Aditya"))
print(marks["Aditya"])
#   What is the difference
print(marks.get("Aditya2"))  # Gives NONE as there is no value
print(marks["Aditya2"])  # Returns an Error and terminate program

