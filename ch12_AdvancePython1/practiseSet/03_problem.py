# Write list Comprehention to print a list which contains the multiplication table of entered number

num = int(input("Enter a Number: "))

table = [num*i for i in range(1,11)]
# for i in range(1,11):
#     table.append([i*j for j in l])


# print(len(table)) === 10
for i in range(len(table)):
    print(f"{num}X{i+1} = {(table[i])}")