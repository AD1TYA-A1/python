# Here We can Feel that strings are immutable Every function on runnnig give a new string Which tells us that STRINGS ARE IMMUTABLE
# Original String Remains the Same
# Q1---> Python program to display a user entered name follwoed by Good Afternoon using input() function
# Sol1

name = input("Enter your Name: \n")
print("Good AfterNoon, ", name)

# Here is another way to print
print(f"Good Afternoon, {name}")
# f"Good Afternoon"-->I ahve converted this string into a fString which will allow me to access the value of a varibale using curly braces


# Q2-->Using name and date in the given template of letter
template = """\t\tDear <|Name|>
                You are Selected!!
                <|Date|>"""

print(
    template.replace("<|Name|>", "Aditya").replace("<|Date|>", "01/01/2026")
)  # Chaining of .replace()


# Q3--->Write a program to detect Double Space in a String
# See Double spaces here
str = "Hey I am  a string      s"
print(str)
print(str.find("  "))  # Returns Index of " "(The substring)

# Q4--->Replace thise double spaces with single Space
print(str.replace("  ", " "))
