"""
0 for rock
1 for paper
2 for scissor
"""

import random

computer = int(random.random() * 10)

while computer != 100:
    computer = int(random.random() * 10)
    if computer == 0 or computer == 1 or computer == 2:
        break


dict = {0: "Rock", 1: "Paper", 2: "Scissor"}  # r-->ROCK  # p-->PAPER  # s-->SCISSOR

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
        print(f"""
            User:{dict[user]}
            Computer:{dict[computer]}
            IT IS A DRAW!!
""")
    elif computer == 0 and user == 1:
        print(
            f"""
                User:{dict[1]}
                Computer:{dict[0]}
                YOU WON!!

              """
        )
    elif computer == 1 and user == 2:
        print(
            f"""
            User:{dict[2]}
            Computer:{dict[1]}
            YOU WON!!
        """
        )
    elif computer == 2 and user == 0:
        print(
            f"""
            User:{dict[0]}
            Computer:{dict[2]}
            YOU WON!!
        """
        )
    else:
        print(f"""
         User:{dict[user]}
            Computer:{dict[computer]}
            COMPUTER WON!!
""")
