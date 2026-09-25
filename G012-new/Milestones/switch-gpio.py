from gpiozero import Button

button = Button(17)

def on_press():
    print("Pressed")

button.when_pressed = on_press
