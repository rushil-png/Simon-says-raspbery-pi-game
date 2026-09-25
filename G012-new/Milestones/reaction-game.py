from gpiozero import LED, Button
from time import sleep, time
import random

blue = LED(21)
green = LED(16)
red = LED(12)
button = Button(7)

best_time = None
name = ""

print("Start")

while True:
    print("Ready...")
    
    num = random.randint(1,10)
    sleep(num)
    
    blue.on()
    print("Now!")
    
    start_time = time()
    
    button.wait_for_press()
    reaction_time = time() - start_time
    blue.off()
    
    print(f"You reacted in {reaction_time:.3f} seconds")
    
    if best_time is None or reaction_time < best_time:
        print("New record!")
        name = input("Please enter your name: ")
        print(f"You current best record is {reaction_time} by {name}")

        green.on()
        sleep(3)
        green.off()
        
        best_time = reaction_time
        
        
    else:
        print("Too Slow!")
        red.on()
        sleep(3)
        red.off()
    
    print(f"The current best record is {best_time} seconds by {name}")