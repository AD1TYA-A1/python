#  A way to access a class inside inside a function or a method 


# HERE WE USED ABSTRACTION AND ENCAPSULATION
# ----> ABSTRACTION : YOU HAVE NO CLUE , WE HAVE HIDDEN THE IMPLEMENTATION DETAILS. Such as here we took the last name and first name by own without letting the user know 
# ----> ENCAPSULATION : WE HAVE WRAPPED ALL THE WORK IN A SINGLE UNIT THAT IS CLASS "human" HERE. The class contained all of out methods decorators and all the other stuffs

class human:
    gender = "male"
    @property
    def name(self):
        return f"{self.fname}\n{self.lname}"
    # "aname" is instance property  
    
    @name.setter
    def name(self,value):
        self.fname = value.split(" ")[0]
        self.lname = value.split(" ")[1]

    @property
    def mobile(self):
        return f"{self.countryCode}\n{self._mobile}"
    
    
    @mobile.setter
    def mobile(self,value):
        self.countryCode = value.split(" ")[0]
        self._mobile = value.split(" ")[1]

    @classmethod  
    def category(cls):
        print(f"Category as a class Attribute is : {cls.gender} ")



a = human()
a.gender = "female"
a.name = "Admin Joe" # I want to give convinience to my user for you write full name and we will extract you first and last Name from here

a.mobile = "+91 8449697670"

print(a.mobile)