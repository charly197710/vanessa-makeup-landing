
from PIL import Image, ImageFilter, ImageEnhance
import os

# Usar el archivo con fondo removido
src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_nobg.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src)
print("Original:", img.size, img.mode)

# 1. Encontrar el bounding box del contenido real
alpha = img.split()[3]
bbox = alpha.getbbox()
print("Content bbox:", bbox)

# 2. Crop al contenido + padding generoso
pad = 30
x1 = max(0, bbox[0] - pad)
y1 = max(0, bbox[1] - pad)
x2 = min(img.width, bbox[2] + pad)
y2 = min(img.height, bbox[3] + pad)

# Hacer cuadrado centrado
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

print("Square crop:", x1, y1, "to", x2, y2, "=", x2-x1, "x", y2-y1)
img = img.crop((x1, y1, x2, y2))

# 3. Redimensionar a 1200x1200 con maxima calidad (LANCZOS)
img = img.resize((1200, 1200), Image.LANCZOS)
print("Resized:", img.size)

# 4. Mejorar efecto 3D:
# a) Aumentar contraste para que los bordes se vean mas definidos
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.3)

# b) Aumentar nitidez para efecto HD
enhancer = ImageEnhance.Sharpness(img)
img = enhancer.enhance(1.5)

# c) Aumentar saturacion ligeramente para que los colores resalten
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(1.2)

# 5. Guardar como PNG de alta calidad
img.save(dst, "PNG", optimize=False)
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
