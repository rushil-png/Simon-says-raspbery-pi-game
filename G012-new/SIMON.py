from gpiozero import Button, LED
from time import sleep
import random
from collections import defaultdict

# ----------------------------
# LED and Button setup
# ----------------------------
led_red = LED(17)
led_blue = LED(18)
led_green = LED(24)
led_yellow = LED(23)

button_red = Button(6)
button_blue = Button(5)
button_green = Button(19)
button_yellow = Button(13)

leds = [led_blue, led_red, led_yellow, led_green]
btns = [button_blue, button_red, button_yellow, button_green]

colour_names = ["Blue", "Red", "Yellow", "Green"]

start_delay = 0.8
end_delay = 0.3
delay_step = 0.07

LB_FILE = "Lb.txt"
max_entries = 20  # only keep top 20 scores

# ----------------------------
# Smart Random Generator
# ----------------------------
class SmartRandom:
    def __init__(self, max_gap=6):
        self.last_seen = {1: -1, 2: -1, 3: -1, 4: -1}
        self.transitions = defaultdict(float)
        self.sequence_length = 0
        self.max_gap = max_gap
        self.sequence = []

    def next(self):
        i = self.sequence_length + 1
        numbers = [1, 2, 3, 4]
        weights = []

        for n in numbers:
            w = 1.0
            if self.sequence:
                prev = self.sequence[-1]
                w /= (1 + self.transitions[(prev, n)])
            if self.sequence and self.sequence[-1] == n:
                w *= 0.5
            if len(self.sequence) >= 2 and self.sequence[-1] == self.sequence[-2] == n:
                w *= 0.1
            if len(self.sequence) >= 3 and self.sequence[-3] == self.sequence[-1] and self.sequence[-2] == n:
                w *= 0.3

            gap = i - self.last_seen[n]
            if gap > self.max_gap:
                w *= 5.0
            else:
                w *= (1 + gap * 0.1)

            weights.append(w)

        x = random.choices(numbers, weights=weights)[0]

        while len(self.sequence) >= 3 and self.sequence[-1] == self.sequence[-2] == self.sequence[-3] == x:
            x = random.choice(numbers)

        # Update memory
        self.sequence.append(x)
        self.last_seen[x] = i
        if len(self.sequence) >= 2:
            self.transitions[(self.sequence[-2], self.sequence[-1])] += 1
        for k in self.transitions:
            self.transitions[k] *= 0.98

        self.sequence_length += 1
        return x - 1  # Convert 1-4 to 0-3 for LEDs/buttons

# ----------------------------
# Helper Functions
# ----------------------------
def index_to_colour(i):
    return colour_names[i]

def get_lb_file(difficulty):
    return {1: "lbeasy.txt", 2: "lbmedium.txt", 3: "lbhard.txt"}.get(difficulty, "Lb.txt")

def start_game():
    for led in leds:
        led.on()
    sleep(1)
    for led in leds:
        led.off()

def display_sequence(sequence, delay):
    print("Start")
    for j in sequence:
        led = leds[j]
        led.on()
        print(index_to_colour(j))
        sleep(delay)
        led.off()
        sleep(0.25)

def press():
    while True:
        if button_blue.is_pressed:
            return 0
        if button_red.is_pressed:
            return 1
        if button_yellow.is_pressed:
            return 2
        if button_green.is_pressed:
            return 3
        sleep(0.01)

def player_sequence(sequence):
    print("Your Turn")
    for exp in sequence:
        pressed = press()
        print(index_to_colour(pressed))
        leds[pressed].on()
        sleep(0.3)
        leds[pressed].off()
        if pressed != exp:
            print("Wrong button!")
            return False
    return True

def menu():
    print("""Choose difficulty
1: Easy
2: Medium
3: Hard
""")
    difficulty = int(input("Enter your choice here : "))
    print(f"You chose: {difficulty}")
    return difficulty

def success_animation():
    for _ in range(2):
        for led in leds:
            led.on()
        sleep(0.2)
        for led in leds:
            led.off()
        sleep(0.2)

def load_leaderboard(difficulty):
    leaderboard = []
    LB_FILE = get_lb_file(difficulty)
    try:
        with open(LB_FILE, "r") as f:
            for line in f:
                name, score, level = line.strip().split(",")
                leaderboard.append((name, int(score), int(level)))
    except FileNotFoundError:
        pass
    return leaderboard

def save_leaderboard(leaderboard, difficulty):
    LB_FILE = get_lb_file(difficulty)
    with open(LB_FILE, "w") as f:
        for entry in leaderboard[:max_entries]:
            f.write(f"{entry[0]},{entry[1]},{entry[2]}\n")

def show_leaderboard(difficulty):
    leaderboard = load_leaderboard(difficulty)
    print("\n========== LEADERBOARD ==========\n")
    if not leaderboard:
        print("No scores yet!")
        return
    for i, (name, score, level) in enumerate(leaderboard[:max_entries], start=1):
        print(f"{i}. {name} - Score: {score}, Level: {level}")
    print("================================\n")

def update_leaderboard(name, score, level, difficulty):
    leaderboard = load_leaderboard(difficulty)
    leaderboard.append((name, score, level))
    leaderboard.sort(key=lambda x: (-x[1], -x[2]))
    save_leaderboard(leaderboard, difficulty)

def game_over(score, level, difficulty):
    print("Game over")
    print("Final Score:", score)
    print("Final Level:", level)

    # LED animation
    for _ in range(3):
        for led in leds:
            led.on()
            sleep(0.2)
            led.off()
        for led in reversed(leds):
            led.on()
            sleep(0.2)
            led.off()

    name = input("Enter Your name: ")
    update_leaderboard(name, score, level, difficulty)
    show_leaderboard(difficulty)
    print("Press any button to restart...")
    press()

# ----------------------------
# Main Function
# ----------------------------
def main():
    global sequence
    sequence = []
    score = 0
    level = 0

    difficulty = menu()
    start_game()
    current_delay = start_delay

    smart_gen = SmartRandom()  # Smart random generator

    while True:
        for _ in range(difficulty):
            r = smart_gen.next()
            sequence.append(r)

        level += 1
        print("Level:", level)
        print("Sequence:", [index_to_colour(i) for i in sequence])

        display_sequence(sequence, current_delay)
        current_delay = max(end_delay, current_delay - delay_step)

        if not player_sequence(sequence):
            game_over(score, level, difficulty)
            break

        success_animation()
        score += len(sequence)
        print("+", len(sequence), "points")
        print("Score:", score)

# ----------------------------
# Start Game Loop
# ----------------------------
if __name__ == "__main__":
    while True:
        main()