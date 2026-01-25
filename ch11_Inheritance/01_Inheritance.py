class animal:
    @staticmethod
    def eats():
        print("I belong to animal Class and I can eat food")

class dog(animal):
    @staticmethod
    def barks():
        print("I am dog and I can Bark")


bullDog = dog()
bullDog.eats()
bullDog.barks()