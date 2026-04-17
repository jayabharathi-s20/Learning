

#VARIABLES--CONTAINER TO STORE DATA OF ANY DATATYPES

data="hello"
print(data)

x=20
print(x)

#Many Values to Multiple Variables
a,b,c="lds",20,True
print(a)
print(b)
print(c)

#One Value to Multiple Variables
l=k=j="same word"
print(l)
print(k)
print(j)

#Unpack a Collection
fruits = ["apple", "banana", "cherry"]
l,j,k=fruits
print(l)
print(j)
print(k)


#Remember that variable names are case-sensitive
#Multi Words Variable Names
#Camel Case
myVariableName = "John"
#Pascal Case
MyVariableName = "John"
#Snake Case
my_variable_name = "John"
print(myVariableName)
print(MyVariableName)
print(MyVariableName)

#Python - Output Variables--In the print() function, you output multiple variables, separated by a comma:

word1 = "Python"
word2 = "is"
word3= "awesome"
print(word1, word2, word3)

word4 = "Python "
word5 = "is "
word6 = "awesome"
print(word4+ word5+ word6)

#Global keyword
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

# x = "awesome"

# def myfunc():
#   global x
#   x = "fantastic"

# myfunc()

# print("Python is " + x)







