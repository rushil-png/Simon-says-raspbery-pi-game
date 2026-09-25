## Simon Game (Raspberry Pi + Web Version) 

## Description

A memory-based Simon game implemented using Python and GPIO on Raspberry Pi.  
The player must repeat a sequence of LED flashes using buttons.  
The length of the sequence increases at each new level.
The project also includes a web version that allows the game to be played in a browser without requiring Raspberry Pi hardware.

## Technical Overview

The game uses a Raspberry Pi and GPIO to control LEDs and read button input from the user. It is implemented with Python to combine game logic with user interaction with the hardware. The program generates a sequence of colours displayed with the LEDs. The player has to memorise and reproduce the sequence using the corresponding buttons.

The program has components responsible for:
- Sequence generation
- Input handling
- Game logic
- Persistent leaderboard

A custom class SmartRandom is used to generate random sequences with reduced repetitive or predictable patterns.

The game supports two modes:
- GPIO mode (physical LEDs and buttons)
- Web mode (browser-based interface using Flask)

The web version communicates with the backend through HTTP endpoints such as /start_game, /press, and /led_state.

## Requirements

### Raspberry Pi (GPIO mode)

- Python 3.x
- Raspberry Pi OS
- gpiozero library

Optional:
- Thonny IDE (used for development and testing)

```bash
pip3 install gpiozero
```

### Web Mode Requirements

- Flask

Install with:
```bash
pip install flask
```

## Diagrams

- GPIO Layout – Microsoft Whiteboard  
- Breadboard Layout – Circuit Canvas  

## Features

- LED sequence is generated randomly
- Player uses buttons to repeat the sequence
- Adjustable difficulty levels (Easy / Medium / Hard) via keyboard input
- Increasing difficulty on new levels
- Dynamic speed (LED display becomes faster each round)
- Scoring system based on sequence length
- LED success animation for correct input
- Game over animation with final score display
- Restart functionality (press any button to play again)
- Leaderboard (top scores saved between runs)
- Web interface (playable without Raspberry Pi)


## How the Game Works

1. The game shows a sequence of LED flashes  
2. The player must repeat the same sequence using buttons  
3. Each round adds new elements to the sequence  
4. The game ends when the player makes a mistake  


## Scoring System

- Score increases based on the length of the sequence
- Longer sequences give higher rewards
- Final score is displayed at game over


## Hardware Setup

- 4 LEDs:
  - Red → GPIO 17
  - Blue → GPIO 18
  - Green → GPIO 24
  - Yellow → GPIO 23

- 4 Buttons:
  - Red → GPIO 6
  - Blue → GPIO 5
  - Green → GPIO 19
  - Yellow → GPIO 13


## How to Run

### Raspberry Pi (GPIO mode)

1. Connect the Raspberry Pi with all components correctly wired
2. Ensure the GPIO pins match the configuration in the code
3. Run the program:


```bash
python3 SIMON.py
```

### Web Version

Run the Flask server:

python3 app.py

Then open in browser:
http://127.0.0.1:5000


## Web API Endpoints

- POST /start_game → start a new game
- POST /press → send user input
- GET /led_state → get LED states and game status
- GET /leaderboard → retrieve leaderboard
- POST /submit_score → submit score


## Contributors

- Giulio Tomaselli
- Orlando Caka
- Rushil Shah
- Moses Mendes