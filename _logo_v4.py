
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print("Original:", img.size)

# Detectar color de fondo (muestrear esquinas)
corners = [
    img.getpixel((0, 0)),
    img.getpixel((w-1, 0)),
    img.getpixel((0, h-1)),
    img.getpixel((w-1, h-1)),
]
print("Corner colors:", corners)

# Usar el color mas comun de las esquina como fondo
from collections import Counter
# Simplificar colores (redondear a 16)
simplified = [(r//16*16, g//16*16, b//16*16, a) for r,g,b,a in corners]
bg_color = Counter(simplified).most_common(1)[0][0]
print("Detected bg color:", bg_color)

# Hacer transparente el color de fondo (con tolerancia)
pixels = img.load()
tolerance = 30
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if (abs(r - bg_color[0]) < tolerance and 
            abs(g - bg_color[1]) < tolerance and 
            abs(b - bg_color[2]) < tolerance):
            pixels[x, y] = (0, 0, 0, 0)

# Encontrar bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
if bbox:
    x1, y1, x2, y2 = bbox
    print("Content bbox:", bbox)
    cw = x2 - x1
    ch = y2 - y1
    
    # Padding del 5%
    pad = int(max(cw, ch) * 0.05)
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(img.width, x2 + pad)
    y2 = min(img.height, y2 + pad)
    
    # Hacer cuadrado
    side = max(x2-x1, y2-y1)
    cx = (x1+x2)//2
    cy = (y1+y2)//2
    half = side//2
    nx1 = max(0, cx-half)
    ny1 = max(0, cy-half)
    nx2 = min(img.width, nx1+side)
    ny2 = min(img.height, ny1+side)
    
    print("Square crop:", nx1, ny1, "to", nx2, ny2)
    img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 800x800
img = img.resize((800, 800), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
