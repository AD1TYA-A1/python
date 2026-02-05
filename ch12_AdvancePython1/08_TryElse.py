try:
    a = int(input("Hey Enter a number: "))
    print(a)
except Exception as e:
    print(e)
else:   # This Works when try block is fully Successfully Executed!!!
    print("Hey I am inside else block")