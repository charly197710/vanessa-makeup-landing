
from PIL import Image, ImageEnhance
import os

src = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_new3.png"
dst = r"C:\Users\WIN10\Desktop\vanessa-makeup\logo_circle.png"

img = Image.open(src).convert("RGBA")
w, h = img.size
print("Original:", img.size)

# Detectar fondo de esquinas
corners = [img.getpixel((0,0)), img.getpixel((w-1,0)), img.getpixel((0,h-1)), img.getpixel((w-1,h-1))]
print("Corners:", corners)

# Quitar fondo
bg_r = sum(c[0] for c in corners) // 4
bg_g = sum(c[1] for c in corners) // 4
bg_b = sum(c[2] for c in corners) // 4
tolerance = 35

pixels = img.load()
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if abs(r-bg_r)<tolerance and abs(g-bg_g)<tolerance and abs(b-bg_b)<tolerance:
            pixels[x, y] = (0, 0, 0, 0)

# Bounding box del contenido
alpha = img.split()[3]
bbox = alpha.getbbox()
print("Content bbox:", bbox)

# Shrink 6% para ajustar bordes
x1, y1, x2, y2 = bbox
cw, ch = x2-x1, y2-y1
sx = int(cw*0.06)
sy = int(ch*0.06)
x1+=sx; y1+=sy; x2-=sx; y2-=sy

# Hacer cuadrado centrado
side = max(x2-x1, y2-y1)
cx, cy = (x1+x2)//2, (y1+y2)//2
half = side//2
nx1=max(0,cx-half); ny1=max(0,cy-half)
nx2=min(img.width,nx1+side); ny2=min(img.height,ny1+side)

print("Square crop:", nx1, ny1, "to", nx2, ny2, "=", nx2-nx1, "x", ny2-ny1)
img = img.crop((nx1, ny1, nx2, ny2))

# Mejorar HD/3D
img = ImageEnhance.Contrast(img).enhance(1.35)
img = ImageEnhance.Sharpness(img).enhance(1.5)
img = ImageEnhance.Color(img).enhance(1.1)

# Redimensionar a 900x900
img = img.resize((900, 900), Image.LANCZOS)
img.save(dst, "PNG")
print("Saved:", os.path.getsize(dst)//1024, "KB -", img.size)
