# Write a program to find out the line number where python is present from ques 6
with open("log.txt","r") as f:
    content = f.readlines()
    # print(len(content))
    # print(content[4])
    line = 0
    condition = True
    while condition:
        if "python" in content[line]:
            print(f"Got python in Line: {line+1}")
            break
        if line == {len(content) - 1}:
            print("No Python Present")
            break
        line+=1

    