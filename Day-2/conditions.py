#EXAMPLE-1

# balance=5000

# while True:
#     print("\n1. Check Balance")
#     print("2. Deposit")
#     print("3. Withdraw")
#     print("4. Exit")

#     choice=int(input("Enter your choices: "))

#     if choice==1:
#         print(f"Your balance is {balance}")
#     elif choice==2:
#         amount=int(input("Enter amount : "))
#         balance+=amount
#         print("Deposited")
#         print(f"you balance is {balance}")
#     elif choice==3:
#         withdraw_amount=int(input("Enter amount : "))
#         if withdraw_amount >balance:
#             print("Insufficient balance")
#         else:
#             balance-=withdraw_amount
#             print(f"Amount withdrawn ,you balance is {balance}")
#     elif choice ==4:
#         print("Exit")
#     else:
#         print("invalid choice")

#EXAMPLE-2

# names=["jaya","suba","ini"]
# count=0
# for name in names:
#     if "a" in name:
#         count+=1
# print(count)

#EXAMPLE-3

# for i in range(10):
#     if i==2:
#         continue
#     print(i)

#EXAMPLE-4

# for i in range(10):
#     if i==5:
#         break
#     print(i)

#EXAMPLE-5

fruits=["apple","kiwi","lll"]
vowels="aeiou"
word_count=0
for fruit in fruits:
    for i in fruit:
        if i in vowels:
            word_count+=1
            break
print(word_count)


i=1
while i<=10:
    print(i)
    i+=1




