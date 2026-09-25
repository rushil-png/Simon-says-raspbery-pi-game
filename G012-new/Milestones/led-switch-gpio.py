from gpiozero import LED, Button

led = LED(12)
button = Button(20)

def on_press():
    print("Pressed")
    led.toggle()
    
button.when_pressed = on_press
