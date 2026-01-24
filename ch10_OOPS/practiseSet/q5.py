# Write a class "train" which has methods to book a ticket, get status (no of seats) and get fare information of train runnning under Indian Railways.

# import random   I want to directly use ranint not random.ranint() soo using a new "from" keyword APPROCH!!
from random import randint


class train:

    def __init__(self, trainNo, fro , to):
        self.trainNo = trainNo
        self.fro = fro
        self.to = to


    def bookTicket(self):
        print(f"Ticket is booked for {self.trainNo}, from {self.fro} to {self.to}")

    def getStatus(self):
        print(f"Train no: {self.trainNo} is running on time")

    def getFare(self):
        print(
            f"Ticket fare for {self.trainNo}, from {self.fro} to {self.to} and the fare is {randint(222,5555)}"
        )


chennaiExpress = train("4AB23H","DEHRADUN", "Chennai")
chennaiExpress.bookTicket()
chennaiExpress.getFare()
chennaiExpress.getStatus()
