thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["brand"])
print(len(thisdict))
print(type(thisdict))

thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)

#Access Dictionary Items

car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}

x = car.keys()

print(x) #before the change

car["color"] = "white"

print(x)

x = car.values()

print(x) #before the change

car["year"] = 2020

print(x) #after the change

x = car.items()

print(x) #before the change

car["year"] = 2020

print(x) #after the change

#Change Dictionary Items

thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2022})
print(thisdict)

#Remove Dictionary Items
thisdict.pop("model")
print(thisdict)

thisdict.popitem()
print(thisdict)

# del thisdict
# print(thisdict)

# thisdict.clear()
# print(thisdict)

#Copy Dictionaries
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
print(mydict)

#nested dict
child1 = {
  "name" : "Emil",
  "year" : 2004
}
child2 = {
  "name" : "Tobias",
  "year" : 2007
}
child3 = {
  "name" : "Linus",
  "year" : 2011
}

myfamily = {
  "child1" : child1,
  "child2" : child2,
  "child3" : child3
}

print(myfamily["child2"]["name"])
