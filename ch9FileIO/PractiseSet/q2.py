# The game() function let's a user play a game and return the score as Integer.
# You need to read a file "Hi-Score.txt" which is either blank or contains the previous Hi-Scores.
# You need to write a program to update the Hi-Score whenever the game() function breaks the high score

import random


def game():
    # Read high score with proper error handling
    try:
        file = open("HiScore.txt", "r")
        content = file.read().strip()
        file.close()
        HiScore = int(content) if content else 0
    except FileNotFoundError:
        HiScore = 0

    score = 0
    """
    0 for rock
    1 for paper
    2 for scissor
    """
    play = True

    dict = {
        0: "Rock",
        1: "Paper",
        2: "Scissor",
    }  # r-->ROCK  # p-->PAPER  # s-->SCISSOR

    while play:
        # Generate computer's choice for each round
        computer = random.randint(0, 2)
        
        print(
            """
            0 for rock
            1 for paper
            2 for scissor
            """
        )

        condition = True
        user = int(input("Enter your Choice \n"))
        if user == 0 or user == 1 or user == 2:
            condition = False

        while condition:
            user = int(input("Invalid Input \n"))
            if user == 0 or user == 1 or user == 2:
                break

        if user >= 0 and user <= 2:
            if user == computer:
                print(
                    f"""
                    User:{dict[user]}
                    Computer:{dict[computer]}
                    IT IS A DRAW!!
                    """
                )
                print(
                    """
                      Press "s" to play again
                      and 
                      Press "a" to exit
                      """
                )
                playAgain = input()
                if playAgain == "a":
                    break

            elif computer == 0 and user == 1:
                print(
                    f"""
                    User:{dict[1]}
                    Computer:{dict[0]}
                    YOU WON!!
                    """
                )
                score += 1

                if score > HiScore:
                    file = open("HiScore.txt", "w")
                    file.write(str(score))
                    file.close()
                    HiScore = score

                print(
                    """
                      Press "s" to play again
                      and 
                      Press "a" to exit
                      """
                )
                playAgain = input()
                if playAgain == "a":
                    break

            elif computer == 1 and user == 2:
                print(
                    f"""
                    User:{dict[2]}
                    Computer:{dict[1]}
                    YOU WON!!
                    """
                )
                score += 1

                if score > HiScore:
                    file = open("HiScore.txt", "w")
                    file.write(str(score))
                    file.close()
                    HiScore = score

                print(
                    """
                      Press "s" to play again
                      and 
                      Press "a" to exit
                      """
                )
                playAgain = input()
                if playAgain == "a":
                    break

            elif computer == 2 and user == 0:
                print(
                    f"""
                    User:{dict[0]}
                    Computer:{dict[2]}
                    YOU WON!!
                    """
                )
                score += 1

                if score > HiScore:
                    file = open("HiScore.txt", "w")
                    file.write(str(score))
                    file.close()
                    HiScore = score

                print(
                    """
                      Press "s" to play again
                      and 
                      Press "a" to exit
                      """
                )
                playAgain = input()
                if playAgain == "a":
                    break

            else:
                print(
                    f"""
                    User:{dict[user]}
                    Computer:{dict[computer]}
                    COMPUTER WON!!
                    """
                )
                score = 0
                print(
                    """
                      Press "s" to play again
                      and 
                      Press "a" to exit
                      """
                )
                playAgain = input()
                if playAgain == "a":
                    break


game()
