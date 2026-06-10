
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Original:", img.size, "Mode:", img.mode)

# Convertir a RGBA si no lo es
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Encontrar bounding box del contenido no-transparente
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print("Content bbox:", bbox)
    cw = x2 - x1
    ch = y2 - y1
    print("Content size:", cw, "x", ch)
    
    # Padding del 5%
    pad = int(max(cw, ch) * 0.05)
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(img.width, x2 + pad)
    y2 = min(img.height, y2 + pad)
    
    # Hacer cuadrado centrado en el contenido
    w = x2 - x1
    h = y2 - y1
    side = max(w, h)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    half = side // 2
    nx1 = max(0, cx - half)
    ny1 = max(0, cy - half)
    nx2 = min(img.width, nx1 + side)
    ny2 = min(img.height, ny1 + side)
    
    print("Square crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
    img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 800x800
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
