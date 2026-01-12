# Write a recursive function to find the sum of finst "n" natural numbers
def sumofnNaturalNumber(n):
    sum = 0
    if n == 0:
        return sum
    else:
        sum = sum+n
        return sum+sumofnNaturalNumber(n-1)

sum = sumofnNaturalNumber(9)
print(sum)