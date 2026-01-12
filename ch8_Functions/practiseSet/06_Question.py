# Write a python funtion that converts inches to cms
def inchesToCm(inch):
    # 1 inch = 2.54cm
    cm = inch*2.54
    return cm
inch = int(input("Enter Inches to convert it to cms : "))
print(f"{inch} inches are {inchesToCm(inch)} cms")