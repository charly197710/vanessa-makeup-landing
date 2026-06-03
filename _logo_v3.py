
from PIL import Image
import os

# Usar el archivo con fondo removido (97KB, 500x500, RGBA)
src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_nobg.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Source:", img.size, img.mode)

# La imagen es 500x500 RGBA con contenido de 400x332 en (56,77 a 456,409)
# Hacer crop centrado del contenido + padding
x1, y1, x2, y2 = 56, 77, 456, 409
pad = 20
x1 = max(0, x1 - pad)
y1 = max(0, y1 - pad)
x2 = min(img.width, x2 + pad)
y2 = min(img.height, y2 + pad)

# Hacer cuadrado
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

print("Crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
img = img.crop((nx1, ny1, nx2, ny2))

# Redimensionar a 600x600
img = img.resize((600, 600), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
