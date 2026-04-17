a="python"
print(a)

b='''
jdfdkfd
fdsfd
dfsfdfsd
'''
print(b)

word="python"
print(word[2])
print(len(word))
for c in word:
    print(c)

d="python programming"
print("python" in d)
print("python" not in d)

#Slicing
print(d[:6])
print(d[7:])
print(d[::-1])
print(d[-4:])

#Str modifications
e=" hello,world"
print(e.upper())
print(e.lower())
print(e.strip())
print(e.replace("h","H"))
print(e.split(","))

#Concatenation
f="hello"
g="world"
print(f+g)
print(f,g)

#format strings
price=12
print(f"price - {price}")
print(f"price - {price:.2f}")



