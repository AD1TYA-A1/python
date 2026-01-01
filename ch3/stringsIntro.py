#  Strings in pyhton can be made using 3 conventions

str1 = "Aditya"
# STRINGS ARE IMMUTABLE (in str1 string you cannot change any letter now you have to create a new string to change any letter say Aditya--->Adityaa )
str2 = "Aditya"
str3 = """Aditya is a Gentleman  
with Uncountable capablities to Grow 
and
Never Stop"""
# It prints the it exactly

print("str1:", str1, "\n", "str2:", str2, "\n", "str3:", str3)

print("Length of str3: ", len(str3))
# 76

# ACCESSING THE KEYS USING INDEX
print(str1[-1])
# a
print(str1[-2])
# y
print(str1[-5])
# d
print(str1[0])
# A
print(str1[1])
# d
print(str1[3])
# t

# ShortString Concept (A type of slicing)
shortStr1 = str1[0:4]
# Gives data members from index 0 to 4 (EXCLUDING 4)
print(shortStr1)
# Adit

# NEGATIVE SLICING
#  0   1   2   3   4   5      -->Positive/Normal Indexing
#  A   d   i   t   y   a
# -6  -5  -4  -3  -2  -1      -->Negative Indexes
negShortStr2 = str1[-3:-1]
print(negShortStr2)
# ty


# Slicing With Skip Value
a = "0123456789"
print(a[2:6:3])
# Resolving first 2:5 soo from 2ndIndex to 5th (Exckuding 5) = "2345"
# Now that remaning 2 will move like
# "2   3   4   5"     (2 mtlb Print in gap of 2)
# 2 then 2 gap (no 3,4)
# now points to 4 now 4 will be print
# it moves ahead skips 5 but string is now over therefore
# Final Output:"25"
print(a[:5])  # "01234"
print(a[0:])  # "0123456789


# Functions in String
print(len("Aditya"))  # 6
print(str1.endswith("ya"))  # TRUE
print(str1.endswith("yaaa"))  # False

print(str1.startswith("A"))
# True
print(str1.startswith("a"))
# False
# CaseSensitive
# There are soo many Other functions like .upper(),.lower() , .capitalize()==Capitalizes the first keyword of the string , .find() ==>Returns the index of the word , .replace()


# Escape Sequences
# Like \n, \t gives a tab space
