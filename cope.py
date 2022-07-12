import time 

print("L bozo you thought there would be smthn here lmaoooooo")
time.sleep(1)

for i in range(100000000000000):
    print(str(i) + " " + str(time.time()))
    with open("cope.txt", "a") as f:
        f.write(str(i) + " " + str(time.time()) + "\n")


