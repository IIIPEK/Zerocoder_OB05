# Tetris Game

This project is a simple implementation of the classic Tetris game using Python and Pygame. It features:

- Smooth animations and responsive controls.
- Dynamic gameplay with increasing speed.
- Visual display for the next piece.
- Scoring system with bonuses for clearing multiple lines at once.

## Getting Started

Follow these steps to run the game on your system:

### Prerequisites

- Python 3.7 or later.
- Pygame library.

You can install the required library with pip:

```bash
pip install pygame
```

### Running the Game

1. Clone this repository or download the source files.
2. Run the `main.py` file:

```bash
python main.py
```

### Controls

- **Left Arrow**: Move piece left.
- **Right Arrow**: Move piece right.
- **Up Arrow**: Rotate piece.
- **Down Arrow**: Speed up piece.
- **Space**: Drop piece instantly.

## File Structure

- `main.py`: The entry point of the game.
- `tetris_game.py`: Contains the game logic and rendering.

## Game Features

1. **Shapes and Colors**: Includes all standard Tetris tetromino shapes, each with a unique color.
2. **Grid System**: The game grid ensures pieces fit naturally.
3. **Next Piece Preview**: Displays the next piece on the right side of the screen.
4. **Game Over Screen**: Displays "Game Over" when no more moves are possible.
5. **Score Tracking**: Awards points for clearing lines, with higher rewards for multiple lines cleared at once.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Pygame](https://www.pygame.org/) for the game development library.

Enjoy the game!
