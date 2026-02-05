# try:
#     a = int(input("Hey Enter a number: "))
#     print(a)
# except Exception as e:
#     print(e)
# finally:
#     print("Hey I am inside finally block")


# OK SOO FINALLY IS RUNNING EVERY TIME EVEN WHEN TRY BLOCK RUNS OR FINALLY BLOCK RUNS SOOOOOO WHY WE USE FINALLY WHY CANNOT WE JUST DO LIKKE THIS:
# try:
#     a = int(input("Hey Enter a number: "))
#     print(a)
# except Exception as e:
#     print(e)
# # finally:     #    NO FINALLY BUT STIILLS WORKS FOR BOTH VALID AND INVALID ARGS
# print("Hey I am inside finally block")


# IMP========IMP     IMP========IMP  IMP========IMP  IMP========IMP  IMP========IMP  
# FINALLY IS VERY HELPFUL IN FUNCTIONS LIKE EVEN IF FUNCTION RETURNED A VALUE AT STARTING STILL FINALLY WILL BE WORKING

def main():
    try:
        a = int(input("Hey Enter a number: "))
        print(a)
        return
    except Exception as e:
        print(e)
        return
    finally:    # This block executes even when the function have returned 
        a = 10
        b= 100
        print(f"The sum of {a} and {b} is {a+b}")
        print("Hey I am inside finally block")


main()

# Finally will still work even when the function ignores the rest statment inside after return 