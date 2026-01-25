class animal:
    @staticmethod
    def eats():
        print("I belong to animal Class and I can eat food")

class dog(animal):
    @staticmethod
    def barks():
        print("I belong to dog class and I can Bark!!!")

# class siberianHusky(animal,dog):
#   class siberianHusky(animal,dog):
#     ...<2 lines>...
#             print("I am a Siberian Husky!!!")
# TypeError: Cannot create a consistent method resolution order (MRO) for bases animal, dog


class drinks:
    @staticmethod
    def drinks():
        print("I can drink")


class siberianHusky(dog,drinks):    # siberianHusky automatically extends "animal" class as "siberianHusky" extends "dog" and "dog" extends "animal"   
    @staticmethod
    def breed():
        print("I am a Siberian Husky!!!")


# a = animal()
# a.breed -----> Cannot access breeed


a = siberianHusky()
a.barks()
a.eats()
a.breed()
a.drinks()