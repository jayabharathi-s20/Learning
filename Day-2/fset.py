# frozenset
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

fs = frozenset({1, 2, 3})
cp = fs.copy()
print(fs)
print(cp)

a = frozenset({1, 2, 3, 4})
b = frozenset({3, 4, 5})
print(a.difference(b))
print(a - b)