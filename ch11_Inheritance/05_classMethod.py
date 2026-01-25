class human:
    gender = "male"
    
    def category(self):
        print(f"Category as a class Attribute is : {self.gender}")


a = human()
a.gender = "female"
a.category()