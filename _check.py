
from PIL import Image
img = Image.open(r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png")
print(f"Mode: {img.mode}")
print(f"Size: {img.size}")
# Check for alpha
if img.mode == 'RGBA':
    alpha = img.split()[3]
    bbox = alpha.getbbox()
    print(f"Alpha bbox: {bbox}")
else:
    print("No alpha channel - checking for white/black background...")
    # Sample corners
    corners = [(0,0), (0,img.height-1), (img.width-1,0), (img.width-1,img.height-1)]
    for x, y in corners:
        print(f"  Corner ({x},{y}): {img.getpixel((x,y))}")
