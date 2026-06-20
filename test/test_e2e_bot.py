import sys
import os
# pyrefly: ignore [missing-import]
import pygame

# 1. Run Pygame in Normal Mode (a window WILL pop up so you can watch the bot play)
# Comment these out to make it headless again
# os.environ["SDL_VIDEODRIVER"] = "dummy"
# os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.init()

# 2. Mock sys.exit to prevent the game from killing the testing script at the end
original_exit = sys.exit
def mock_exit(*args, **kwargs):
    pass
sys.exit = mock_exit

# 3. We will mock the keyboard state so our bot can press buttons programmatically
pressed_keys = {
    pygame.K_RIGHT: False,
    pygame.K_LEFT: False,
    pygame.K_SPACE: False,
    pygame.K_e: False,
    pygame.K_f: False,
    pygame.K_ESCAPE: False,
}

class MockKeys:
    def __getitem__(self, key):
        return 1 if pressed_keys.get(key, False) else 0

# This function overrides Pygame's default keyboard polling
def mock_get_pressed():
    return MockKeys()

pygame.key.get_pressed = mock_get_pressed

# 4. We patch pygame.display.flip() because it gets called exactly once per frame
original_flip = pygame.display.flip
frame_count = 0

def bot_logic():
    global frame_count
    frame_count += 1
    
    if 'GAMENIH' in sys.modules:
        game = sys.modules['GAMENIH']
        
        # --- BOT INSTRUCTIONS (Write your E2E Scenario here) ---
        
        # Bot: Bypass the main menu and go straight to the game!
        if frame_count == 1:
            game.game_state = "GAMEPLAY"
        
        # Bot: Move right for the first 60 frames
        if frame_count < 60:
            pressed_keys[pygame.K_RIGHT] = True
        else:
            pressed_keys[pygame.K_RIGHT] = False
            
        # Bot: Jump exactly at frame 60
        if frame_count == 60:
            pressed_keys[pygame.K_SPACE] = True
        else:
            pressed_keys[pygame.K_SPACE] = False
            
        # Bot: Shoot at frame 100
        if frame_count == 100:
            pressed_keys[pygame.K_e] = True
        else:
            pressed_keys[pygame.K_e] = False
            
        # Bot: Automatically end test after 150 frames by sending a QUIT event
        if frame_count > 150:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    return original_flip()

# Apply the patch
pygame.display.flip = bot_logic

print("--- Starting E2E Bot Test ---")

# 5. Load the game (this blocks and runs the entire game loop automatically)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import GAMENIH

print(f"--- Test Results ---")
print(f"Total Frames run: {frame_count}")
print(f"Final Score: {GAMENIH.score}")
print(f"Player Final HP: {GAMENIH.player.health}")
print(f"Did the player die?: {GAMENIH.is_game_over}")
