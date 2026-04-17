import os
#Python File Open

f=open("new_file.txt")
print(f.read())
f.close()

#If its on diff location
# f = open("D:\\myfiles\welcome.txt")
# print(f.read())

with open("another_file.txt") as f:
  print(f.read())

with open("another_file.txt") as f:
  print(f.read(5))

with open("another_file.txt") as f:
  print(f.readline())
  print(f.readline())

with open("new_file.txt") as f:
  for x in f:
    print(x)


#Write to an Existing File

with open("another_file.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("another_file.txt") as f:
  print(f.read())


#Overwrite Existing Content

with open("new_file.txt", "w") as f:
  f.write("Now the file has more content in new_file!")

#open and read the file after the appending:
with open("new_file.txt") as f:
  print(f.read())



#create a new file if not exists
# f = open("myfile.txt", "x")

#Python Delete File
# os.remove("delete.txt")

#To delete a folder
# os.rmdir("delete_folder")

#Check if File exist:
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")


