a = "10.2";
print(type(a));

a = float(a); #Converts the string a into float
print(type(a));


#Input function
a = input("Enter 1st Number  \n");  #This input takes value as String
b = input("Enter 2nd Number  \n");  #This is also takes the value as String
print("a is: ",a);
print("b is: ",b);

#Now converting it into int using Type Conversion

a = int(a);
b = int(b);

print("The sum is: ",a+b);  #And here inside print function it concatinate String If I do not type convert the strin into integer value using int(x) finction


z = 2;
print("z^12 is: ",z**12)