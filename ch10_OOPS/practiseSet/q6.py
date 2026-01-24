# Can you change the self parameter inside the class to something else (say "harry"). Try changing "self" to slf or "harry" and see the effects

class car:

    def __init__(slf, carName, carNumber):
        slf.carName = carName
        slf.carName = carNumber

    # def color(self, color): # It should be slf not self the Instance object name should be same to passs it to all the functions else it gives the error
    #  <bound method car.color of <__main__.car object at 0x0000023A3D648C20>>
    #     print(f"Your {self.carName} has color {self.color}")

    def color(slf, color):
        print(f"Your {slf.carName} has color {color}")


Wheeler = car("M4 URK", "McLaren")

Wheeler.color("Black")



