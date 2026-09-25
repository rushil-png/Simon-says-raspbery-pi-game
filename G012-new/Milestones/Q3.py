key = False

def box_door():
    b = input("Box[B] or Door[D] ")
    if b.upper() == "B":
        box();
    elif b.upper() == "D":
        door()

def box():
    print("Found a key inside the box")
    global key
    key = True
    box_door()

def door():
    if key == True:
        quiz()
    elif key == False:
        print("Cannot open door without a key")
        box_door()

def quiz():
    print()
    print("=====QUIZ TIME!=====")
    print()
    q1()

def q1():
    ans = None
    while(ans != "yellow"):
        temp = input("Q1) What is the 3rd colour of the rainbow? ")
        ans = temp.lower()
    q2()

def q2():
    ans = None
    while(ans != 1000):
        temp = input("Q2) How many years in a millennium? ")
        ans = int(temp)
    q3()
    
def q3():
    ans = None
    while(ans != 206):
        temp = input("Q3) How many bones in the adult human body? ")
        ans = int(temp)
    finish()

def finish():
    print()
    print("==========================================")
    print("=====YOU HAVE FINISHED THE ADVENTURE!=====")
    print("==========================================")

#start
print("=====WELCOME TO AN ADVENTURE!=====")
print()
box_door()
