#Tuple
thistuple = ("apple", "banana", "cherry")
print(thistuple)

print(len(thistuple))

thistuple = ("apple",)
print(type(thistuple))

#NOT a tuple
# thistuple = ("apple")
print(type(thistuple))

#access tuples
thistuple = ("apple", "banana", "cherry")

print(thistuple[1])
print(thistuple[-1])

thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:5])
print(thistuple[-4:-1])

if "apple" in thistuple:
  print("Yes, 'apple' is in the fruits tuple")

#Unpack Tuples
fruits = ("apple", "banana", "cherry")

(green, yellow, red) = fruits

print(green)
print(yellow)
print(red)

(green, yellow, *red) = fruits

print(green)
print(yellow)
print(red)

(green, *tropic, red) = fruits

print(green)
print(tropic)
print(red)

#Join Tuples

tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)

fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

print(mytuple)

#Tuple Methods
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

x = thistuple.count(5)

print(x)


thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)

x = thistuple.index(8)

print(x)