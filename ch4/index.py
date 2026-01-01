# Lists in Python are like arrays but they can store multiple collection of value of different  data type value in a single Vaiable. We can acccess the data members using indexes

friends = ["Aditya", "Arun", 32, 33.87, False, "Anshul"]
print(friends[0])

# In Strings it will give you errors because STRINGS ARE IMMUTABLE
# We Know that Strings are IMMUTABLE but Lists are MUTABLE
friends[0] = "Admin"
print(friends[0])


# We can do other function like slicing and upper(),lower()-->But Unlike Strings these funtion will not return a new list Rather they will CHANGE THE LIST
print(friends[1:4])
friends.append(True)
print(friends[1:7])


l1 = [1, 56, 3, 45, 3, 90, 89.3, 0.3]
print("Typpe of l1 is :", type(l1))     #<class 'list'>
# l1.sort();
# l1.reverse();
# l1.insert(0,32);  #Insert 32 at index 0
# l1.pop(3)  # Pops out Value at 3rd Index
print(l1.pop(5))
print(l1)
