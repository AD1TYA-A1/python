# We are going to write a program that genrates a random number and asks the user to guess it .

# If the player's guess is higher than the actual number, the program displays "Lower Number Please". Similarly if the user's guess is too low, the program prints "Higher Number Please". When user guesses the correct number, the program displays the number of guesses the player took to arive at the number


# Then The turn Shifts to the another person and the one who took the least amount of guesses WINS!!

# HINT: Use the random Module

import random


def rndm():
    # print("I am random function")
    num = random.randint(1, 100)
    return num


def addUser(userName, score):
    with open("user.txt", "r") as f:
        content = f.readlines()
        # print(len(content))
        length = len(content)
        for i in range(0, length):
            if userName in content[i]:
                OldScore = content[i].split(" ")
                if int(OldScore[1]) > score:
                    content[i] = f"{userName}: {score} \n"
                    with open("user.txt", "w") as f2:
                        f2.writelines(content)
                        break
                break

        else:
            with open("user.txt", "a") as f2:
                f2.write(f"{userName}: {score} \n")


userName = input("Enter your Name to Play: ")
score = 0
print("Computer have chosen a Number")
a = int(input("Guess a number: "))
rndm = rndm()
while a != rndm:
    if a > rndm:
        print("Lower Number Please!!")
        score+=1
    elif a < rndm:
        print("Higher Number Please!!")
        score+=1
    a = int(input())

print("Got That")
print(f"{userName} Score: {score}")

addUser(userName,score)
# addUser("Aditya", 10)
