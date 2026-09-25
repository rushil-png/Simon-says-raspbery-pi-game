# Simon Game — Raspberry Pi + Web Version

A memory-based **Simon game** built with Python, supporting both a physical **Raspberry Pi GPIO version** and a **browser-based web version**.

The player must memorise a sequence of coloured LED flashes and reproduce the sequence using the corresponding buttons. Each successful round increases the sequence length and difficulty.

---

## 🎮 Features

* 🧠 Memory-based Simon gameplay
* 🔴🟢🔵🟡 Four-colour LED and button system
* 🍓 Raspberry Pi GPIO support
* 🌐 Browser-based web version
* 📈 Increasing sequence length each round
* ⚡ Dynamic difficulty with faster sequences
* 🎯 Score system based on sequence length
* ✨ Success animation for completed rounds
* 💥 Game-over animation
* 🔄 Restart functionality
* 🏆 Persistent leaderboard
* 🎲 Custom `SmartRandom` class designed to reduce repetitive or predictable sequences
* 🎚️ Easy, Medium and Hard difficulty levels

---

## 🕹️ How It Works

The game follows a simple loop:

```text
        ┌──────────────┐
        │ Start Game   │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Generate     │
        │ Sequence    │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Flash LEDs   │
        │ to show      │
        │ sequence     │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Player       │
        │ repeats      │
        │ sequence     │
        └──────┬───────┘
               ↓
          Correct?
          ↙       ↘
       YES         NO
        ↓           ↓
   Increase      Game Over
   difficulty       ↓
        ↓       Show Score
   New Round         ↓
        │       Leaderboard
        └───────────────
```

Each round adds another colour to the sequence. The player must reproduce the entire sequence in the correct order.

A mistake ends the game.

---

## 💻 Technical Overview

The project is written in **Python** and consists of two gameplay modes.

### GPIO Mode

The Raspberry Pi version uses:

* Python
* `gpiozero`
* LEDs connected to GPIO pins
* Physical buttons for player input

The Raspberry Pi controls the LEDs to display the sequence and monitors the buttons to detect the player's response.

### Web Mode

The web version uses **Flask** to provide a browser-based version of the game.

The browser communicates with the Python backend through HTTP endpoints, allowing the game to be played without Raspberry Pi hardware.

---

## 🧩 Project Components

The program is separated into several main components:

### Sequence Generation

Generates the colour sequence that the player must memorise.

### Input Handling

Reads player input from either:

* Physical GPIO buttons
* Web interface buttons

### Game Logic

Controls:

* Round progression
* Sequence checking
* Difficulty
* Timing
* Scoring
* Game-over conditions

### Leaderboard

Stores the highest scores so they can be displayed between game sessions.

### `SmartRandom`

A custom randomisation class used to generate sequences while reducing repetitive or predictable patterns.

---

# 🔌 Hardware Setup

## LEDs

| Colour    |    GPIO |
| --------- | ------: |
| 🔴 Red    | GPIO 17 |
| 🔵 Blue   | GPIO 18 |
| 🟢 Green  | GPIO 24 |
| 🟡 Yellow | GPIO 23 |

## Buttons

| Colour    |    GPIO |
| --------- | ------: |
| 🔴 Red    |  GPIO 6 |
| 🔵 Blue   |  GPIO 5 |
| 🟢 Green  | GPIO 19 |
| 🟡 Yellow | GPIO 13 |

> **Note:** Make sure the GPIO configuration in the code matches your physical wiring.

---

## 🖼️ Circuit Diagrams

### GPIO Layout

Created using **Microsoft Whiteboard**.

### Breadboard Layout

Created using **Circuit Canvas**.

Add your diagrams to the repository and link them here, for example:

```markdown
![GPIO Layout](images/gpio-layout.png)

![Breadboard Layout](images/breadboard-layout.png)
```

---

# ⚙️ Requirements

## Raspberry Pi Version

* Raspberry Pi
* Raspberry Pi OS
* Python 3.x
* `gpiozero`

Install `gpiozero` with:

```bash
pip3 install gpiozero
```

### Optional

* [Thonny](https://thonny.org/) — used during development and testing

---

## 🌐 Web Version

The web version requires:

* Python 3.x
* Flask

Install Flask with:

```bash
pip install flask
```

---

# 🚀 Running the Game

## Raspberry Pi / GPIO Mode

### 1. Connect the hardware

Connect the four LEDs and four buttons according to the GPIO configuration above.

### 2. Verify the GPIO pins

Make sure the physical wiring matches the pin configuration in the Python code.

### 3. Run the game

```bash
python3 SIMON.py
```

---

## 🌐 Web Mode

### 1. Install Flask

```bash
pip install flask
```

### 2. Start the server

```bash
python3 app.py
```

### 3. Open the game

Open your browser and visit:

```text
http://127.0.0.1:5000
```

The game can then be played through the web interface without requiring the physical Raspberry Pi hardware.

---

# 📡 Web API

The Flask backend provides several HTTP endpoints.

| Method | Endpoint        | Description                        |
| ------ | --------------- | ---------------------------------- |
| `POST` | `/start_game`   | Starts a new game                  |
| `POST` | `/press`        | Sends a player's colour input      |
| `GET`  | `/led_state`    | Returns LED states and game status |
| `GET`  | `/leaderboard`  | Retrieves leaderboard scores       |
| `POST` | `/submit_score` | Submits a player's score           |

### Example Request

Start a new game:

```http
POST /start_game
```

Send a button press:

```http
POST /press
```

Retrieve the current LED state:

```http
GET /led_state
```

---

# 🎯 Difficulty Levels

The game supports three difficulty levels:

| Difficulty | Description                    |
| ---------- | ------------------------------ |
| **Easy**   | Slower sequence playback       |
| **Medium** | Increased speed and difficulty |
| **Hard**   | Faster sequence playback       |

The difficulty increases as the player progresses through the game.

---

# 🏆 Scoring

The player's score is based on the length of the sequence successfully completed.

As the sequence gets longer, successfully completing a round provides a higher score.

The final score is displayed when the player makes a mistake and the game ends.

High scores can be stored in the persistent leaderboard.

---

# 🔄 Game Over & Restart

When the player enters an incorrect sequence:

1. The game stops.
2. A game-over animation is displayed.
3. The player's final score is calculated.
4. The score can be submitted to the leaderboard.
5. The player can restart the game.

In GPIO mode, the game can be restarted by pressing a button.

---

# 📁 Suggested Project Structure

```text
Simon-Game/
│
├── SIMON.py
├── app.py
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── images/
│   ├── gpio-layout.png
│   └── breadboard-layout.png
│
└── leaderboard/
    └── ...
```

*The exact structure may differ depending on how the project is organised.*

---

# 🛠️ Future Improvements

Potential improvements include:

* 🔊 Add sound effects for each colour
* 🎵 Add background music
* 💾 Improve leaderboard storage
* 👤 Add player names
* 📊 Add statistics such as highest level and average score
* 🎨 Improve the web UI
* 📱 Improve mobile browser support
* 🌍 Allow multiple players to compete online
* 🔐 Add user accounts and authentication
* 🧪 Add automated tests for the game logic

---

# 📚 Technologies Used

* **Python 3**
* **Raspberry Pi GPIO**
* **gpiozero**
* **Flask**
* **HTML / CSS / JavaScript**
* **HTTP API**
* **Microsoft Whiteboard**
* **Circuit Canvas**

---

## 👨‍💻 Project

This project demonstrates how the same game logic can be adapted for both **physical hardware** and a **web-based interface**, while keeping the core gameplay and scoring system consistent.
