
from PIL import Image, ImageFilter, ImageEnhance
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_nobg.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Original:", img.size, img.mode)

# Crop al contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
pad = 25
x1 = max(0, bbox[0] - pad)
y1 = max(0, bbox[1] - pad)
x2 = min(img.width, bbox[2] + pad)
y2 = min(img.height, bbox[3] + pad)

# Hacer cuadrado
w = x2 - x1
h = y2 - y1
side = max(w, h)
cx = (x1 + x2) // 2
cy = (y1 + y2) // 2
half = side // 2
x1 = max(0, cx - half)
y1 = max(0, cy - half)
x2 = min(img.width, x1 + side)
y2 = min(img.height, y1 + side)

img = img.crop((x1, y1, x2, y2))
print("Cropped:", img.size)

# Escalado progresivo (mejor calidad que un solo paso)
# 500 -> 750 -> 1000 -> 1500
sizes = [750, 1000, 1500]
target = 1500

for s in sizes:
    if img.width < s:
        img = img.resize((s, s), Image.LANCZOS)
        print("Scaled to:", s)

# Ajustes para efecto 3D/HD
# Contraste
img = ImageEnhance.Contrast(img).enhance(1.4)
# Nitidez
img = ImageEnhance.Sharpness(img).enhance(1.6)
# Color
img = ImageEnhance.Color(img).enhance(1.15)

# Guardar
img.save(dst, "PNG", optimize=False)
print("Final:", img.size, "-", os.path.getsize(dst)//1024, "KB")
