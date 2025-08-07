
---

# Tank Battle Game

## Introduction

This is a terminal-based tank battle game written in C++. It supports multiple modes including Player vs Player (PVP), Player vs AI (PVE), and automatic demonstration mode (DEMO). Players can control tanks to move, fire, and fight on a shrinking map until one tank's life point is deducted to zero.

## Compilation

To make the compilation easier, the project uses a `Makefile`. You can simply enter:

```bash
make
```

This will compile all source files and generate the executable named `main`.

## File Structure

This program uses Layered Architecture Pattern and Object-Oriented Paradigm. The structure is shown as follows:

### Presentation Layer:
* `main.cpp`: Program entry point, responsible for initialization
* `Renderer.h / Renderer.cpp`: Game rendering, displays tanks, bullets, and map in the terminal

### Application Layer:
* `game.h / game.cpp`: Core game logic, including turn control, input handling, map shrinking, and save/load/log functionalities
* `AI.h / AI.cpp`: Basic logic for computer controlled tank, including chasing, escaping, and avoiding bullets

### Domain Layer:
* `map.h / map.cpp`: Map class, responsible for map size and shrinking logic
* `tank.h / tank.cpp`: Tank class, handling tank position, direction, life points, movement, and shooting
* `bullet.h / bullet.cpp`: Bullet behavior, including movement and collision detection
* `common.h`: Direction, game mode and color definition

### Data Layer:
`Game::save()`, `Game::load()`, and `Game::log()` defined in `game.cpp`, responsible for saving and load game state, and logging game process to a file.

## Class Overview

This program applies Object-Oriented Programming, here's an overview of classes defined in the program:
| Class      | Responsibility                                                            |
| ---------- | ------------------------------------------------------------------------- |
| `Tank`     | Represents a tank's position, direction, health, cooldown, etc.           |
| `Bullet`   | Represents a moving projectile with direction and explosion status.       |
| `Map`      | Tracks the game boundaries and shrinking logic.                           |
| `Renderer` | Draws the game state to console.                                          |
| `Game`     | Coordinates turns, movement, bullet management, shrinking, victory logic. |
| `AI`       | Provides movement decision based on bullet positions, health, etc.        |


## How to Play

### Start the Game

Enter 
```bash
./main -l <log_file> -m <mode> -p <life point>
```
 `log_file` is the file to which you wish to log the game process. For `mode`, you can choose from `PVP`, `PVE`, and `DEMO`. `life point` is the initial life point for both tanks, which should be an integer.

  You can also simply enter 
  
  ```bash
  ./main
  ```
  
  with no arguments, and the game will adopt the default configuration, as shown below:
 ```
Default configuration:
- Log file: tankwar.log
- Mode: PVP
- Life points: 5
 ``` 

 Enter the command `./main -h` to check guidance in terminal. 




### Controls

Each turn, the player is prompted to input a command:

* `move f`: Move forward
* `move l`: Turn left
* `move r`: Turn right
* `dir`: Show tank direction in the map
* `lab`: Show tank label instead of direction
* `save <filename>`: Save the game state
* `load <filename>`: Load a saved game

### Features

* Tanks will shoot bullets after the fire cooldown becomes 0
* Bullet moves in the direction of the tank when fired and can hit tanks
* When tanks hit each other, the tank with higher life point will win
* The map shrinks every 16 turns — tank outside takes damage for 1 point each turn
* Game state can be saved and loaded
* A log file (`tankwar.log`) records information each turn

### Process Log
In the log file, the game data is stored in the format shown below:
```
Turn: <turn>
TankA: 
Current life point: <life point>, Current position: <coordinate>, Current direction: <direction>
TankB: 
Current life point: <life point>, Current position: <coordinate>, Current direction: <direction>
-------------------------------------------------------------------------
```

For example:
```
Turn: 29
TankA: 
Current life point: 5, Current position: (5, 6), Current direction: Down
TankB: 
Current life point: 3 Current position: (6, 1) Current direction: Right
-------------------------------------------------------------------------
```



## Notes

* Various colors are applied to distinguish tanks and messages
* The `log()` function appends tank status each turn to the log file
* Since the life point deduction of tanks is not clear enough, messages will appear to remind players when it happens
* There are also reminding messages when tanks are about to shoot

---






