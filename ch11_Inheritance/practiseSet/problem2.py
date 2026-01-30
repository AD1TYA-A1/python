# Create a class "Pets" from a class "Animals" and further create a class "Dog" form "Pets". Add a method "bark" to class "Dog" 

class animal:
    @staticmethod
    def eat():
        print("All Animals Eat")

class pets(animal):
    @staticmethod
    def Domestication():
        print("I am a pet I can be Domesticated")

class dog(pets):
    @staticmethod
    def bark():
        print("I am Dog and I bark")


husky = dog()
husky.eat()
husky.Domestication()
husky.bark()