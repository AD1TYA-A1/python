a = 89


def fun():
    # a = 3  # Local varibale for "fun" function  
    global a # This will change the a = 89 to a = 3
    a = 3
    print(a)


fun()
print(a)
