class animal:
    @staticmethod
    def eats():
        print("I belong to animal Class and I can eat food")

class drinks:
    @staticmethod
    def drinks():
        print("I can drink")


class dog(animal,drinks):
    @staticmethod
    def barks():
        print("I belong to dog class and I can Bark!!!")





# a = animal()
# a.breed -----> Cannot access breeed


a = dog()
a.drinks()
a.eats()
a.barks()
