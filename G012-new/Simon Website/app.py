# ===== GPIO SAFE IMPORT =====
GPIO_AVAILABLE = False

try:
    from gpiozero import Button, LED
    GPIO_AVAILABLE = True
except Exception as e:
    print(f"GPIO not available: {e}")
    GPIO_AVAILABLE = False

from flask import Flask, request, jsonify, render_template
from time import sleep
import threading
import random
import os

app = Flask(__name__, template_folder="frontend")

# ===== GPIO SETUP =====
if GPIO_AVAILABLE:
    led_red = LED(17)
    led_blue = LED(18)
    led_green = LED(24)
    led_yellow = LED(23)

    button_red = Button(6)
    button_blue = Button(5)
    button_green = Button(19)
    button_yellow = Button(13)
else:
    led_red = led_blue = led_green = led_yellow = None
    button_red = button_blue = button_green = button_yellow = None

# Game Settings
start_delay = 0.8
end_delay = 0.3
delay_step = 0.07
sequence = []
score = 0

btns = [button_blue, button_red, button_yellow, button_green]
leds = [led_blue, led_red, led_yellow, led_green]
colour_names = ["Blue", "Red", "Yellow", "Green"]

max_entries = 20

led_state = [False, False, False, False]
game_status = {"running": False, "message": "ready"}
pending_game_over = {"waiting": False, "score": 0, "level": 0, "difficulty": 1}

last_web_input = None
waiting_for_input = False

# ===== HELPERS =====
def get_lb_file(difficulty):
    if difficulty == 1:
        return "lbeasy.txt"
    if difficulty == 2:
        return "lbmedium.txt"
    if difficulty == 3:
        return "lbhard.txt"


def index_to_colour(i):
    return colour_names[i]


def set_led(index, on):
    led_state[index] = on

    if leds[index] is not None:
        if on:
            leds[index].on()
        else:
            leds[index].off()


# ===== GAME =====

def start_game():
    for i in range(4):
        set_led(i, True)
    sleep(1)
    for i in range(4):
        set_led(i, False)


def display_sequence(delay):
    for j in sequence:
        set_led(j, True)
        print(index_to_colour(j))
        sleep(delay)
        set_led(j, False)
        sleep(0.25)


# ===== UPDATED FUNCTION =====
def press():
    global last_web_input, waiting_for_input

    # WEB MODE
    if not GPIO_AVAILABLE:
        waiting_for_input = True 

        while last_web_input is None:
            sleep(0.01)

        value = last_web_input
        last_web_input = None
        waiting_for_input = False

        print("Web input:", index_to_colour(value))
        return value

    # GPIO MODE 
    while True:
        if button_blue.is_pressed:
            while button_blue.is_pressed:
                sleep(0.01)
            return 0
        if button_red.is_pressed:
            while button_red.is_pressed:
                sleep(0.01)
            return 1
        if button_yellow.is_pressed:
            while button_yellow.is_pressed:
                sleep(0.01)
            return 2
        if button_green.is_pressed:
            while button_green.is_pressed:
                sleep(0.01)
            return 3
        sleep(0.01)

def player_sequence():
    for exp in sequence:
        pressed = press()
        print(index_to_colour(pressed))

        set_led(pressed, True)
        sleep(0.3)
        set_led(pressed, False)

        if pressed != exp:
            print("Wrong button!")
            game_status["message"] = "wrong button!"

            for _ in range(5):
                set_led(exp, True)
                sleep(0.1)
                set_led(exp, False)
                sleep(0.1)

            return False
    return True


def success_animation():
    for _ in range(2):
        for i in range(4):
            set_led(i, True)
        sleep(0.2)
        for i in range(4):
            set_led(i, False)
        sleep(0.2)


def game_over_animation():
    sleep(1)
    delays = [0.15, 0.13, 0.11, 0.09, 0.07, 0.05]

    for delay in delays:
        for i in range(4):
            set_led(i, True)
            if i > 0:
                set_led(i - 1, False)
            sleep(delay)
        set_led(3, False)


# ===== LEADERBOARD =====

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


def update_leaderboard(name, score, level, difficulty):
    leaderboard = load_leaderboard(difficulty)
    leaderboard.append((name, score, level))
    leaderboard.sort(key=lambda x: (-x[1], -x[2]))
    save_leaderboard(leaderboard, difficulty)


def game_over(score, level, difficulty):
    global pending_game_over

    game_status["running"] = False
    game_status["message"] = "game over"

    game_over_animation()

    pending_game_over["waiting"] = True
    pending_game_over["score"] = score
    pending_game_over["level"] = level
    pending_game_over["difficulty"] = difficulty


def main(difficulty=1):
    global sequence, score

    sequence.clear()
    score = 0
    level = 0

    start_game()
    current_delay = start_delay

    sleep(1)

    game_status["running"] = True
    game_status["message"] = "watch sequence"

    while True:
        for _ in range(difficulty):
            sequence.append(random.randint(0, 3))

        level += 1

        display_sequence(current_delay)
        game_status["message"] = "your turn"      
        current_delay = max(end_delay, current_delay - delay_step)

        if not player_sequence():
            game_over(score, level, difficulty)
            break

        success_animation()
        score += len(sequence)


# ===== FLASK =====

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game_web():
    difficulty = request.form.get('difficulty', 1, type=int)
    threading.Thread(target=main, args=(difficulty,)).start()
    return jsonify({'status': 'Game started'})


@app.route('/leaderboard')
def leaderboard():
    difficulty = request.args.get('difficulty', 1, type=int)
    return jsonify(load_leaderboard(difficulty))


@app.route('/submit_score', methods=['POST'])
def submit_score():
    name = request.form.get('name', 'Anonymous')

    if pending_game_over["waiting"]:
        update_leaderboard(
            name,
            pending_game_over["score"],
            pending_game_over["level"],
            pending_game_over["difficulty"]
        )
        pending_game_over["waiting"] = False

    return jsonify({"status": "saved"})


# ===== NEW ROUTE =====
@app.route('/press', methods=['POST'])
def web_press():
    global last_web_input, waiting_for_input

    if not waiting_for_input:
        return jsonify({"status": "ignored"})

    value = request.form.get('value', type=int)
    last_web_input = value
    return jsonify({"status": "ok"})


@app.route('/led_state')
def get_led_state():
    return jsonify({
        "leds": led_state,
        "running": game_status["running"],
        "message": game_status["message"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
