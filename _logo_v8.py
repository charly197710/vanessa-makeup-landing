
from PIL import Image, ImageFilter, ImageEnhance
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new2.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print("Original:", img.size)

# Bounding box con shrink del 8%
alpha = img.split()[3]
bbox = alpha.getbbox()
x1, y1, x2, y2 = bbox
cw, ch = x2-x1, y2-y1
shrink_x = int(cw * 0.08)
shrink_y = int(ch * 0.08)
x1 += shrink_x
y1 += shrink_y
x2 -= shrink_x
y2 -= shrink_y

print("Content after shrink:", x1, y1, x2, y2, "=", x2-x1, "x", y2-y1)

# Hacer cuadrado usando el LADO MAS GRANDE
side = max(x2-x1, y2-y1)
cx, cy = (x1+x2)//2, (y1+y2)//2
half = side//2
nx1 = max(0, cx-half)
ny1 = max(0, cy-half)
nx2 = min(img.width, nx1+side)
ny2 = min(img.height, ny1+side)

# Si se sale de la imagen, ajustar
if nx2 > img.width:
    nx1 -= (nx2 - img.width)
    nx2 = img.width
if ny2 > img.height:
    ny1 -= (ny2 - img.height)
    ny2 = img.height

print("Final crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)

# Crear un canvas transparente cuadrado
canvas_size = max(nx2-nx1, ny2-ny1)
canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
cropped = img.crop((nx1, ny1, nx2, ny2))
paste_x = (canvas_size - cropped.width) // 2
paste_y = (canvas_size - cropped.height) // 2
canvas.paste(cropped, (paste_x, paste_y))

print("Canvas:", canvas_size, "x", canvas_size)

# Mejorar calidad para efecto HD/3D
canvas = ImageEnhance.Contrast(canvas).enhance(1.3)
canvas = ImageEnhance.Sharpness(canvas).enhance(1.4)
canvas = ImageEnhance.Color(canvas).enhance(1.15)

# Redimensionar a 900x900
canvas = canvas.resize((900, 900), Image.LANCZOS)
canvas.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", canvas.size)
