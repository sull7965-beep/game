import unittest
import sys
import os
import ast
import math
from unittest.mock import MagicMock

class MockVector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return MockVector2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return MockVector2(self.x - other.x, self.y - other.y)
        
    def __mul__(self, scalar):
        return MockVector2(self.x * scalar, self.y * scalar)
        
    def normalize(self):
        length = math.hypot(self.x, self.y)
        if length == 0: 
            return MockVector2(0, 0)
        return MockVector2(self.x / length, self.y / length)
        
    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

class MockRect:
    def __init__(self, x, y, w, h, center=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        if center:
            self.x = center[0] - w/2
            self.y = center[1] - h/2
        self.topleft = (self.x, self.y)
        
    def colliderect(self, other):
        return not (self.x + self.width <= other.x or
                    self.x >= other.x + other.width or
                    self.y + self.height <= other.y or
                    self.y >= other.y + other.height)

class MockSurface:
    def __init__(self, size=(0,0), flags=0):
        self.size = size
        
    def get_width(self): 
        return self.size[0]
        
    def get_height(self): 
        return self.size[1]
        
    def get_rect(self, **kwargs):
        return MockRect(0, 0, self.size[0], self.size[1], **kwargs)
        
    def convert_alpha(self): 
        return self
        
    def convert(self): 
        return self
        
    def fill(self, color): 
        pass
        
    def blit(self, *args, **kwargs): 
        pass
        
    def set_alpha(self, alpha): 
        pass
        
    def set_colorkey(self, color): 
        pass
        
    def subsurface(self, rect): 
        return MockSurface((rect[2], rect[3]))

class MockImage:
    @staticmethod
    def load(path):
        return MockSurface((100, 100))

class MockTransform:
    @staticmethod
    def scale(surface, size):
        return MockSurface(size)
        
    @staticmethod
    def rotate(surface, angle):
        return surface
        
    @staticmethod
    def flip(surface, x, y):
        return surface

# Setup mock pygame
mock_pygame = MagicMock()
mock_pygame.Vector2 = MockVector2
mock_pygame.Rect = MockRect
mock_pygame.Surface = MockSurface
mock_pygame.image = MockImage
mock_pygame.transform = MockTransform
mock_pygame.SRCALPHA = 1
sys.modules['pygame'] = mock_pygame

# Load GAMENIH.py securely using AST to strip the main game loop and exit calls
def load_game_module():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GAMENIH.py')
    with open(file_path, 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    new_body = []
    
    for node in tree.body:
        # Remove top-level while loops (the game loop)
        if isinstance(node, ast.While):
            continue
            
        # Remove sys.exit() and pygame.quit() calls
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute):
                if func.attr == 'quit':
                    continue
                if getattr(func.value, 'id', '') == 'sys' and func.attr == 'exit':
                    continue
                    
        new_body.append(node)

    tree.body = new_body
    code = compile(tree, filename='GAMENIH.py', mode='exec')
    namespace = {}
    
    # Mock joystick method that would otherwise crash
    mock_pygame.joystick.get_count.return_value = 0
    
    exec(code, namespace)
    return namespace

game_module = load_game_module()

# Extract classes for testing
GameNode = game_module['GameNode']
PlayerBullet = game_module['PlayerBullet']
EnemyBullet = game_module['EnemyBullet']
HealItem = game_module['HealItem']

class TestGAMENIH(unittest.TestCase):

    def test_player_bullet_move(self):
        direction = MockVector2(1, 0)
        bullet = PlayerBullet(10, 20, direction)
        
        self.assertEqual(bullet.position.x, 10)
        self.assertEqual(bullet.position.y, 20)
        self.assertEqual(bullet.speed, 10)
        
        bullet.move()
        # After move, position should be (10 + 1*10, 20 + 0*10) = (20, 20)
        self.assertEqual(bullet.position.x, 20)
        self.assertEqual(bullet.position.y, 20)
        
    def test_player_bullet_get_rect(self):
        direction = MockVector2(1, 0)
        bullet = PlayerBullet(10, 20, direction)
        rect = bullet.get_rect()
        # get_rect returns Rect(x-5, y-5, size[0]+3, size[1]+3)
        self.assertEqual(rect.x, 5)
        self.assertEqual(rect.y, 15)
        self.assertEqual(rect.width, 13)
        self.assertEqual(rect.height, 8)

    def test_enemy_bullet_initialization(self):
        # direction should be normalized
        direction = MockVector2(3, 4) # length 5
        image = MockSurface()
        bullet = EnemyBullet(0, 0, direction, image)
        
        # 3/5 = 0.6, 4/5 = 0.8
        self.assertAlmostEqual(bullet.direction.x, 0.6)
        self.assertAlmostEqual(bullet.direction.y, 0.8)
        self.assertEqual(bullet.speed, 7)
        
    def test_enemy_bullet_move(self):
        direction = MockVector2(0, 1)
        image = MockSurface()
        bullet = EnemyBullet(100, 100, direction, image)
        
        bullet.move()
        self.assertAlmostEqual(bullet.position.x, 100)
        self.assertAlmostEqual(bullet.position.y, 107)

    def test_heal_item_rect(self):
        image = MockSurface()
        item = HealItem(50, 60, image)
        rect = item.get_rect()
        self.assertEqual(rect.x, 50)
        self.assertEqual(rect.y, 60)
        self.assertEqual(rect.width, 25)
        self.assertEqual(rect.height, 25)

    def test_game_node_initialization(self):
        node = GameNode(10, 20, (255, 0, 0), 50, 50, health=100)
        self.assertEqual(node.position.x, 10)
        self.assertEqual(node.position.y, 20)
        self.assertEqual(node.health, 100)
        self.assertEqual(node.max_health, 100)
        self.assertEqual(node.size, (50, 50))
        self.assertEqual(len(node.children), 0)

    def test_game_node_add_child(self):
        parent = GameNode(0, 0, None, 10, 10)
        child = GameNode(5, 5, None, 5, 5)
        parent.add_child(child)
        self.assertEqual(len(parent.children), 1)
        self.assertIs(parent.children[0], child)

    def test_game_node_get_rect(self):
        node = GameNode(15, 25, None, 40, 40)
        parent_pos = MockVector2(100, 100)
        rect = node.get_rect(parent_pos)
        # Parent position added to relative position
        self.assertEqual(rect.x, 115)
        self.assertEqual(rect.y, 125)
        self.assertEqual(rect.width, 40)
        self.assertEqual(rect.height, 40)

if __name__ == '__main__':
    unittest.main()
