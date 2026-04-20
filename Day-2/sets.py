thisset = {"apple", "banana", "cherry", "apple"}

print(thisset)

# True and 1 is considered the same value:
# False and 0 is considered the same value:

thisset = {"apple", "banana", "cherry", True, 1, 2}
print(len(thisset))
print(thisset)
print(type(thisset))

#Access Set Items
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

print("banana" in thisset)

#Add Set Items
thisset.add("orange")

print(thisset)

tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset)

mylist = ["kiwi", "orange"]

thisset.update(mylist)

print(thisset)

#Remove Set Items
#Note: If the item to remove does not exist, remove() will raise an error.
# thisset.remove("grape")

# print(thisset)
thisset.discard("banana")

print(thisset)

# x = thisset.pop()

# print(x)

# print(thisset)

# thisset.clear()

# print(thisset)

#Join Sets
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1 | set2
print(set3)

set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}

myset = set1.union(set2, set3, set4)
print(myset)

myset = set1 | set2 | set3 |set4
print(myset)

set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}

set1.update(set2)
print(set1)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.intersection(set2)
print(set3)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1 & set2
print(set3)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set1.intersection_update(set2)

print(set1)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.difference(set2)

print(set3)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1 - set2
print(set3)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set1.difference_update(set2)

print(set1)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.symmetric_difference(set2)

print(set3)

set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set1.symmetric_difference_update(set2)

print(set1)

