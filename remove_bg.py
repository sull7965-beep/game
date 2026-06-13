from PIL import Image

def remove_background(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    
    # Use newer API to avoid deprecation warning
    datas = list(img.getdata())
    
    new_data = []
    
    for item in datas:
        # Remove anything that is close to white to handle anti-aliasing edges
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")

input_image = r"C:\Users\user\.gemini\antigravity\brain\c6581452-4364-4bce-a41c-e3d2ed244233\glowing_short_blue_sword_1780135327352.png"
output_image = r"c:\Users\user\Downloads\akuuu\pedang_transparent.png"
remove_background(input_image, output_image)
print("Background removed and saved as pedang_transparent.png")
