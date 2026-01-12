# Write a Program using fuction to convert Celsius to Fahrenheit
def celToFahren(celsius):
    f = ((celsius * 1.8) + 32)
    return f

c = int(input("Enter Celcius to convert it to Fahrenheit: "))
f = celToFahren(c)
print(f"{c}°Celsius is equal to {int(f)}F")  