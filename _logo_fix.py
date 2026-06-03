
from PIL import Image, ImageFilter
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_original.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
print(f"Original: {img.size}")

# Crear canal alpha basado en brillo (fondo oscuro = transparente)
pixels = img.load()
w, h = img.size
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        brightness = (r + g + b) / 3
        if brightness < 50:
            pixels[x, y] = (0, 0, 0, 0)

# Encontrar bounding box
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print(f"Content bbox: {bbox}")
    cw = x2 - x1
    ch = y2 - y1
    # Hacer cuadrado con un poco de padding
    side = max(cw, ch) + 40  # 20px padding cada lado
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    half = side // 2
    x1 = max(0, cx - half)
    y1 = max(0, cy - half)
    x2 = min(img.width, x1 + side)
    y2 = min(img.height, y1 + side)
    print(f"Crop: ({x1},{y1}) to ({x2},{y2})")
    img = img.crop((x1, y1, x2, y2))

# Redimensionar a 900x900 con alta calidad
img = img.resize((900, 900), Image.LANCZOS)
img.save(dst, "PNG")
print(f"Saved: {os.path.getsize(dst)//1024}KB - {img.size}")
