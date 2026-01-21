# Write a program to generate multiplication tables from 2 to 20  and write it to the different files.Place these files in a folder for a 13-year Old

def generateTable(n):
    table = ""
    for i in range(2,n+1):
        table=""
        for j in range(1,11):
            table+=f"{i} X {j} = {i*j} \n"
        with open(f"table/table_{i}.txt","w") as f:
            f.write(table)
                


generateTable(4)