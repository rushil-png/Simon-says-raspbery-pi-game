from gpiozero import LED, Button

led = LED(13)
button = Button(21)

def on_press():
    print("Pressed")
    led.toggle()
    
button.when_pressed = on_press
