# Module name should not any special charectors Like underscores etc

def greet():
    print("Hello User!!!")

greet()

print(__name__)
# If I run "module.py" it will return "__main__"
# If I run this module from another file like I will run this "module.py" from "10_main.py" soo this time "__name__"===> will give "module" as output i.e, the name of the file 

if (__name__ == "__main__"):
    # We can do this when we want to do some specefic task in this file only we do not want our this piece of code to be imported into another file
    print("We are directly running this code")
else:
    print("We are running this code by importing this into a module")