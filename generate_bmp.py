import struct

def generate_handless_enemy_bmp(filename="handless_enemy.bmp"):
    width = 16
    height = 16
    scale = 16  # Scale up to 256x256
    
    # Colors (B, G, R)
    colors = {
        0: (0, 0, 0),         # Transparent (will use black for bmp background)
        1: (10, 20, 50),      # Dark outline
        2: (30, 120, 230),    # Main orange (BGR) -> wait, BGR for Orange is (0, 128, 255) roughly. Let's do (30, 120, 230) -> BGR: B=30, G=120, R=230
        3: (20, 20, 20),      # Black/dark for face
        4: (255, 255, 255),   # White eye glint / teeth
        5: (20, 90, 200),     # Shadow orange (BGR)
        6: (50, 150, 250),    # Highlight orange (BGR)
    }

    # 16x16 Pixel Art Matrix
    matrix = [
        [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,6,6,6,6,6,6,6,6,6,6,1,0,0],
        [0,1,6,2,2,2,2,2,2,2,2,2,2,6,1,0],
        [1,6,2,2,2,2,2,2,2,2,2,2,2,2,6,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,2,2,3,3,2,2,2,2,2,2,3,3,2,2,1],
        [1,2,2,2,3,3,2,2,2,2,3,3,2,2,2,1],
        [1,2,2,2,3,4,2,2,2,2,4,3,2,2,2,1],
        [1,2,2,2,3,3,2,2,2,2,3,3,2,2,2,1],
        [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
        [1,5,2,2,2,2,2,3,3,2,2,2,2,2,5,1],
        [1,5,2,2,2,2,3,4,4,3,2,2,2,2,5,1],
        [1,5,5,2,2,2,3,3,3,3,2,2,2,5,5,1],
        [0,1,5,5,5,2,2,2,2,2,2,5,5,5,1,0],
        [0,0,1,1,5,5,5,5,5,5,5,5,1,1,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    ]

    img_width = width * scale
    img_height = height * scale

    # BMP Header
    filesize = 54 + 3 * img_width * img_height
    header = struct.pack('<HL2H2L2H6L', 
        0x4D42, filesize, 0, 0, 54, 40, img_width, img_height, 1, 24, 0, 
        3 * img_width * img_height, 0, 0, 0, 0)

    with open(filename, 'wb') as f:
        f.write(header)
        
        # Write pixels (BMP is bottom-up, so we reverse the rows)
        for y in range(img_height - 1, -1, -1):
            row_data = bytearray()
            for x in range(img_width):
                orig_x = x // scale
                orig_y = y // scale
                color_index = matrix[orig_y][orig_x]
                
                # Use a dark gray for transparent background instead of pure black for better visibility
                if color_index == 0:
                    row_data.extend([40, 40, 40])  # Dark gray background
                else:
                    b, g, r = colors[color_index]
                    row_data.extend([b, g, r])
            
            # Padding for 4-byte alignment
            padding = (4 - (len(row_data) % 4)) % 4
            row_data.extend([0] * padding)
            
            f.write(row_data)

if __name__ == '__main__':
    generate_handless_enemy_bmp()
    print("Created handless_enemy.bmp")
