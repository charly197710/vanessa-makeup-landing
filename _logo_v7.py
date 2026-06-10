
from PIL import Image
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new2.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size

# Bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
print("Raw bbox:", bbox)

# Shrink del 5% para recortar bordes
x1, y1, x2, y2 = bbox
cw = x2 - x1
ch = y2 - y1
shrink_x = int(cw * 0.05)
shrink_y = int(ch * 0.05)
x1 += shrink_x
y1 += shrink_y
x2 -= shrink_x
y2 -= shrink_y

# Hacer cuadrado - usar el lado mas grande centrado
new_w = x2 - x1
new_h = y2 - y1
side = max(new_w, new_h)
cx = (x1 + x2) // 2
cy = (y1 + y2) // 2
half = side // 2
nx1 = max(0, cx - half)
ny1 = max(0, cy - half)
nx2 = min(img.width, nx1 + side)
ny2 = min(img.height, ny1 + side)

print("Crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 900x900
img = img.resize((900, 900), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
