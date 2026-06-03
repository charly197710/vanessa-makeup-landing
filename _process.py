
from PIL import Image
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
        # Si el pixel es muy oscuro (fondo), hacerlo transparente
        if brightness < 40:
            pixels[x, y] = (0, 0, 0, 0)

# Encontrar bounding box del contenido visible
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print(f"Content bbox: {bbox}")
    cw = x2 - x1
    ch = y2 - y1
    side = max(cw, ch)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    half = side // 2
    x1 = max(0, cx - half)
    y1 = max(0, cy - half)
    x2 = min(img.width, x1 + side)
    y2 = min(img.height, y1 + side)
    print(f"Crop: ({x1},{y1}) to ({x2},{y2})")
    img = img.crop((x1, y1, x2, y2))

# Redimensionar
img = img.resize((600, 600), Image.LANCZOS)
img.save(dst, "PNG")
print(f"Saved: {os.path.getsize(dst)//1024}KB - {img.size}")
