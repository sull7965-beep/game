# Square Survivor

Square Survivor is a 2D survival game built with Python and Pygame. Survive as long as you can against endless waves of enemies!

## Gameplay
- **Player**: You play as **Sule**. You are equipped with a sword.
- **Enemies**: Beware of the incoming **Hugo** enemies from the left and right.
- **Combat**: Attack enemies by touching them with your sword. If enemies touch you, you will lose HP.
- **Healing**: Defeated enemies have a chance to drop healing items to restore your HP.
- **Leveling**: The game gets harder as your score increases, spawning more enemies faster.

## Controls
- **Right Arrow**: Move Right
- **Left Arrow**: Move Left

## Requirements
- Python 3.x
- Pygame

## How to Run

### Using pip
1. Make sure you have installed Pygame:
   ```bash
   pip install pygame
   ```
2. Run the main script:
   ```bash
   python GAMENIH.py
   ```

### Using uv
You can run the game directly using `uv` which will handle the `pygame` dependency automatically:
```bash
uv run --with pygame GAMENIH.py
```

## Running Tests
Unit tests are provided to verify the game logic (classes, movements, hitboxes) headlessly without launching the game window.

You can run the tests easily using `uv` (no additional dependencies needed as `pygame` is fully mocked for tests):
```bash
uv run python test/test_GAMENIH.py
```

## Assets
Make sure all necessary assets (images like `latar.png`, `player.png`, `enemy.png`, `pedang2.png`, etc., and sound files like `sound.ogg`, `levelup.ogg`, etc.) are placed in the same directory as the script before running the game.