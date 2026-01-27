#  A way to access a class inside inside a function or a method 
class human:
    gender = "male"
    @classmethod  # A decorator that makes a Function to allow use class Attributes instead of Instance Attribute
    # Altogether this decorator gives preferance more to class Attributes not to Instance Attribute 
    # We use cls instead of self  SYNTACTIC SUGAR. You can leave it as self Also
    def category(cls):
        # print(f"Category as a class Attribute is : {cls.gender} \n and name is {cls.name}")
        # ERROR:   print(f"Category as a class Attribute is : {cls.gender} \n and name is {cls.name}")
        # AttributeError: type object 'human' has no attribute 'name'

        # THIS GIVES ERROR BECAUSE UPON USING THIS DECORATOR @CLASSMETHOD IT GIVES NO VALUE TO INSTANCE ONLY TO CLASS ATRIBUTE 
        # EVEN IF YOU ADD A OBJECT ATTRIBUTE AND TRY TO ACCESS {HERRE cls.name} it throws error BECAUSE THIS CATEGIRY() FUNCTION HAVE TO ACCESSIBLITY TO MY INSTANCE 


        print(f"Category as a class Attribute is : {cls.gender} ")



a = human()
a.gender = "female"
a.name = "Admin"
a.category()