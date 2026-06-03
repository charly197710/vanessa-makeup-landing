
from PIL import Image

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
img = Image.open(src)
print(f"Mode: {img.mode}, Size: {img.size}")

# Muestrear las esquinas y bordes para identificar el color de fondo
corners = {
    "top-left": (0, 0),
    "top-right": (img.width-1, 0),
    "bottom-left": (0, img.height-1),
    "bottom-right": (img.width-1, img.height-1),
    "center": (img.width//2, img.height//2),
    "top-mid": (img.width//2, 0),
    "bottom-mid": (img.width//2, img.height-1),
    "left-mid": (0, img.height//2),
    "right-mid": (img.width-1, img.height//2),
}

for name, (x, y) in corners.items():
    pixel = img.getpixel((x, y))
    print(f"  {name}: {pixel}")

# Contar pixels por brillo
bright = 0; dark = 0; mid = 0
for y in range(0, img.height, 10):
    for x in range(0, img.width, 10):
        r, g, b = img.getpixel((x, y))
        avg = (r + g + b) / 3
        if avg > 200: bright += 1
        elif avg < 50: dark += 1
        else: mid += 1

total = bright + dark + mid
print(f"
Pixel sampling (every 10px):")
print(f"  Bright (>200): {bright} ({bright*100//total}%)")
print(f"  Dark (<50): {dark} ({dark*100//total}%)")
print(f"  Mid: {mid} ({mid*100//total}%)")
