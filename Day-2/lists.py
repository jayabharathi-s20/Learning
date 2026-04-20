lists=["abc",23,"ljk",True]

print(type(lists))
print(len(lists))

a=list(("abc",12,True,("hjg",2.5)))
print(type(a))

#ACCESSING LIST ITEMS
b=[23,True,"jaya","klj"]
print(b[1])
print(b[:1])
print(b[::-1])

thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[-4:-1])

#Change List Items
thislist[1] = "blackcurrant"
print(thislist)

thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)

thislist.insert(2, "watermelon")
print(thislist)

#Add List Items
thislist.append("orange")
print(thislist)

thislist.insert(1, "orange")
print(thislist)

tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)

#Remove List Items

thislist.remove("orange")
print(thislist)

thislist.pop(1)
print(thislist)

thislist.pop()
print(thislist)

del thislist[0]
print(thislist)
del thislist


#Loop Lists
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)


for i in range(len(thislist)):
  print(thislist[i])

i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

#List Comprehension
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = [x for x in fruits if "a" in x]

print(newlist)

#Sort Lists

fruits.sort()
print(fruits)

fruits.sort(reverse = True)
print(fruits)

#Copy Lists
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)



