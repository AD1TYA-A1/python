# Store the multiplication tables generated in problem 3 in Tables.txt

num = int(input("Enter a Number: "))

table = [num*i for i in range(1,11)]
# for i in range(1,11):
#     table.append([i*j for j in l])


# print(len(table)) === 10
# for i in range(len(table)):
#     print(f"{num}X{i+1} = {(table[i])}")

with open("table.txt", "a") as f1:
    for i in range(len(table)):
        f1.write(f"{num} X {i+1} = {(table[i])}"+"\n")

    f1.write("\n \n ")
