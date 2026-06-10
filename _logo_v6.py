
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new2.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print("Original:", img.size)

# Encontrar bounding box del contenido (pixeles no-transparentes)
alpha = img.split()[3]
bbox = alpha.getbbox()
print("Content bbox:", bbox)

# Reducir el contenido un 10% por cada lado para recortar bien
if bbox:
    x1, y1, x2, y2 = bbox
    cw = x2 - x1
    ch = y2 - y1
    shrink_x = int(cw * 0.10)
    shrink_y = int(ch * 0.10)
    x1 = x1 + shrink_x
    y1 = y1 + shrink_y
    x2 = x2 - shrink_x
    y2 = y2 - shrink_y
    
    # Hacer cuadrado centrado en este nuevo bbox
    new_cw = x2 - x1
    new_ch = y2 - y1
    side = max(new_cw, new_ch)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    half = side // 2
    nx1 = max(0, cx - half)
    ny1 = max(0, cy - half)
    nx2 = min(img.width, nx1 + side)
    ny2 = min(img.height, ny1 + side)
    
    # Asegurar que sea cuadrado
    if nx2 - nx1 < ny2 - ny1:
        nx2 = nx1 + (ny2 - ny1)
    elif ny2 - ny1 < nx2 - nx1:
        ny2 = ny1 + (nx2 - nx1)
    
    print("Tight crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
    img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 900x900 (mas grande para que llene mejor el circulo)
from PIL import Image as Img
img = img.resize((900, 900), Img.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
