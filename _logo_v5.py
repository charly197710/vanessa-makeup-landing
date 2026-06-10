
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new2.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print("Original:", img.size)

# Detectar color de fondo de las esquinas
corners = [
    img.getpixel((0, 0)),
    img.getpixel((w-1, 0)),
    img.getpixel((0, h-1)),
    img.getpixel((w-1, h-1)),
]
print("Corners:", corners)

# Color de fondo = promedio de las esquinas
bg_r = sum(c[0] for c in corners) // 4
bg_g = sum(c[1] for c in corners) // 4
bg_b = sum(c[2] for c in corners) // 4
print("BG color:", bg_r, bg_g, bg_b)

# Hacer transparente el fondo (con tolerancia amplia)
pixels = img.load()
tolerance = 40
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if (abs(r - bg_r) < tolerance and 
            abs(g - bg_g) < tolerance and 
            abs(b - bg_b) < tolerance):
            pixels[x, y] = (0, 0, 0, 0)

# Encontrar bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print("Content bbox:", bbox)
    cw = x2 - x1
    ch = y2 - y1
    print("Content size:", cw, "x", ch)
    
    # Padding del 4%
    pad = int(max(cw, ch) * 0.04)
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(img.width, x2 + pad)
    y2 = min(img.height, y2 + pad)
    
    # Hacer cuadrado centrado
    side = max(x2-x1, y2-y1)
    cx = (x1+x2)//2
    cy = (y1+y2)//2
    half = side//2
    nx1 = max(0, cx-half)
    ny1 = max(0, cy-half)
    nx2 = min(img.width, nx1+side)
    ny2 = min(img.height, ny1+side)
    
    print("Square crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
    img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 800x800
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
