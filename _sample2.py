
from PIL import Image

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
img = Image.open(src)
print("Mode:", img.mode, "Size:", img.size)

# Muestrear esquinas
corners = [
    ("top-left", 0, 0),
    ("top-right", img.width-1, 0),
    ("bottom-left", 0, img.height-1),
    ("bottom-right", img.width-1, img.height-1),
    ("center", img.width//2, img.height//2),
]

for name, x, y in corners:
    pixel = img.getpixel((x, y))
    print(name, ":", pixel)

# Contar por brillo
bright = 0; dark = 0; mid = 0
step = 20
for y in range(0, img.height, step):
    for x in range(0, img.width, step):
        r, g, b = img.getpixel((x, y))
        avg = (r + g + b) / 3
        if avg > 200: bright += 1
        elif avg < 50: dark += 1
        else: mid += 1

total = bright + dark + mid
pct_b = bright * 100 // total if total else 0
pct_d = dark * 100 // total if total else 0
pct_m = mid * 100 // total if total else 0
print("Bright:", bright, "(" + str(pct_b) + "%)")
print("Dark:", dark, "(" + str(pct_d) + "%)")
print("Mid:", mid, "(" + str(pct_m) + "%)")
