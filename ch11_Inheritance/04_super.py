class animal:
    def __init__(self):
        print("I am a constructor of animal Class")

    @staticmethod
    def eats():
        print("I belong to animal Class and I can eat food")


class dog(animal):
    def __init__(self):
        print("I am a constructor of dog Class")

    @staticmethod
    def barks():
        print("I belong to dog class and I can Bark!!!")


class siberianHusky(
    dog
):  # siberianHusky automatically extends "animal" class as "siberianHusky" extends "dog" and "dog" extends "animal"

    # 🔍 What’s going wrong?

    # super() can ONLY be used inside a method, usually inside __init__().

    def __init__(self):
        print("I am a constructor of SiberianHusky Class")
        super().__init__()  # CALLS THE CONSTRUCTOR OF ITS PARENT CLASS

    @staticmethod
    def breed():
        print("I am a Siberian Husky!!!")


a = siberianHusky()  # I am a constructor of SiberianHusky Class
# b = dog()   # I am a constructor of dog Class
# c = animal() # I am a constructor of animal Class


#   NOW IN ORDER TO CALL CONSTRUCTOR OR ANY OTHER FUNCTION OF ANY CLASSS WE USE "SUPER()"
